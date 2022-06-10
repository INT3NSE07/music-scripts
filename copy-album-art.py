import os
from glob import glob
import subprocess
import traceback
from typing import cast
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4
from shutil import copy2

musicPath = r"C:\Users\Jonathan\Downloads\Music-m4a"
albumArtPath = r"C:\Users\Jonathan\Downloads\album-art-png"
inputExt = "m4a"
albumArtExt = "png"

def main():
  for filePath in glob(os.path.join(musicPath, f'**\*.{inputExt}'), recursive=True):
    try:
      albumPath = os.path.dirname(filePath)
      albumName = os.path.basename(albumPath)
      coverArtPath = os.path.join(albumArtPath, f'{albumName}.{albumArtExt}')

      copy2(coverArtPath, albumPath)
    except:
      traceback.print_stack()
      pass


if __name__ == "__main__":
    main()