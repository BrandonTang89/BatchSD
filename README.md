# BatchSD (Batch Song Downloader)
A "SuperLight" song downloader that downloads music from youtube in bulk.

### Basic Usage
The list of songs can be inputted in 4 different ways
1. Spotify: Provide a spotify playlist URL (however only downloads the first 30 :( )
2. Youtube: Provide a youtube playlist URL
3. CSV: Provide a CSV file formatted as shown in the example "songs.csv"
4. Adhoc: While running the program, simply input how many songs you want to download and enter the names 1 at a time.

## Set-Up and Install
1. Download the "BatchSD_SETUP.zip" from the releases section of this repository
2. Extract the file
3. Run "-- Click to Setup --.cmd"
4. Double click on "BatchSD_Final.exe"

## About
This programme was jointly developed by Brandon Tang and Reiden Ong to enable the masses to more conveniently download songs from youtube. It relies on the pytube API and uses FFMPEG to convert the downloaded MP4 files into MP3 format.

Installing Dependencies (if running the source "BatchSD_Final.py" file and or building from source)
- Install python 3.7+ from "https://www.python.org/"
- Install python libraries using
<pre>pip install bs4 pytube ffmpy3 virtualenv pyinstaller</pre>

Building from Source
- Clone the repo
- Make whatever edits required
- Run build.cmd which activates a virtual environement (in mypython) and runs pyinstaller
