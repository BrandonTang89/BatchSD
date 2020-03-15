############################################################################################################################################
# BATCHSD CODE
#
#   Structure of code
#       - Imports and variable instantiation
#       - Universal Youtube Download Functions
#       - High level functions to handle different input
#       - Post processing and other offline helpder functions
#       - CLI and front-end functions
#
#############################################################################################################################################

import os
import sys
import shutil
import csv
import time
import urllib.request
import ffmpy3
import progressbar
from multiprocessing import Pool
from bs4 import BeautifulSoup
from pytube import YouTube, Playlist
vid_dir = "songs"
audio_dir = "mp3"
audio_only = False
customname = True
num_processes = 4
failed_downloads = []

print(r" ____        _       _     ____  ____ ")
print(r"| __ )  __ _| |_ ___| |__ / ___||  _ \ ")
print(r"|  _ \ / _` | __/ __| '_ \\\___ \| | | |")
print(r"| |_) | (_| | || (__| | | |___) | |_| |")
print(r"|____/ \__,_|\__\___|_| |_|____/|____/  BETA")
print(r"a *superlight* batch song downloader")
print(r"by BT and RD")
print(r"")

#############################################################################################################################################
# UNIVERSAL DOWNLOAD FUNCTIONS
#
#   multiprocessing_download(name_list) -- >
#       yt_download("Song Name") -->
#           yt_query("Song Name") [Returns URL]
#           yt_ url_download("URL") [Downloads the video at "URL"] -->
#               download_fails_fn() [Downloads Failed Videos (deprecated)]
#        convert_vid_to_audio
#
#############################################################################################################################################
# --- Takes a list of URLs and Downloads them ---
# --- Input: List of Song Names or URLS, url_type indicates if the namelist is of names or urls ---
def multiprocessing_download(name_list, url_type=False):
    with Pool(processes=num_processes) as pool:
        start = 0
        end = min(num_processes, len(name_list))
        while True:
            print(str(start) + " / " + str(len(name_list)) + " downloaded ")
            if not url_type:
                pool.map(yt_download, name_list[start:end])
            else:
                pool.map(yt_url_download, name_list[start:end])
            if end == len(name_list):
                break
            end = min(end + num_processes, len(name_list))
            start += num_processes

    convert_vid_to_audio()

# --- Download each video (with first result) ---
def yt_download(name):

    # Check if video already downloaded
    if os.path.isfile(vid_dir+"/"+name+".mp4"):
        print(name, "has already been downloaded, skipping")
        return 0

    url = ""
    print("Downloading", name, "...")
    for i in range(3):
        try:
            url = yt_query(name)[0]
            break
        except:
            print("No YT Queries Found")
            if i < 2:
                print("Trying again")
            else:
                print("Sorry, can't seem to download this...")
            pass

    if url != "":
        yt_url_download(url, name=name)

# Returns URL of Song
def yt_query(name):
    query = urllib.parse.quote(name)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    urls = []
    #print("possible links:")
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        urls.append('https://www.youtube.com' + vid['href'])
        #print('     https://www.youtube.com' + vid['href'])
    return urls


# Helper Function for Progress Bar
def progress_Check(stream=None, chunk=None, remaining=None):
    # Gets the percentage of the file that has been downloaded.
    percent = (100*(file_size-remaining))/file_size
    bar.update(percent)
    # print("{:00.0f}% downloaded".format(percent))

# --- Function to Download a Video URL ---
def yt_url_download(url, name=""):
    # Global Variables to Modify
    global failed_downloads
    global file_size  # For Progress Bar
    global bar       # For Progress Bar

    print("URL: ", url)
    yt = YouTube(url, on_progress_callback=progress_Check)

    # Choosing Stream
    if (audio_only):
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.filter(progressive=True).first()

    # Get setting up file size variable for progress bar
    file_size = stream.filesize

    # Check Custom Name Setting
    if not customname:
        name = ""

    # Downloading File
    with progressbar.ProgressBar(max_value=100) as bar:
        try:
            if name != "":
                # save file as filename to specified dir
                stream.download(vid_dir, filename=name)
            else:
                stream.download(vid_dir)
        except Exception as e:
            print("Error Downloading File")
            print("Error: " + str(e))
            pass

# --- Function to Download Failed Videos --- [Deprecated]
def download_fails_fn():
    global failed_downloads
    if failed_downloads == []:
        return
    print("Trying to Download Failed Files")
    for index, (url, name) in enumerate(failed_downloads):
        print(index+1, "/", len(failed_downloads))
        yt_url_download(url, name)
    convert_vid_to_audio()


#############################################################################################################################################
# HIGH LEVEL FUNCTIONS FOR DIFFERENT INPUT TYPES [These functions call the universal youtube download functions above]
#
#   spotify_download(playlist_url) [downloads songs from spotify playlist]
#       --> spotify_import(url) [uses bs4 to get Song Names]
#   adhoc_download(names) [handles adhoc input]
#   csv_download(csv_filename) [handles CSV input]
#   youtube_playlist_download(playlist_url) [handles youtube playlist download]
#
#############################################################################################################################################
def spotify_download(playlist_url):
    playlist = spotify_import(playlist_url)

    # print(playlist)
    cont = input("Continue? (y/n):  ")
    if (cont == "y"):
        multiprocessing_download(playlist)
    else:
        print("Aborted")
        return


def spotify_import(url):
    #url = "https://open.spotify.com/user/11167406418/playlist/4sqiTOJuBd17olFPKosgTq?si=B59i-8wEQaC-HYVQF09X3Q"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    # name array
    tracks = soup.findAll("span", {"class": "track-name"})
    #print("tracks: ")
    for i in range(len(tracks)):
        tracks[i] = str(tracks[i])
        tracks[i] = tracks[i][36:-7]
        # print(tracks[i])

    # returns list of links
    artists = soup.findAll('span', {"class": "artists-albums"})

    for i in range(len(artists)):
        artists[i] = str(artists[i])
        #artists[i] = artists[i][127:-155]
        artists[i] = artists[i].split("•")[0]
        artists[i] = artists[i].split("</span></a>")
        for j in range(len(artists[i])):  # for multiple artists
            artists[i][j] = artists[i][j].split(">")[-1]

        temp = ""
        for j in range(len(artists[i])-1):  # adding all to one string
            temp += str(artists[i][j])
            if(j < len(artists[i])-2):
                temp += ", "
        artists[i] = temp

    print("tracks and artists | Total Songs: " + str(len(tracks)))
    output = []
    for i in range(len(tracks)):
        output.append(tracks[i]+" - "+artists[i])
        print(tracks[i]+" - "+artists[i])
    return output


def adhoc_download(names):
    print("Downloading", len(names), "files")
    multiprocessing_download(names)


def csv_download(csv_filename):
    songs = []  # songs[i] = title + artist
    try:
        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                songs.append((row[0] + " " + row[1]))
    except Exception as e:
        print(e)
        print("Error Occured Reading CSV, please ensure that the file exist and is formatted properly")
        return

    for index, song in enumerate(songs):
        print(index, ": " + song)

    cont = input("Continue? (y/n):  ")
    if (cont != "y"):
        print("Aborted")
        return
    try:
        multiprocessing_download(songs)
    except:
        pass


def youtube_playlist_download(playlist_url):
    print("---Youtube Playlist Download---")
    playlist = Playlist(playlist_url)
    playlist.populate_video_urls()
    print("Number of Videos in Playlist: ", len(playlist.video_urls))
    print(playlist.video_urls)
    cont = input("Continue? (y/n):  ")
    if (cont == "y"):
        try:
            multiprocessing_download(playlist.video_urls, True)
        except Exception as e:
            print(e)
            pass
    else:
        print("Aborted")
        return

#############################################################################################################################################
# POST PROCESSING AND OFFLINE FUNCTIONS
#
#   convert_vid_to_audio(vid_dir, audio_dir) [Uses FFMPEG to Convert Songs in "vid_dir" to mp3 files in "audio_dir"]
#   clear_temp_vid_files(vid_dir) [Deletes files in "vid_dir"]
#   close() [Function called to invoke shutdown of programme]
#
#############################################################################################################################################


def convert_file(song):
    initial_file = vid_dir+"/"+song
    final_file = audio_dir+"/"+song[:-4]+".mp3"
    if (os.path.isfile(final_file)):  # avoid converting repeated files
        print("Already Converted " + song + ", skipping")
        return

    print("Converting: " + song)
    ff = ffmpy3.FFmpeg(
        inputs={initial_file: ["-y"]},
        outputs={final_file: None}
    )
    # print(ff.cmd)
    ff.run()

# Post Processing (Convert to MP3)
def convert_vid_to_audio():
    print("Downloads (Hopefully) Complete; Converting MP4 to MP3...")
    try:
        os.mkdir(audio_dir)  # create audio_dir if it doesnt already exist
    except:
        pass

    name_list = os.listdir(vid_dir)
    with Pool(processes=num_processes) as pool:
        start = 0
        end = min(num_processes, len(name_list))
        while True:
            print(str(start) + " / " + str(len(name_list)) + " converted ")
            pool.map(convert_file, name_list[start:end])

            if end == len(name_list):
                break
            end = min(end + num_processes, len(name_list))
            start += num_processes


def clear_temp_vid_files(vid_dir):
    shutil.rmtree(vid_dir)


def close():
    print("")
    print("************************************************************")
    if os.listdir(vid_dir) == []:  # if user hasnt downloaded anything, dont quit
        main()
    print("All pending operations complete, songs stored in mp3 folder.")
    exiting = input("Would you like to exit this program? (y/n?): ")
    if(exiting == "n" or exiting == ""):
        print("")
        main()
    else:
        clear_temp_vid_files(vid_dir)
        sys.exit()  # to prevent multiple queries

#############################################################################################################################################
# CLI AND FRONT-END FUNCTIONS
#
#   presets() [sets predefined global variables]
#   settings() [Called upon need to edit settings from CLI]
#   main() [Function called to invoke programme]
#
#############################################################################################################################################


def presets():
    global vid_dir
    global audio_dir
    global audio_only
    global customname
    vid_dir = "songs"
    audio_dir = "mp3"
    audio_only = False
    customname = True

    # Check if vid_dir exist
    try:
        os.mkdir(vid_dir)  # create vid_dir if it doesnt already exist
    except:
        pass


presets()


def settings():
    global vid_dir
    global audio_dir
    global audio_only
    global customname
    vid_dir = input("Directory for Video Files: (default:songs)")
    if vid_dir == "":
        vid_dir = "songs"
    audio_dir = input("Directory for Audio (MP3) files? (default:mp3)")
    if audio_dir == "":
        audio_dir = "mp3"

    audio_only_string = input(
        "Download Only Using Audio Stream? (y/n?) (slower but less space required, default:False)")
    if audio_only_string == "y" or audio_only_string == "true":
        audio_only = True
        print("Audio Stream Only: True")
    else:
        audio_only = False
        print("Audio Stream Only: False")

    customname_string = input(
        "Custom Names for Song (from spotify playlist/csv file/ adhoc; if false, name of YouTube Video is used as song name) ? (y/n?), default:True)")
    if customname_string == "n" or customname_string == "false":
        customname = False
        print("Custom Names: False")
    else:
        customname = True
        print("Custom Names: True")

    # Check if vid_dir exist
    try:
        os.mkdir(vid_dir)  # create vid_dir if it doesnt already exist
    except:
        pass


def main():
    print("Options")
    print("|  a ----- Ad-Hoc (Default)")
    print("|  x ----- CSV (.csv, editable from MS Excel)")
    print("|  s ----- Spotify playlist URL (max. 30)")
    print("|  y ----- Youtube Playlist URL")
    print("|  ")
    print("|  p ----- Preferences Menu")
    print("|  h ----- Help")
    print("|  e ----- Exit")
    operation = input("Option of choice: ")
    print("")

    if operation == "s":
        # Gather Input
        print("---Spotify Download---")
        playlist_url = input("Playlist URL: ")
        print("")

        spotify_download(playlist_url)

    elif operation == "x":
        # Gather Input
        print("---CSV Download---")

        csv_filename = input("CVS File Path: (default:songs.csv)")
        print("")
        if csv_filename == "":
            csv_filename = "songs.csv"

        csv_download(csv_filename)

    elif operation == "y":
        # https://www.youtube.com/watch?v=q3tG-1yONdU&list=PLs6QjtyrwVUZLgfAkvF8DdnNC7cYFHdTq
        playlist_url = input("Playlist URL: ")
        print("")
        youtube_playlist_download(playlist_url)

    elif operation == "p":
        settings()

    elif operation == "h":
        print("just saying but readme.txt exists for a reason ")
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
        readmeee = open('README.txt')
        print(readmeee.read())
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")

    elif operation == "e":
        print("Bye bye :)")
        sys.exit()

    else:
        # Gather Input
        print("---Adhoc Download---")
        n = input(
            "How many songs/videos do you want? [just press enter to return to main menu]: ")
        try:
            n = int(n)
        except:
            print("Please enter a valid natural number")
            n = 0
        names = []

        for i in range(n):
            name = input("Enter Song " + str(i) + ":")
            if name != "":
                names.append(name)
            else:
                print("No Song Specified... (skipping)")

        adhoc_download(names)

    close()


# Autorun Main Function
if __name__ == '__main__':
    main()
