Initial setup
C:\Python310\python.exe -m venv venv
.\venv\Scripts\Activate.ps1
.\venv\Scripts\python.exe -m pip install --upgrade pip
pip install filetype wand mutagen

Run
.\venv\Scripts\Activate.ps1

# Disable cookies db lock
taskkill /f /im msedge.exe
cd "C:\Program Files (x86)\Microsoft\Edge\Application\"
.\msedge.exe  --disable-features=LockProfileCookieDatabase

Other commands
Get-ChildItem "D:\gdrive\media\Music\secular\" -Recurse -File |
Foreach-Object {
  $fileName = $_.FullName
  $purl = (ffprobe -v quiet -print_format json -show_format -show_streams -print_format json $_.FullName | ConvertFrom-Json).format.tags.comment
  Write-Output $purl
}