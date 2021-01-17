import os
import sys
from shutil import copy2

from setuptools import setup

setup(
        name = "sortier",
        version = "1.0",
        url = "https://github.com/michaelgrossklos/tvshowsorter",
        author = "Michael Grossklos",
        description = "Sorting ripped or downloaded tv-shows into folders named after the seasons they're belonging to",
        author_email = "mail@grossklos.com",
        licence = "GNU v3",
        py_modules = ["sortier"],
        install_requires = [
            "click",
            "colorama",
            ],
        entry_points = '''
            [console_scripts]
            sortier=sortier:cli
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
Copying the config file into the desired location ($HOME/.conf/tvss/sortier.json)
If the file already exists it will get overwritten.
Should work for all platforms.
"""
conf_path = os.path.join(os.path.expanduser('~'), '.config')
conf_sortier_path = os.path.join(conf_path, 'sortier')
conf_file_path = os.path.join(conf_sortier_path, 'sortier.json')

if conf_path:
    if not os.path.exists(conf_sortier_path):
        try:
            os.mkdir(conf_sortier_path)
        except FileNotFoundError as e:
            print(e)
    
    if os.path.exists(conf_file_path):
        try:
            os.remove(conf_file_path)
        except Exception as e:
            sys.exit(e)
    
    try:
        copy2('sortier.json', os.path.join(conf_path, 'sortier', 'sortier.json'), follow_symlinks = True)
    except FileExistsError as e:
        sys.exit(e)
