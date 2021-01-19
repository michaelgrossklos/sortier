"""
Sortier: Sorting ripped or downloaded tv-shows into folders
Copyright (C) 2021  Michael Grossklos (mail@grossklos.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import logging
import os
import re
import shutil
import sys
from os import listdir
from pathlib import Path

import click


class Sortier(object):
    """
    The main class with all the functionality.
    This class gets called at different placed an is also needed to start the program.
    """
    
    '''
    TODO: According to the Plex naming convetions, we need to implement more options
    https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/
    
    '''
    
    def __init__(self, delete_folders, date, debug = False, language = 'de'):
        self.debug = debug
        self.date = date
        self.config_file_path = os.path.join(Path.home(), '.config', 'sortier', 'sortier.json')
        self.conf = self.read_config_file()
        self.regex_season_episode = self.conf['REGEX']
        self.origin_path = home_path(self.conf['default_paths']['ORIGIN_PATH'])
        self.destination_path = home_path(self.conf['default_paths']['DESTINATION_PATH'])
        self.extensions = self.conf['FILE_EXTENSIONS']
        self.season = self.conf['LANGUAGES'][language]
        self.language = language
        self.LOG = start_logging(debug)
        self.titles = None
        self.delete_folders = delete_folders or False
        
        if self.delete_folders:
            message("warning", 'DELETING source folders is ON!')
    
    def make_show_title(self, name: str, season: str) -> str:
        """
        Makes the full title of the tv-show
        :param name: The name of the show
        :type: str
        :param season: The season and episode of the tv-show
        :type: str
        :return: The whole title of the tv-show
        :rtype: str
        """
        if self.date:
            return f"{name} - {season} - {self.date}"
        else:
            return f"{name} - {season}"
    
    def read_config_file(self) -> dict:
        """
        Opens and reads in the config file and sets it to an variable.
        :return conf: dict
        """
        with open(self.config_file_path, "r") as f:
            conf = json.load(f)
        
        return conf
    
    def change_path_settings(self, origin_path = None, destination_path = None) -> None:
        """
        Changes either the destination or the origin path in config file
        Gets called by two commands: destpth & oripath
        :param origin_path: Path to original video files
        :type: str
        :param destination_path: Path to where to save the sorted video files
        :type: str
        :return: None
        """
        if origin_path:
            path = home_path(origin_path)
        else:
            path = home_path(destination_path)
        
        self.LOG.debug("Trying to change path: " + path)
        
        self.LOG.debug("Reading config file ...")
        conf = self.read_config_file()
        
        if origin_path and conf['default_paths']['ORIGIN_PATH'] != origin_path:
            conf['default_paths']['ORIGIN_PATH'] = origin_path
        elif destination_path and conf['default_paths']['DESTINATION_PATH'] != destination_path:
            conf['default_paths']['DESTINATION_PATH'] = destination_path
        else:
            message("error", "Path: " + path + " already set. Type 'sortier settings' to see all path")
            return
        
        try:
            self.LOG.debug("Writing path to config file...")
            with open(self.config_file_path, "w") as f:
                json.dump(conf, f, indent = 4)
        except FileNotFoundError as e:
            self.LOG.debug(e)
        except PermissionError as e:
            self.LOG.debug(e)
        except Exception as e:
            self.LOG.debug(e)
        
        message("info", "Path: " + path + " changed successfully")
    
    def extend_file_extensions(self, file_extensions: dict) -> None:
        """
        Extends the list of file extentions in the config file.
        :param file_extensions: The extensions including "." (dot)
        :type: dict
        :return: None
        """
        self.LOG.debug("Trying to add file extensions: " + str(file_extensions))
        
        for x in file_extensions:
            if x not in self.extensions:
                self.LOG.debug(str(file_extensions) + " is not available in config file")
                conf = self.read_config_file()
                
                for e in file_extensions:
                    self.extensions.append(e)
                
                conf['FILE_EXTENSIONS'] = self.extensions
                
                try:
                    self.LOG.debug("Writing extensions to config file...")
                    with open(self.config_file_path, "w") as f:
                        json.dump(conf, f, indent = 4)
                except FileNotFoundError as e:
                    self.LOG.debug(e)
                except PermissionError as e:
                    self.LOG.debug(e)
                except Exception as e:
                    self.LOG.debug(e)
            else:
                message("error", "Extensions already available. Type: 'sortier settings' to see all extensions")
    
    def echo_settings(self) -> None:
        """
        Prints the actual settings (from sortier.json) to the commandline.
        Gets called by the command: settings
        :return: None
        """
        click.clear()
        click.secho("ACTUAL SETTINGS FOR SORTIER:", fg = "white", bold = True, bg = "cyan")
        click.secho("Regex for seasons: " + self.regex_season_episode, fg = "blue")
        click.secho("Origin/Source path: " + self.origin_path, fg = "blue")
        click.secho("Destination path: " + self.destination_path, fg = "blue")
        click.secho("File extensions available: " + str(self.extensions), fg = "blue")
        click.secho("Languages available: " + str([key for key in self.conf['LANGUAGES']]), fg = "blue")
        click.secho("Language set: " + self.language, fg = "blue")
        click.secho("Season is called: " + self.season + "\n", fg = "blue")
        click.secho("More information on:", fg = "white", bg = "cyan", bold = True)
        click.secho("Github: https://github.com/michaelgrossklos/sortier", fg = "cyan", bold = True)
        click.secho("Discord: https://discord.gg/y5Kx2UGxhQ" + "\n", fg = "cyan", bold = True)
    
    def set_titles(self, tv_show_titles: dict) -> None:
        """
        Sets the titles provided by the user to the corresponding variable.
        Gets called by command: titles
        :param tv_show_titles: The titles provided by user input
        :return: None
        """
        if not tv_show_titles:
            sys.exit('You need to provide at least one title...')
        
        self.titles = tv_show_titles
        self.LOG.debug(self.titles)
    
    def walk_origin_show_files(self) -> None:
        """
        The actual worker.
        Sorts, renames and copies the video files and makes the needed paths
        :return: None
        """
        try:
            os.chdir(home_path(self.conf['default_paths']['ORIGIN_PATH']))
            self.LOG.debug('Current working path: ' + os.getcwd())
        except FileNotFoundError as e:
            sys.exit(e)
        
        for f in listdir('.'):
            self.LOG.debug(f)
            for title in self.titles:
                if not re.search(make_regex_show_title(title), f, re.IGNORECASE):
                    continue
                
                for dir_path, dir_names, file_names in os.walk(f):
                    for filename in file_names:
                        f_name, f_ext = os.path.splitext(filename)
                        
                        for i in self.extensions:
                            if f_ext == i and f_name.find('sample') == -1:
                                message("info", "Match found: " + f_name)
                                
                                season_episode = re.search(self.regex_season_episode, f_name, re.IGNORECASE)
                                
                                season_path = os.path.join(
                                        self.destination_path, title, self.season + " " + season_episode.group(2))
                                
                                make_season_path(season_path)
                                
                                from_file = os.path.join(self.origin_path, dir_path, f_name + f_ext)
                                to_file = os.path.join(season_path, self.make_show_title(title, season_episode.group(
                                        1)) + f_ext)
                                
                                if not os.path.isfile(to_file):
                                    shutil.copy2(from_file, to_file)
                                
                                if self.delete_folders:
                                    message("warning", "Deleting: " + os.path.join(self.origin_path, dir_path))
                                    shutil.rmtree(os.path.join(self.origin_path, dir_path))


def message(msg_type: str, msg: str) -> None:
    """
    Helper function to provide a prettyfied colored message depending on type.
    :param msg_type: The type of message; either info, error or warning
    :type: str
    :param msg: The actual message
    :type: str
    :return: None
    """
    TYPE = {
        "error":   "[ERROR]",
        "warning": "[WARNING]",
        "info":    "[INFO]",
        }
    COLOR = {
        "error":   "red",
        "warning": "yellow",
        "info":    "blue",
        }
    
    click.secho(TYPE[msg_type] + " " + msg, fg = COLOR[msg_type], bold = True)


def make_season_path(path: str) -> None:
    """
    Makes the path for a season depending to a show.
    :param path: The complete path for the folder
    :type: str
    :return: None
    """
    if not os.path.exists(path):
        try:
            Path(path).mkdir(parents = True, exist_ok = True)
        except PermissionError as e:
            sys.exit(e)


def make_regex_show_title(title: str) -> str:
    """
    Makes a regex expression out of the user given title.
    Is needed to find the titles in the folder names.
    :param title: The title of an tv-show
    :return: The regular expression of the given title.
    :rtype: str
    """
    s_title = title.lower().split()
    divider = "(?:.*)?"
    title = r"" + divider + divider.join(s_title) + divider
    
    return title


def home_path(path: str) -> str:
    """
    The home path is the path to the current users folder. It can vary depending on OS.
    This function gets the correct path and concatenates the given path to it.
    It gets rid of eventual pefixed slashes
    :param path: The path under the current users home folder.
    :type_ str
    :return: The complete path including the home folder.
    :rtype: str
    """
    if path[:1] == os.fspath("/"):
        path = path[1:]
    
    return os.path.join(Path.home(), path)


def start_logging(debug: str) -> logging.Logger:
    """
    Starts the logging depending on the logging level
    :param debug: The logging level (info, debug, error, fatal)
    :type: str
    :return: The logger itself
    :rtype: Logger
    """
    logging.basicConfig(level = logging.WARNING, format = "%(msg)s")
    
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    return logging.getLogger('logtext')


@click.group()
@click.option(
        "--language", "-l",
        required = False,
        default = "de",
        type = click.STRING,
        help = "Sets the language for season names"
        )
@click.option(
        "--debug/--no-debug",
        default = False,
        help = "Turn debug mode on"
        )
@click.option("--delete-folders",
              default = False,
              type = click.BOOL,
              help = "Delete the source folder after copying the file"
              )
@click.option(
        "--date",
        default = None,
        type = click.STRING,
        help = "For date based tv-shows"
        )
@click.pass_context
def cli(ctx, delete_folders, date, debug, language):
    """
    Sorting your ripped or downloaded tv-shows into folders named after the seasons they're belonging to (f.e.: Season
    01). Renames all files like "Name Of Show s01e01.ext" for direct use in your media center like Plex or Emby. So
    it can find all meta data needed.
    """
    click.clear()
    click.echo(
            "------------------------------------------------------------------------------------------------\n"
            "Sortier: Sorting ripped or downloaded tv-shows into folders\n"
            "Copyright (C) 2021 Michael Grossklos (mail@grossklos.com)\n"
            "Github: https://github.com/michaelgrossklos/sortier\n"
            "Discord: https://discord.gg/y5Kx2UGxhQ\n"
            "------------------------------------------------------------------------------------------------\n"
            "This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to\n"
            "redistribute it under certain conditions;\n"
            "go to: https://www.gnu.org/licenses/gpl-3.0.html for details.\n"
            "------------------------------------------------------------------------------------------------\n")
    ctx.obj = Sortier(delete_folders, date, debug, language)
    ctx.obj.LOG.debug('Starting CLI...')


@cli.command()
@click.argument('tv_show_titles', nargs = -1)
@click.pass_context
def titles(ctx, tv_show_titles):
    """
    The titles of the shows to be sorted. REQUIRED!
    """
    ctx.obj.LOG.debug('Calling command titles...')
    ctx.obj.set_titles(tv_show_titles)
    ctx.obj.walk_origin_show_files()


@cli.command()
@click.pass_context
def settings(ctx):
    """
    Shows the actual settings
    """
    ctx.obj.echo_settings()


@cli.command()
@click.argument('file_extensions', nargs = -1)
@click.pass_context
def addextensions(ctx, file_extensions):
    """
    Extends the list of file extensions. Type: 'sortier settings' to the the actual list.
    """
    ctx.obj.extend_file_extensions(file_extensions)


@cli.command()
@click.argument('destpath', default = None, type = click.STRING)
@click.pass_context
def destpath(ctx, destpath):
    """
    Changes the destination path permanently
    """
    ctx.obj.change_path_settings(None, destpath)


@cli.command()
@click.argument('oripath', default = None, type = click.STRING)
@click.pass_context
def oripath(ctx, oripath):
    """
    Changes the origin path permanently
    """
    ctx.obj.change_path_settings(oripath, None)
