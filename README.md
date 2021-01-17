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
which `s01e20` means season 1, episode 20.

#### File extensions

Not always, but most of the time, are the provided default file extensions sufficient. If that is not the case you can extend the list of file
extensions by using the commmand ``tvss addextensions ".mpeg" ".webm"``.

Like the command title, you can specify just one or an unlimited amount of extensions. You just need to wrap each extension into quotation marks
followed by a space. The order in which you define those, is irrelevant.

The extension you're adding, will get saved permanently. So, you don't need to set them the next time you use TVSS.

If you want to know what extensions are already provided, just use the command `tvss settings` without any arguments, and an overview of all settings
gets printed on the screen.