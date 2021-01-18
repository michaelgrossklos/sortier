import json
import os
import sys
from pathlib import Path
from shutil import copy2

import setuptools
from setuptools import setup

with open("README.adoc", "r", encoding = "utf-8") as f:
    long_description = f.read()

setup(
        name = "sortier",
        version = "1.0",
        url = "https://github.com/michaelgrossklos/sortier",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        package = setuptools.find_packages(),
        author = "Michael Grossklos",
        description = "Sorting ripped or downloaded tv-shows into folders named after the seasons they're belonging to",
        author_email = "mail@grossklos.com",
        licence = "GNU v3",
        py_modules = ["sortier.sortier"],
        install_requires = [
            "click",
            "colorama",
            ],
        entry_points = '''
            [console_scripts]
            sortier=sortier.sortier:cli
        ''',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Programming Language :: Python :: 3',
            'Environment :: Console',
            'Operating System :: OS Independent',
            ],
        python_requires = '>=3.7',
        )

"""
Copying the config file into the desired location ($HOME/.conf/tvss/sortier.json)
If the file already exists it will get overwritten.
Should work for all platforms.
"""
conf_path = os.path.join(Path.home(), '.config')
conf_sortier_path = os.path.join(conf_path, 'sortier')
conf_file_path = os.path.join(conf_sortier_path, 'sortier.json')


def read_config_file():
    with open(conf_file_path, "r") as f:
        conf = json.load(f)
    
    return conf


if conf_path:
    if not os.path.exists(conf_sortier_path):
        try:
            Path(conf_sortier_path).mkdir(parents = True, exist_ok = True)
        except FileNotFoundError as e:
            print(e)
    
    if os.path.exists(conf_file_path):
        try:
            os.remove(conf_file_path)
        except Exception as e:
            sys.exit(e)
    
    try:
        copy2('sortier/sortier.json', os.path.join(conf_path, 'sortier', 'sortier.json'),
              follow_symlinks = True)
    except FileExistsError as e:
        sys.exit(e)

conf = read_config_file()

conf['default_paths']['ORIGIN_PATH'] = os.path.join("Downloads", "extracted")
conf['default_paths']['DESTINATION_PATH'] = os.path.join("Downloads", "extracted", "SORTED")

try:
    with open(conf_file_path, "w") as f:
        json.dump(conf, f, indent = 4)
except FileNotFoundError as e:
    print(e)
except PermissionError as e:
    print(e)
except Exception as e:
    print(e)
