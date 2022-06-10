import os
import sys
import subprocess
import traceback
import filetype
from glob import glob
from pathlib import Path
from shutil import copy
from wand.image import Image
from mutagen.mp4 import MP4, MP4Cover


musicDownloadPath = r"C:\Users\Jonathan\Downloads\Music"
musicArchivePath = r"D:\media\Music\music-archive.txt"
outputMusicPath = r"C:\Users\Jonathan\Music"
picardExePath = r"C:\Program Files\MusicBrainz Picard\picard.exe"
mp3tagExePath = r"C:\Program Files (x86)\Mp3tag\Mp3tag.exe"
albumArtDownloaderExePath = r"C:\Program Files\AlbumArtDownloader\AlbumArt.exe"

ytDlUrl = "https://music.youtube.com/browse/VLLM"
outputExt = "m4a"
thumbnailExt = "png"
croppedAlbumArtSuffix = f"-updated.{thumbnailExt}"
logFileName = "log.txt"
ignoredFiles = ["desktop.ini", "music-archive.txt", logFileName]

AAC_ARTIST = "©ART"
AAC_ALBUM = "©alb"
AAC_ALBUMART = "covr"


def main():
    try:
        # if [file for file in os.listdir(outputMusicPath) if not file in ignoredFiles] != []:
        #     sys.exit(f"Make sure {outputMusicPath} is empty")

        Path(musicDownloadPath).mkdir(exist_ok=True)
        logfile = open(os.path.join(musicDownloadPath, logFileName), 'w+')
        copy(musicArchivePath, musicDownloadPath)
        os.chdir(musicDownloadPath)

        # automatically crop to square thumbnail
        # mkdir _%(album)q cmd fails if album name contains quotes which is being delimited by \
        # slice the thumbnail filepath by len(thumbnailExt) + 1 to remove the file extension and the period
        ytDlCmd = f"yt-dlp --download-archive music-archive.txt --extract-audio --audio-format \"{outputExt}\" --embed-thumbnail --convert-thumbnails {thumbnailExt} --exec-before-download \"ffmpeg -i %(thumbnails.-1.filepath)q -q:v 1 -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\" %(thumbnails.-1.filepath.:-{len(thumbnailExt) + 1})q{croppedAlbumArtSuffix}\" --exec-before-download \"mv %(thumbnails.-1.filepath.:-{len(thumbnailExt) + 1})q{croppedAlbumArtSuffix} %(thumbnails.-1.filepath)q\" --cookies-from-browser chrome --add-metadata -o \"%(album)s/%(title)s.%(ext)s\" --parse-metadata \"%(release_date>%Y-%m-%d)s:%(meta_date)s\" \"{ytDlUrl}\""

        print(f"Executing {ytDlCmd}")
        subprocess.call(ytDlCmd, shell=True,
                        stdout=logfile, stderr=logfile)

        # Open picard to auto-tag recognized music
        # Make sure that each file has album and artist values
        # For untagged music, make sure to also save those files which will move all music from {musicDownloadPath} folder to {outputMusicPath}
        subprocess.call(picardExePath, shell=True,
                        stdout=logfile, stderr=logfile)

        if [file for file in os.listdir(musicDownloadPath) if not file in ignoredFiles] != []:
            sys.exit(
                f"All untagged files should be saved in picard so that they are moved to {outputMusicPath}")

        for filePath in glob(os.path.join(outputMusicPath, f'**\*.{outputExt}'), recursive=True):
            aacFile = MP4(filePath)
            albumPath = os.path.dirname(filePath)
            artist = aacFile.tags[AAC_ARTIST][0]
            album = aacFile.tags[AAC_ALBUM][0]
            albumArtPath = os.path.join(
                albumPath, f"{album}.{thumbnailExt}")

            # Check is needed for songs which belong to same album
            if not os.path.exists(albumArtPath):
                albumArtDownloaderArgs = f"-artist \"{artist}\" -album \"{album}\" -path \"{albumArtPath}\" -autoclose -sort size -minSize 1200 -maxSize 1500 -coverType front"
                albumArtDownloaderCmd = f"\"{albumArtDownloaderExePath}\" {albumArtDownloaderArgs}"
                subprocess.call(albumArtDownloaderCmd, shell=True,
                                stdout=logfile, stderr=logfile)

            # Could not find suitable album art, so manually download from itunes or other sources
            if not os.path.exists(albumArtPath):
                input(
                    f"Download album art manually from itunes or other sources and copy it to {os.path.join(albumPath, album)}. Press enter once done: ")

                files = [file for file in os.listdir(
                    albumPath) if file.startswith(album) and filetype.is_image(os.path.join(albumPath, file))]
                if len(files) == 0:
                    # extract album art
                    albumArt = aacFile.tags[AAC_ALBUMART][0]
                    with open(albumArtPath, 'wb') as img:
                        img.write(albumArt)
                else:
                    downloadedAlbumArt = os.path.join(albumPath, files[0])
                    if filetype.guess_extension(downloadedAlbumArt) != thumbnailExt:
                        Image(filename=downloadedAlbumArt).convert(
                            thumbnailExt).save(filename=albumArtPath)
                        os.remove(downloadedAlbumArt)

            with open(albumArtPath, 'rb') as f:
                albumart = MP4Cover(
                    f.read(), imageformat=MP4Cover.FORMAT_PNG)
            aacFile.tags[AAC_ALBUMART] = [bytes(albumart)]
            aacFile.save()

        subprocess.call(mp3tagExePath, shell=True,
                        stdout=logfile, stderr=logfile)

        print(f"Manually copy back music-archive to {musicArchivePath}")
    except Exception as e:
        print(e)
        traceback.print_stack()
        pass


if __name__ == "__main__":
    main()
