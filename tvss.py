"""
TV Show Sorter: Sorting ripped or downloaded tv-shows into folders
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


class TvShowSorter(object):
    
    def __init__(self, origin_path, destination_path, delete_folders, debug = False, \
                 language =
                 'de'):
        self.debug = debug
        self.config_file_path = os.path.join(Path.home(), '.config', 'tvss', 'tvss.json')
        self.conf = self.read_config_file()
        self.regex_season_episode = self.conf['REGEX']
        self.origin_path = home_path(origin_path or self.conf['default_paths']['ORIGIN_PATH'])
        self.destination_path = home_path(destination_path or self.conf['default_paths']['DESTINATION_PATH'])
        self.extensions = self.conf['FILE_EXTENSIONS']
        self.season = self.conf['LANGUAGES'][language]
        self.language = language
        self.LOG = start_logging(debug)
        self.titles = None
        self.delete_folders = delete_folders or False
        
        if self.delete_folders:
            message("warning", 'DELETING source folders is set!')
        
        try:
            os.chdir(home_path(self.conf['default_paths']['ORIGIN_PATH']))
            self.LOG.debug('Current working path: ' + os.getcwd())
        except FileNotFoundError as e:
            sys.exit(e)
    
    def read_config_file(self) -> dict:
        with open(self.config_file_path, "r") as f:
            conf = json.load(f)
        
        return conf
    
    def extend_file_extensions(self, file_extensions):
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
                message("error", "Extension already available. Type: 'tvss settings' to see all extensions")
    
    def echo_settings(self):
        click.clear()
        click.secho("ACTUAL SETTINGS FOR TVSS:", fg = "black", bold = True, bg = "cyan")
        click.secho("Regex for seasons: " + self.regex_season_episode, fg = "blue")
        click.secho("Origin/Source path: " + self.origin_path, fg = "blue")
        click.secho("Destination path: " + self.destination_path, fg = "blue")
        click.secho("File extensions available: " + str(self.extensions), fg = "blue")
        click.secho("Languages available: " + str([key for key in self.conf['LANGUAGES']]), fg = "blue")
        click.secho("Language set: " + self.language, fg = "blue")
        click.secho("Season is called: " + self.season + "\n", fg = "blue")
        click.secho("More information on:", fg = "black", bg = "cyan", bold = True)
        click.secho("https://github.com/michaelgrossklos/tvshowsorter" + "\n", fg = "cyan", bold = True)
    
    def walk_origin_show_files(self) -> None:
        for f in listdir('.'):
            self.LOG.debug(self.titles)
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
                                        self.destination_path, self.season + " " + season_episode.group(2)[1:])
                                
                                make_season_path(season_path)
                                
                                from_file = os.path.join(self.origin_path, dir_path, f_name + f_ext)
                                to_file = os.path.join(season_path, title + " " + season_episode.group(1) + f_ext)
                                
                                if not os.path.isfile(to_file):
                                    shutil.copy2(from_file, to_file)
                                
                                if self.delete_folders:
                                    message("warning", "Deleting: " + os.path.join(self.origin_path, dir_path))
                                    shutil.rmtree(os.path.join(self.origin_path, dir_path))


def message(msg_type, msg):
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


def set_titles(self, tv_show_titles) -> None:
    if not tv_show_titles:
        sys.exit('You need to provide at least one title...')
    
    self.titles = tv_show_titles
    self.LOG.debug(self.titles)


def make_season_path(path: str):
    if not os.path.exists(path):
        try:
            Path(path).mkdir(parents = True, exist_ok = True)
        except PermissionError as e:
            sys.exit(e)


def make_regex_show_title(title: str) -> str:
    s_title = title.lower().split()
    divider = "(?:.*)?"
    title = r"" + divider + divider.join(s_title) + divider
    
    return title


def home_path(path: str) -> str:
    return os.path.join(Path.home(), path)


def start_logging(debug) -> logging.Logger:
    logging.basicConfig(level = logging.WARNING, format = "%(msg)s")
    
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    return logging.getLogger('logtext')


@click.group()
@click.option(
        "--origin-path", "-o",
        required = False,
        type = click.Path(exists = True, resolve_path = True, writable = True, readable = True,
                          path_type = click.STRING),
        help = "The path to the source files to sort"
        )
@click.option(
        "--destination-path", "-d",
        required = False,
        type = click.Path(exists = True, resolve_path = True, writable = True, readable = True,
                          path_type = click.STRING),
        help = "The path where to save the sorted files"
        )
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
@click.pass_context
def cli(ctx, origin_path, destination_path, delete_folders, debug, language):
    """
    Sorting your ripped or downloaded tv-shows into folders named after the seasons they're belonging to (f.e.: Season
    01).
    Renames all files like "Name Of Show s01e01.ext" for direct use in your
    media center like Plex or Emby. So it can find all meta data needed.
    """
    click.clear()
    click.echo(
            "------------------------------------------------------------------------------------------------\n"
            "TV Show Sorter: Sorting ripped or downloaded tv-shows into folders\n"
            "Copyright (C) 2021 Michael Grossklos (mail@grossklos.com)\n"
            "https://github.com/michaelgrossklos/tvshowsorter\n"
            "------------------------------------------------------------------------------------------------\n"
            "This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to\n"
            "redistribute it under certain conditions;\n"
            "go to: https://www.gnu.org/licenses/gpl-3.0.html for details.\n"
            "------------------------------------------------------------------------------------------------\n")
    ctx.obj = TvShowSorter(origin_path, destination_path, delete_folders, debug, language)
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
    Extends the list of file extensions. Type: 'tvss settings' to the the actual list.
    """
    ctx.obj.extend_file_extensions(file_extensions)
