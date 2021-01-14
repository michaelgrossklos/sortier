# Tv-Show Sorter (TVSS)

This tool is capable to sort any kind of tv shows. During the process, all files get unpacked (if needed) and all video files will be renamed, sorted
into season named folders and saved wherever you desire. So it is possible to upload the files to your media server like Plex or Empy. These media
centers need the correct naming convention in order to find all the metadata like posters, background images and other information.

The seasons need to be in a folder called like the season. F.e.: "Season 01". Also, the videos itself need to follow these kind opf conventions. Files
need to be named like this: "Game OF Thrones (2011) s01e01.mkv". This very tools does it for you.

### Renaming files

The files to be renamed are only the video files. You can specify their extension (defaults: *.mkv, *.avi, *.mp4, *.mov) by using the
parameter ``--extensions``.

#### File name a.k.a titles (required)

In order to rename and more importantly find the right files, you need to provide the title of the show. It is the only required parameter. For
example "Game Of Thrones". Capitalization gets ignored. In order to do that, you need to use the parameter ``--title`` in binding with a list of
titles: f.e. ``tvss --title ['game of thrones', 'boston legal', 'friends']``
You get the idea. If you only need to specify one name, just do ``tvss --title ['game of thones']``.

#### File extensions

Not always, but most of the time, are the provided default file extensions sufficient. So you need to extend the list by the file extensions you need
for the actual tv shows. There are two options to do so.

##### Option 1

Temporarily add the extensions just for this one time by using the parameter ``--extensions``. You need to provide a list of extensions: f.e.:
``tvss --extensions ['.wmv', '.flv']``. Notice the dot in front of the extension! Like explained above you also can specify just one extension by
using ``tvss --extension ['.wmv']``.

##### Option 2

Permanently save the extensions to the config file. TVSS uses a config file that gets saved in your home directory during the installation. It is
called `.tvss`. The dot indicates that the file is hidden by default. Because, under normal circumstances, one does not need to change anything in it.

To save the extensions permanently to the config you need to use another parameter ``--permit-extensions ``. Note that this parameter only works in
conjunction with the `--extensions` parameter. Otherwise, you will get an error.