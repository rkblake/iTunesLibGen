import os
import sys

songs = []

if __name__ == "__main__":
    music_root_dir = raw_input("Specify directory to update from: ")
    for path in os.walk(music_root_dir):
        for filename in path[2]:
            songs.append(path[0]+'/'+filename)
    print songs
