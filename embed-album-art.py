import os
from glob import glob
import subprocess
import traceback
from typing import cast
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4, MP4Cover

musicPath = r"C:\Users\Jonathan\Downloads\Music-m4a"
inputExt = "m4a"
albumArtExt = "png"

def main():
  for filePath in glob(os.path.join(musicPath, f'**\*.{inputExt}'), recursive=True):
    try:
      albumPath = os.path.dirname(filePath)
      albumName = os.path.basename(albumPath)
      coverArtPath = os.path.join(albumPath, f'{albumName}.{albumArtExt}')

      aacFile = MP4(filePath)
      with open(coverArtPath, 'rb') as f:
        albumart = MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)
      aacFile.tags['covr'] = [bytes(albumart)]
      aacFile.save()
    except:
      traceback.print_stack()
      pass


if __name__ == "__main__":
    main()