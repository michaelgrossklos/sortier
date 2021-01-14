import glob
import logging
import os
import re
import shutil
import sys
from configparser import ConfigParser
from pathlib import Path

import click


class TvShowSorter(object):
    logging.basicConfig(level = logging.WARNING, format = "%(msg)s")
    
    LANGUAGE = {
        'de': 'Staffel',
        'en': 'Season',
        'es': 'Temporada',
        'fr': 'Saison',
        'it': 'Stagione',
        'ru': 'Sezon',
        }
    
    def __init__(self, language, origin_path, destination_path, extensions, debug = False):
        self.debug = debug
        self.conf = self.read_config_file()
        self.regex_season_episode = self.conf['files']['regex']
        self.origin_path = origin_path or self.conf['paths']['origin_path']
        self.destination_path = destination_path or self.conf['paths']['destination_path']
        self.extensions = extensions or self.conf['files']['video_file_ext']
        self.season = TvShowSorter.LANGUAGE[language]
        self.LOG = self.start_logging()
        self.titles = []
        
        try:
            os.chdir(self.conf['paths']['origin_path'])
        except FileNotFoundError as e:
            sys.exit(e)
    
    def start_logging(self) -> logging.Logger:
        if self.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        
        return logging.getLogger('logtext')
    
    @staticmethod
    def read_config_file() -> dict:
        conf = ConfigParser()
        path = os.path.join(Path.home(), '.config', 'tvss', '.tvss')
        conf.read(path)
        click.echo(conf['paths']['origin_path'])
        
        return conf
    
    @staticmethod
    def make_show_title_regex(title: str) -> str:
        s_title = title.split()
        divider = ".*"
        title = r".*" + divider.join(s_title) + ".*"
        
        return title
    
    def make_destination_dir(self) -> None:
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)
    
    def walk_show_files(self) -> None:
        for f in glob.glob(".", recursive = True):
            for title in self.titles:
                if not re.search(self.make_show_title_regex(title), f, re.IGNORECASE):
                    continue
                
                for dir_path, dir_names, file_names in os.walk(f):
                    for filename in file_names:
                        f_name, f_ext = os.path.splitext(filename)
                        
                        for i in self.extensions:
                            if f_ext == i and f_name.find('sample') == -1:
                                click.echo('Found: ', f_name)
                                
                                season_episode = re.search(self.regex_season_episode, f_name, re.IGNORECASE)
                                click.echo('Episode: ', season_episode)
                                
                                season_path = os.path.join(
                                        self.destination_path, self.season + " " + season_episode.group(2)[1:])
                                
                                if not os.path.exists(season_path):
                                    os.mkdir(season_path)
                                
                                from_dir = os.path.join(self.origin_path, dir_path, f_name + f_ext)
                                to_dir = os.path.join(season_path, title + " " + season_episode.group(1) + f_ext)
                                
                                if not os.path.isfile(to_dir):
                                    shutil.copy2(from_dir, to_dir)
    
    def set_titles(self, tv_show_titles: list) -> None:
        self.titles = tv_show_titles


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
@click.pass_context
def cli(ctx, language, origin_path, destination_path, extensions, debug):
    """
    Sorting your ripped or downloaded tv-shows into folder of seasons.
    Renames all files like "Name Of Show s01e01.ext" for direct use in your
    media center like Plex. So it can find all meta data needed.
    """
    ctx.obj = TvShowSorter(language, origin_path, destination_path, extensions, debug)


@cli.command()
@click.argument('tv_show_titles', nargs = -1)
@click.pass_context
def titles(ctx, tv_show_titles):
    """
    The titles of the shows to be sorted. REQUIRED!
    """
    ctx.obj.set_titles(tv_show_titles)
