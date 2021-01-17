# Tv-Show Sorter (TVSS)

This tool is capable to sort any kind of tv shows. During the process, all video files will be renamed, sorted into folders named after the season
they're belonging to and saved wherever you desire. By that it is possible to upload the files to your media server like Plex or Emby. These media
centers need the correct naming convention in order to find all the metadata like posters, background images and other information.

The seasons need to be in a folder called after the season. F.e.: "Season 01". Also, the videos itself need to follow these kind opf conventions.
Files need to be named like this: "My New Show (2011) s01e01.mkv". This very tool does all that for you.

### Installation

To install TVSS just copy the following line to your Terminal or command line:
`pip3 install git+https://github.com/michaelgrossklos/tvshowsorter.git`

I assume you have Python >= 3.7 already installed on your machine. If not, go to https://www.python.org/ and follow the instructions there.

### Using the tool

First of all, it is important to know, that you always can use the `--help` option. This will print someting like this:

```
Usage: tvss [OPTIONS] COMMAND [ARGS]...

  Sorting your ripped or downloaded tv-shows into folders named after the
  seasons they're belonging to (f.e.: Season 01). Renames all files like
  "Name Of Show s01e01.ext" for direct use in your media center like Plex or
  Emby. So it can find all meta data needed.

Options:
  -o, --origin-path PATH       The path to the source files to sort
  -d, --destination-path PATH  The path where to save the sorted files
  -l, --language TEXT          Sets the language for season names
  --debug / --no-debug         Turn debug mode on
  --delete-folders BOOLEAN     Delete the source folder after copying the file
  --help                       Show this message and exit.

Commands:
  addextensions  Extends the list of file extensions.
  settings       Shows the actual settings
  titles         The titles of the shows to be sorted.
```

As you can see in the first line, you first (and always) need to call the program itself by using `tvss`. After that you can specify options which
usually begins with `--` (two dashes). Or (in some cases) also with just one `-`. This is just the short hand version of it. The effect will be
exactly the same.

For example `-l` is the same as `--language`.

All options are, well... optional ;)

Some of them requiring arguments to be passed in, some do not.
`--delete-folders` for example is one that does not need any arguments. Whereas `--origin-path` in fact needs the path where all the video files are
located.

On the other hand, there are commands. Those need to be typed after the options (if you've specified one). Some of them are requiring arguments. Some
do not. For Example `settings` does not need any argument. If you set one, you would get an error.

A complete line for using TVSS could look something like that:

`tvss -l=en --delete-folders titles "my first show" "my second show"` or

`tvss titles "my fisrt show" "my second show"` if you wouldn't use any options.

**IMPORTANT** to know is, that you can't use two commands at the same time, whereas you are able to use more than one option at ones. The order in
which you specify the options does not matter.

### Renaming files

The files to be renamed are only the video files that get stored into the destination folder.

#### File name a.k.a show titles (required)

In order to rename - and more importantly - find the right files, you need to provide the titles of the show.

You do that by typing `tvss titles "My tv show 1" "My tv show 2"`. Capitalization will be ignored. Notice, that you are able to specify just one, or
an unlimited amount of titles. You just need to wrap each title into quotation marks followed by a space. The order in which you define the titles is
irrelevant.

This also means, that you can have multiple tv shows including multiple seasons in your source folder. As long as each episode is contained in its own
folder and this folder is somehow named after the show. For example: `my.tv.show.1` or `345-my.tv.show_2` or `dim-mytvshow.3-IFRIM`. The characters in
between the words of the title itself, and surrounding it are not relevant at all. TVSS will find the title anyways.

How the video file itself is named, does not matter, as long as it holds the season and episode count. For example `my.first.show.s01e20`. In
which `s01e20` means season 1, episode 20. Without that, TVSS is incapable of sorting the episodes and will stop running with printing out an error
message.

### File extensions

Not always, but most of the time, are the provided default file extensions sufficient. If that is not the case you can extend the list of file
extensions by using the commmand ``tvss addextensions ".mpeg" ".webm"``.

Like the command title, you can specify just one or an unlimited amount of extensions. You just need to wrap each extension into quotation marks
followed by a space. The order in which you define those, is irrelevant.

The extension you're adding, will get saved permanently. So, you don't need to set them the next time you use TVSS.

If you want to know what extensions are already provided, just use the command `tvss settings` without any arguments, and an overview of all settings
gets printed on the screen.

### Show all settings

As you are able to change most of the settings, you need to know the actual state they're in. Just type `tvss settings` without any arguments, and
something like the following will get printed on the screen:

```bazaar
ACTUAL SETTINGS FOR TVSS:
Regex for seasons: (s([0-9]{2})e[0-9]{2})
Origin/Source path: /Users/<user>/Downloads/extracted
Destination path: /Users/<user>/Downloads/extracted/SORTED
File extensions available: ['.mkv', '.avi', '.mp4', '.mov']
Languages available: ['de', 'en', 'es', 'fr', 'it', 'ru']
Language set: en
Season is called: Season

You can find more information on:
https://github.com/michaelgrossklos/tvshowsorter
```

### Setting the paths

There are two paths to be set.

#### Origin/Source path

This is the path where the ripped or downloaded files are to find at. In the settings you'll see the whole path. Which by default is set
to `<your home directory>/>Downloads/extracted`. In which `<your home directory>` is substituted with you actual path depending on your operating
system.

Followed by that is the relative path to your source folder, where all the files are in. You can set this path to any location under your home
dierectory, as long as one won't need administrator rights to read from it. Most of the time, it will be your downloads folder or any subfolders under
it. You just need to provide the parent folder, where all other folders, that containing the video files are contained in.

In the example above, your folder structure would look something like this:

```
+-+ Users 
| |
| +--+ Downloads
| |  |
| |  +--+ extracted
| |  |  |
| |  |  +--+ my.first.show.episode
| |  |  |  +--+ my.first.show.video.file.s01e01.mkv
| |  |  +-- my.second.show.episode
| |  |  |  +--+ my.second.show.video.file.s01e02.mkv
| |  |  +-- my.third.show.episode
| |  |  |  +--+ my.third.show.video.file.s01e03.mkv
| |  |  +-- a-different-show_dfjgr
| |  |  |  +--+ a-different-show.video.file.s05e01.mkv
| |  |  +-- a-different-show_dfjgr
| |  |  |  +--+ a-different-show.video.file.s05e02.mkv
| |  |  +-- ...
```

In which `extracted` is the parent folder of all the video files.

#### Destination path

All the video files will be copied to this path.

This path by default is set to `<your home directory>/Downloads/extracted/SORTED`. It's the same principal as of the origin path.

As mentioned above, the files will be sorted into folders named after the seasons. This could look something like this:

```
+-+ Users 
| |
| +--+ Downloads
| |  |
| |  +--+ extracted
| |  |  |
| |  |  +--+ A Tv Show
| |  |  |  |
| |  |  |  +--+ Season 01
| |  |  |  |  +--+ A Tv Show s01e01.mkv
| |  |  |  |  +--+ A Tv Show s01e02.mkv
| |  |  |  |  +--+ A Tv Show s01e03.mkv
| |  |  |  |  +--+ ...
| |  |  |  +--+ Season 02
| |  |  |  |  +--+ A Tv Show s02e01.mkv
| |  |  |  |  +--+ A Tv Show s02e02.mkv
| |  |  |  |  +--+ A Tv Show s02e03.mkv
| |  |  |  |  +--+ ...
```

#### Changing the paths

To change the origin path you can use a dedicated option ` --origin-path="/Downlaods/subfolder/any_other_folder"`. The path needs to be relative to
you home folder. Notice, that the path will not be permanently changed. Just for that one time. To change it permanently, you need to change the
config file itself. You can read about that a bit further down below.

For the destination path you use `--destination-path` in the same manor as with the origin path.

