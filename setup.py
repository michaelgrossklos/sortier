import os
import sys
from shutil import copy2

from setuptools import setup

setup(
        name = "tvss",
        version = "0.1",
        url = "https://github.com/michaelgrossklos/tvshowsorter",
        author = "Michael Grossklos",
        author_email = "mail@grossklos.com",
        licence = "MIT",
        py_modules = ["tvss"],
        install_requires = [
            "Click",
            ],
        entry_points = '''
            [console_scripts]
            tvss=tvss:cli
        ''',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: End User',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            ],
        python_requires = '~=3.7',
        )

"""
Copying the config file into the desired location ($HOME/.conf/tvss/.tvss)
If the file already exists it will get overwritten.
Should work for all platforms.
"""
conf_path = os.path.join(os.path.expanduser('~'), '.config')
conf_tvss_path = os.path.join(conf_path, 'tvss')
conf_file_path = os.path.join(conf_tvss_path, '.tvss')

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
        copy2('.tvss', os.path.join(conf_path, 'tvss', '.tvss'), follow_symlinks = True)
    except FileExistsError as e:
        sys.exit(e)
