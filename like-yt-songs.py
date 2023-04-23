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
        ytmusicapi.setup(filepath="browser.json", headers_raw="""accept: */*
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
authorization: SAPISIDHASH 1682248632_fb7c28e1200dacb6c15c8af32f834e0fb584e49d
content-length: 2200
content-type: application/json
cookie: YSC=aWo6txslo6k; VISITOR_INFO1_LIVE=OshexTTdBpM; PREF=f6=40000000&tz=America.New_York; SID=VwgmdtTvGYozkjQOOHRC-N64rKWDmVa1CcLkzde06STwPqQv5evdJ1x7Xnf2H3wrcAL4JA.; __Secure-1PSID=VwgmdtTvGYozkjQOOHRC-N64rKWDmVa1CcLkzde06STwPqQv0SjwAFWW-9qFwdFylTkqNA.; __Secure-3PSID=VwgmdtTvGYozkjQOOHRC-N64rKWDmVa1CcLkzde06STwPqQvFBGfx7sg95GDbVE8DK57ug.; HSID=AcK8WZcCoiVK8vjGB; SSID=AaNb9bJd9hmtfcDvL; APISID=WIUvnBySk8_rWzLc/AbSsMn9rk3wOotDQJ; SAPISID=FQ1xSrgUqRq67xF5/AQLAaS3JsjNpqoL9y; __Secure-1PAPISID=FQ1xSrgUqRq67xF5/AQLAaS3JsjNpqoL9y; __Secure-3PAPISID=FQ1xSrgUqRq67xF5/AQLAaS3JsjNpqoL9y; LOGIN_INFO=AFmmF2swRQIgHWe9jlrfCWiV5BwLvKcAogDvu3DtKa9pFy9dYoiPnqQCIQCAA7C3s3awh93yi1L77SbN9RMSsOWL2Qa6N66p5JGDqA:QUQ3MjNmeFEtZDJRd0txZDFIOUpUS2JCRWxoWFJhSTV1WmJiRGlFdlVyTm4zMlVxSTlOSzlmdFk3SWhreDNSdmY3VXNkR3lxb0VZQVNzR3R5LVhLdXhqYTFLU0V0S0YxWnRkOVBTTVlLRERLbG8xcHBfQWpybjlLWjV4RXhickkwTmFVWE1FUkdLRm04djBWYnF2TW82X2JzMHYyaTZGYTNn; SIDCC=AP8dLtwe47yw9o-WAYFCpVW6EpRamWluYIXE59DwTuhzJ4STqIrGxT9Ls93oTScw8aJLKzX5; __Secure-1PSIDCC=AP8dLtz8qHEWFMrl-1vq3dkg6ohD1_YciyhccrzcxUFhW6cch3Rye6oBsxq4WWOZE5ZiVtPiww; __Secure-3PSIDCC=AP8dLtxwf0hDQeAYT5L4vD0qo1IqYDcKV2Ys2dORoHy7uzt3mEKP7U9_wNPNxjqKpa4QaAsaVA
dnt: 1
origin: https://music.youtube.com
referer: https://music.youtube.com/
sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"
sec-ch-ua-arch: "x86"
sec-ch-ua-bitness: "64"
sec-ch-ua-full-version: "112.0.5615.138"
sec-ch-ua-full-version-list: "Chromium";v="112.0.5615.138", "Google Chrome";v="112.0.5615.138", "Not:A-Brand";v="99.0.0.0"
sec-ch-ua-mobile: ?0
sec-ch-ua-model: ""
sec-ch-ua-platform: "Windows"
sec-ch-ua-platform-version: "15.0.0"
sec-ch-ua-wow64: ?0
sec-fetch-dest: empty
sec-fetch-mode: same-origin
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
x-goog-authuser: 0
x-goog-visitor-id: CgtPc2hleFRUZEJwTSigp5SiBg%3D%3D
x-origin: https://music.youtube.com
x-youtube-bootstrap-logged-in: true
x-youtube-client-name: 67
x-youtube-client-version: 1.20230417.01.00
        """)
        ytmusic = ytmusicapi.YTMusic("browser.json")

        for filePath in glob.glob(os.path.join(musicPath, f'**\*.{outputExt}'), recursive=True):
            escapedPath = filePath.replace("'", "''")
            cmd = f"(ffprobe -v quiet -print_format json -show_format -show_streams -print_format json \'{escapedPath}\'| ConvertFrom-Json).format.tags.comment"
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            
            ytUrl = result.stdout
            parsed_url = urlparse(ytUrl)
            videoId = parse_qs(parsed_url.query)['v'][0]

            if videoId == "ltcHzgUc944":
                start = True

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
