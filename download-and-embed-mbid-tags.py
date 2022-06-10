import os
from glob import glob
import subprocess
import traceback
from typing import cast
from mutagen.oggopus import OggOpus
from mutagen.mp4 import MP4

musicPath = r"C:\Users\Jonathan\Downloads\Music"
inputExt = "opus"
outputExt = "m4a"
opusAcoustId = "ACOUSTID_ID"
opusArtistId = "MUSICBRAINZ_ARTISTID"
opusAlbumId = "MUSICBRAINZ_ALBUMID"
opusTrackId = "MUSICBRAINZ_TRACKID"

def main():
  for filePath in glob(os.path.join(musicPath, f'**\*.{inputExt}'), recursive=True):
    try:
      albumPath = os.path.dirname(filePath)
      song = os.path.basename(filePath)
      songName, songExt = os.path.splitext(song)
      oggOpusFile = OggOpus(filePath)
      opusTags = oggOpusFile.tags
      ytUrl = opusTags["PURL"][0]
      ytUrl = ytUrl.replace("https://www.", "https://music.", 1)
      cmd = f"yt-dlp --extract-audio --audio-format {outputExt} --cookies-from-browser chrome --add-metadata -P \"{albumPath}\" -o \"{songName}.%(ext)s\" --parse-metadata \"%(release_date>%Y-%m-%d)s:%(meta_date)s\" --force-overwrites {ytUrl}"
      #print(f"Executing {cmd}")
      if subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        outputSongName = f"{songName}.{outputExt}"
        outputSongPath = os.path.join(albumPath, outputSongName)
        aacFile = MP4(outputSongPath)
        tagsCount = len(aacFile.tags)

        if opusAcoustId in opusTags:
          aacFile.tags["----:com.apple.iTunes:Acoustid Id"] = bytes(opusTags[opusAcoustId][0], 'UTF-8')
        else:
          print(f"{filePath} does not have {opusAcoustId}")

        if opusArtistId in opusTags:
          aacFile.tags["----:com.apple.iTunes:MusicBrainz Artist Id"] = bytes(opusTags[opusArtistId][0], 'UTF-8')
        else:
          print(f"{filePath} does not have {opusArtistId}")

        if opusAlbumId in opusTags:
          aacFile.tags["----:com.apple.iTunes:MusicBrainz Album Id"] = bytes(opusTags[opusAlbumId][0], 'UTF-8')
        else:
          print(f"{filePath} does not have {opusAlbumId}")

        if opusTrackId in opusTags:
          aacFile.tags["----:com.apple.iTunes:MusicBrainz Track Id"] = bytes(opusTags[opusTrackId][0], 'UTF-8')
        else:
          print(f"{filePath} does not have {opusTrackId}")

        # new tags were added
        if len(aacFile.tags) > tagsCount:
          aacFile.save()
      else:
        print(f"Error downloading file {filePath}")
    except:
      print(f"Error downloading file {filePath}")
      traceback.print_stack()
      pass


if __name__ == "__main__":
    main()