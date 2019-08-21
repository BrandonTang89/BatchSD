# BatchSD (Batch Song Downloader)
A "SuperLight" song downloader that downloads music from youtube in bulk.

**Due to YouTube reworking its website, this programme does not currently work, I'll fix it when I have the chance**

### Basic Usage
The list of songs can be inputted in 4 different ways
1. Spotify: Provide a spotify playlist URL (however only downloads the first 30 :( )
2. Youtube: Provide a youtube playlist URL
3. CSV: Provide a CSV file formatted as shown in the example "songs.csv"
4. Adhoc: While running the program, simply input how many songs you want to download and enter the names 1 at a time.

More detailed instructions are found in "readme.txt" which is shown at the bottom of the page

## Set-Up and Install
1. Download the "BatchSD_SETUP.zip" from the releases section of this repository
2. Extract the file
3. Run "-- Click to Setup --.cmd"
4. Double click on "BatchSD_Final.exe"

## About and Technical Details
This programme was jointly developed by Brandon Tang and Reiden Ong to enable the masses to more conveniently download songs from youtube. It relies on the pytube API and uses FFMPEG to convert the downloaded MP4 files into MP3 format.

### Installing Dependencies (if running the source "BatchSD_Final.py" file and/or building from source)
- Install python 3.7+ from "https://www.python.org/"
- Install python libraries using
<pre>pip install bs4 pytube ffmpy3 virtualenv pyinstaller</pre>
- Go into the ffmpeg folder, run "install ffmpeg.cmd"

### Building from Source
- Clone the repo
- Make whatever edits required
- Run build.cmd which activates a virtual environement (in mypython) and runs pyinstaller


## Detailed Instructions
<pre>
______       _       _       ___________ 
| ___ \     | |     | |     /  ___|  _  \
| |_/ / __ _| |_ ___| |__   \ `--.| | | |
| ___ \/ _` | __/ __| '_ \   `--. \ | | |
| |_/ / (_| | || (__| | | | /\__/ / |/ / 
\____/ \__,_|\__\___|_| |_| \____/|___/ BETA 1.10
 
Welcome to BatchSD!

BatchSD is an extremely light batch song downloader which can download many songs at once
It is compatible with existing platforms such as Youtube (playlists) as well as Spotify. 

Hope you find it useful!!!

Regards,
RD and BT

**************************************************************************************************
USAGE
The main program is in BatchSD.exe, so just click on it (it may take a while to load)

Functions:
Adhoc 
 - this allows you to download multiple songs by name, so feel free to just key in the name of your song!
 - Please note that the songs are downloaded from a music repository, which include music videos
	 - therefore if the song does not seem correct add a (audio) behind the name

Spotify 
 - In a spotify playlist, click the more options (...) then copy playlist url to obtain the playlist URL
 - Please note that there is currently a limit of 30 songs for the Spotify playlist import function! (could be solved in the future)
	 - if you want to download more than 30 songs pls use the .csv function 

.CSV
 - .csv is a file type which can be made using excel (comma delimited)
 - simply use our songs.csv template or make one of your own!

YouTube Playlist
 - Just copy and paste the youtube playlist URL and it will do its magic!

**************************************************************************************************
FAQs (or questions i imagine may be frequently asked)

What to do if the program crashes?
ANS: close the .exe file and reopen it. if it dosen't work, try harder.

Is there any concern with the large chunk of text that comes out after the Downloading complete sign comes?
ANS: Nope. The text comes from running a 3rd party program which converts videos from nasty .mp4 to nice .mp3s

Where do i find the songs?
ANS: Go to the folder labelled "mp3"

The songs are abit weird, or not the ones im looking for?
ANS: We source from a giant music repository, so you may want to narrow your search parameters.
	 - add the full name of the song
	 - add names of all artists
	 - add "audio" in the search to filter out those nasty music videos

Is there support for chinese songs?
ANS: yes. BatchSD should work for all languages. very cool.

What is up with the random "403" Errors?
ANS: Youtube doesn't really like people downloading videos from their site.
     Hence there is a cap on the number of videos one is able to download per unit time. 
     "403" error just means that youtube is blocking the downloads.
     However BatchSD tries to deal with this by skipping that video and remembering to come back to download it. 

     TLDR, don't worry, if you leave batchSD running long enough, all the songs will eventually be downloaded.

Is this Piracy?
ANS: nawwwwwhhhhhhhh thats uber lame and BatchSD is very cool so we dont do that here.


 __ __   ____  __ __    ___      _____  __ __  ____       __ 
|  |  | /    ||  |  |  /  _]    |     ||  |  ||    \     |  |
|  |  ||  o  ||  |  | /  [_     |   __||  |  ||  _  |    |  |
|  _  ||     ||  |  ||    _]    |  |_  |  |  ||  |  |    |__|
|  |  ||  _  ||  :  ||   [_     |   _] |  :  ||  |  |     __ 
|  |  ||  |  | \   / |     |    |  |   |     ||  |  |    |  |
|__|__||__|__|  \_/  |_____|    |__|    \__,_||__|__|    |__|
                                                             
</pre>
