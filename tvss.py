import glob
import os
import re
import shutil

import yaml


class TvShowSorter:
    
    def __inti__(self):
        self.conf = self.read_config_file()
        self.regex_season_episode = r"(s(\d{2})e\d{2})"
        self.show_title = self.make_show_title_regex("Boston Legal")
        
        os.chdir(self.conf.f_dir)
    
    @staticmethod
    def read_config_file() -> dict:
        with open(".tvss.yml") as f:
            return yaml.load(f)
    
    def make_show_title_regex(title: str) -> str:
        s_title = title.split()
        divider = ".*"
        title = r".*" + divider.join(s_title) + ".*"
        
        return title
    
    def make_destination_path(self) -> None:
        if not os.path.exists(self.conf.destination_path):
            os.mkdir(self.conf.desstination_path)
    
    def walk_show_files(self) -> None:
        for f in glob.glob(".", recursive = True):
            if not re.search(self.show_title, f, re.IGNORECASE):
                continue
            
            for dir_path, dir_names, file_names in os.walk(f):
                for filename in file_names:
                    f_name, f_ext = os.path.splitext(filename)
                    
                    for i in self.conf.file_ext:
                        if f_ext == i and f_name.find('sample') == -1:
                            print(f_name)
                            
                            season_episode = re.search(self.regex_season_episode, f_name, re.IGNORECASE)
                            print(season_episode)
                            
                            season_path = os.path.join(
                                    self.conf.destination_path, "Staffel " + season_episode.group(2)[1:])
                            
                            if not os.path.exists(season_path):
                                os.mkdir(season_path)
                            
                            from_dir = os.path.join(self.conf.origin_path, dir_path, f_name + f_ext)
                            to_dir = os.path.join(
                                    self.conf.destination_path, season_path,
                                    self.show_name + " " + season_episode.group(1) + f_ext)
                            
                            if not os.path.isfile(to_dir):
                                dest = shutil.copy2(from_dir, to_dir)


if __name__ == "__main__":
    tvss = TvShowSorter()
