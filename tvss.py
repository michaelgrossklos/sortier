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
    
    def __init__(self, origin_path, destination_path, extensions, delete_folders, debug = False, language = 'de'):
        self.debug = debug
        self.conf = read_config_file()
        self.regex_season_episode = self.conf['REGEX']
        self.origin_path = home_path(origin_path or self.conf['default_paths']['ORIGIN_PATH'])
        self.destination_path = home_path(destination_path or self.conf['default_paths']['DESTINATION_PATH'])
        self.extensions = extensions or self.conf['extensions']['FILE_EXTENSIONS']
        self.season = self.conf['LANGUAGES'][language]
        self.LOG = start_logging(debug)
        self.titles = None
        self.delete_folders = delete_folders or False
        
        try:
            os.chdir(home_path(self.conf['default_paths']['ORIGIN_PATH']))
            self.LOG.debug('CWD: ' + os.getcwd())
        except FileNotFoundError as e:
            sys.exit(e)
    
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
                                self.LOG.debug('Match found: ' + f_name)
                                
                                season_episode = re.search(self.regex_season_episode, f_name, re.IGNORECASE)
                                
                                season_path = os.path.join(
                                        self.destination_path, self.season + " " + season_episode.group(2)[1:])
                                
                                make_season_path(season_path)
                                
                                from_file = os.path.join(self.origin_path, dir_path, f_name + f_ext)
                                to_file = os.path.join(season_path, title + " " + season_episode.group(1) + f_ext)
                                
                                if not os.path.isfile(to_file):
                                    shutil.copy2(from_file, to_file)
                                
                                if self.delete_folders:
                                    click.echo('Deleting: ' + os.path.join(self.origin_path, dir_path))
                                    shutil.rmtree(os.path.join(self.origin_path, dir_path))
    
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


def read_config_file() -> dict:
    path = os.path.join(Path.home(), '.config', 'tvss', 'tvss.json')
    
    with open(path, "r") as f:
        conf = json.load(f)
    
    return conf


def home_path(path: str) -> str:
    return os.path.join(Path.home(), path)


def start_logging(debug) -> logging.Logger:
    logging.basicConfig(level = logging.WARNING, format = "%(msg)s")
    
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    return logging.getLogger('logtext')


@click.group()
@click.option(
        "--debug/--no-debug",
        envvar = "TVSS_DEBUG",
        default = False,
        help = "Turn debug mode on"
        )
@click.option(
        "--origin-path", "-o",
        envvar = "TVSS_ORIGIN_PATH",
        required = False,
        type = click.Path(exists = True, resolve_path = True, writable = True, readable = True,
                          path_type = click.STRING),
        help = "The path to the source files to sort"
        )
@click.option(
        "--destination-path", "-d",
        envvar = "TVSS_DESTINATION_PATH",
        required = False,
        type = click.Path(exists = True, resolve_path = True, writable = True, readable = True,
                          path_type = click.STRING),
        help = "The path where to save the sorted files"
        )
@click.option(
        "--extensions",
        envvar = "TVSS_EXTENSION",
        required = False,
        help = "To extend the list of video file extensions"
        )
@click.option(
        "--language", "-l",
        envvar = "TVS_LANGUAGE",
        required = False,
        default = "de",
        type = click.STRING,
        help = "Sets the language for season names"
        )
@click.option("--delete-folders",
              envvar = "TVS_DELETE_FOLDERS",
              default = False,
              type = click.BOOL,
              help = "Delete the source folder after copying the file"
              )
@click.pass_context
def cli(ctx, origin_path, destination_path, extensions, delete_folders, debug, language):
    """
    Sorting your ripped or downloaded tv-shows into folder of seasons.
    Renames all files like "Name Of Show s01e01.ext" for direct use in your
    media center like Plex. So it can find all meta data needed.
    """
    print('CLI')
    ctx.obj = TvShowSorter(origin_path, destination_path, extensions, delete_folders, debug, language)


@cli.command()
@click.argument('tv_show_titles', nargs = -1)
@click.pass_context
def titles(ctx, tv_show_titles):
    """
    The titles of the shows to be sorted. REQUIRED!
    """
    ctx.obj.set_titles(tv_show_titles)
    ctx.obj.walk_origin_show_files()
