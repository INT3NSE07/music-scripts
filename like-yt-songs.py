import os
import sys
import subprocess
import traceback
import filetype
import glob
from pathlib import Path
from shutil import copy
from wand.image import Image
from mutagen.mp4 import MP4, MP4Cover
import ytmusicapi
from urllib.parse import urlparse
from urllib.parse import parse_qs

musicType = 'secular'
musicPath = os.path.join(r"D:\gdrive\media\Music", musicType)
outputExt = "m4a"

def main():
    try:
        ytmusicapi.setup(filepath="browser.json")
        ytmusic = ytmusicapi.YTMusic("browser.json")

        for filePath in glob.glob(os.path.join(musicPath, f'**\*.{outputExt}'), recursive=True):
            escapedPath = filePath.replace("'", "''")
            cmd = f"(ffprobe -v quiet -print_format json -show_format -show_streams -print_format json \'{escapedPath}\'| ConvertFrom-Json).format.tags.comment"
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            
            ytUrl = result.stdout
            parsed_url = urlparse(ytUrl)
            videoId = parse_qs(parsed_url.query)['v'][0]

            try:
                ytmusic.rate_song(videoId, rating = 'LIKE')
            except Exception as e:
                print(filePath, ytUrl)
                continue
    except Exception as e:
        print(e)
        traceback.print_stack()
        pass


if __name__ == "__main__":
    main()
