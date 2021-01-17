import os
import sys
from shutil import copy2

from setuptools import setup

setup(
        name = "tvss",
        version = "1.0",
        url = "https://github.com/michaelgrossklos/tvshowsorter",
        author = "Michael Grossklos",
        description = "Sorting ripped or downloaded tv-shows into folders named after the seasons they're belonging to",
        author_email = "mail@grossklos.com",
        licence = "MIT",
        py_modules = ["tvss"],
        install_requires = [
            "Click",
            "Colorama",
            ],
        entry_points = '''
            [console_scripts]
            tvss=tvss:cli
        ''',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Environment :: Console',
            'Operating System :: OS Independent',
            ],
        python_requires = '~=3.7',
        )

"""
Copying the config file into the desired location ($HOME/.conf/tvss/tvss.json)
If the file already exists it will get overwritten.
Should work for all platforms.
"""
conf_path = os.path.join(os.path.expanduser('~'), '.config')
conf_tvss_path = os.path.join(conf_path, 'tvss')
conf_file_path = os.path.join(conf_tvss_path, 'tvss.json')

if conf_path:
    if not os.path.exists(conf_tvss_path):
        try:
            os.mkdir(conf_tvss_path)
        except FileNotFoundError as e:
            print(e)
    
    if os.path.exists(conf_file_path):
        try:
            os.remove(conf_file_path)
        except Exception as e:
            sys.exit(e)
    
    try:
        copy2('tvss.json', os.path.join(conf_path, 'tvss', 'tvss.json'), follow_symlinks = True)
    except FileExistsError as e:
        sys.exit(e)
