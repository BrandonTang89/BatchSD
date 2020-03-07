import requests
import urllib.request
import time
import csv, os, ffmpy3, shutil, sys, progressbar
from bs4 import BeautifulSoup
from pytube import YouTube, Playlist
vid_dir = "songs"
audio_dir = "mp3"
audio_only = False
download_fails = True
customname = True

print(" ____        _       _     ____  ____ ")
print("| __ )  __ _| |_ ___| |__ / ___||  _ \ ")
print("|  _ \ / _` | __/ __| '_ \\\___ \| | | |")
print("| |_) | (_| | || (__| | | |___) | |_| |")
print("|____/ \__,_|\__\___|_| |_|____/|____/  BETA")
print("a *superlight* batch song downloader")
print("by BT and RD")
print("")

############################################################################################################################################
def spotify_import(url):
    #url = "https://open.spotify.com/user/11167406418/playlist/4sqiTOJuBd17olFPKosgTq?si=B59i-8wEQaC-HYVQF09X3Q"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    #name array
    tracks = soup.findAll("span", { "class" : "track-name" })
    #print("tracks: ")
    for i in range(len(tracks)):
        tracks[i] = str(tracks[i])
        tracks[i] = tracks[i][36:-7]
        #print(tracks[i])


    artists = soup.findAll('span', { "class" : "artists-albums" }) #returns list of links

    for i in range(len(artists)):
        artists[i] = str(artists[i])
        #artists[i] = artists[i][127:-155]
        artists[i] = artists[i].split("•")[0]
        artists[i] = artists[i].split("</span></a>")
        for j in range(len(artists[i])): #for multiple artists
            artists[i][j] = artists[i][j].split(">")[-1]

        temp = ""
        for j in range(len(artists[i])-1): #adding all to one string
            temp += str(artists[i][j])
            if(j < len(artists[i])-2): temp += ", "
        artists[i] = temp

    print("tracks and artists")
    output = []
    for i in range(len(tracks)):
        output.append(tracks[i]+" - "+artists[i])
        print(tracks[i]+" - "+artists[i])
    return output

######################################################################################################################################       
# html parsing
def yt_query(name):
    query = urllib.parse.quote(name)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    urls = []
    #print("possible links:")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        urls.append('https://www.youtube.com' + vid['href'])
        #print('     https://www.youtube.com' + vid['href'])
    return urls

# download each video (with first result)
def yt_download(name):

    #Check if video already downloaded
    if os.path.isfile(vid_dir+"/"+name+".mp4"):
        print(name, "has already been downloaded, skipping")
        return 0
    
    print("Downloading", name, "...")
    urls = yt_query(name)
    yt_url_download(urls[0], name=name)


# --- Function to Download a Video URL ---
failed_downloads =[]

# Helper Function for Progress Bar
def progress_Check(stream = None, chunk = None, remaining = None):
    #Gets the percentage of the file that has been downloaded.
    percent = (100*(file_size-remaining))/file_size
    bar.update(percent)
    # print("{:00.0f}% downloaded".format(percent))


def yt_url_download(url, name=""):
    # Global Variables to Modify
    global failed_downloads
    global file_size # For Progress Bar
    global bar       # For Progress Bar

    start_time = time.time()
    # print("URL: ", url)
    yt = YouTube(url, on_progress_callback=progress_Check)

    # Choosing Stream
    if (audio_only):
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.filter(progressive = True).first()

    # Get setting up file size variable for progress bar
    file_size = stream.filesize

    # Check Custom Name Setting
    if not customname:
        name = ""

    # Downloading File
    with progressbar.ProgressBar(max_value=100) as bar:
        
        success = False
        try:
            if name!="":
                stream.download(vid_dir, filename=name) #save file as filename to specified dir
            else:
                stream.download(vid_dir)

            success= True
        except Exception as e:
            print("Error Downloading File")
            print("Error: " + str(e))
            pass

    # Collating Failed Videos to Try Again
    if not success:
        failed_downloads.append((url, name))

        
    # Sleeping to Prevent Youtube Blockage
    time_taken = time.time() - start_time
    time_to_sleep = 10 - time_taken
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)
    


#Post Processing (Convert to MP3)
def convert_vid_to_audio(vid_dir, audio_dir):
    print("Downloads (Hopefully) Complete; Converting MP4 to MP3...")
    try:
        os.mkdir(audio_dir) #create audio_dir if it doesnt already exist
    except:
        pass
    
    for song in os.listdir(vid_dir):
        
        initial_file = vid_dir+"/"+song
        final_file = audio_dir+"/"+song[:-4]+".mp3"
        if (os.path.isfile(final_file)): #avoid converting repeated files
            print("Already Converted " + song + ", skipping")
            continue
        print("Converting: " +song)
        ff = ffmpy3.FFmpeg(
            inputs={initial_file: ["-y"]},
            outputs={final_file:None}
            )
        #print(ff.cmd)
        ff.run()

def clear_temp_vid_files(vid_dir):
    shutil.rmtree(vid_dir)

def download_fails_fn():
    
    global failed_downloads
    if failed_downloads == []:
       return
    print("Trying to Download Failed Files")
    for index, (url, name) in enumerate(failed_downloads):
        print(index+1, "/", len(failed_downloads))
        yt_url_download(url,name)
    convert_vid_to_audio(vid_dir, audio_dir)
        

    

###################################################################################################################################
# MAIN
def presets():
    global vid_dir
    global audio_dir
    global audio_only
    global customname
    vid_dir = "songs"
    audio_dir = "mp3"
    audio_only = False
    customname = True

    #Check if vid_dir exist
    try:
        os.mkdir(vid_dir) #create vid_dir if it doesnt already exist
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

    audio_only_string = input("Download Only Using Audio Stream? (y/n?) (slower but less space required, default:False)")
    if audio_only_string == "y" or audio_only_string == "true":
        audio_only = True
        print("Audio Stream Only: True")
    else:
        audio_only = False
        print("Audio Stream Only: False")

    customname_string = input("Custom Names for Song (from spotify playlist/csv file/ adhoc; if false, name of YouTube Video is used as song name) ? (y/n?), default:True)")
    if customname_string == "n" or customname_string == "false":
        customname = False
        print("Custom Names: False")
    else:
        customname = True
        print("Custom Names: True")

    #Check if vid_dir exist
    try:
        os.mkdir(vid_dir) #create vid_dir if it doesnt already exist
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
        #Gather Input
        print("---Spotify Download---")
        playlist_url = input("Playlist URL: ")
        print("")

        spotify_download(playlist_url)
        
    elif operation == "x":
        #Gather Input
        print("---CSV Download---")
        
        csv_filename = input("CVS File Path: (default:songs.csv)")
        print("")
        if csv_filename =="":
            csv_filename = "songs.csv"
            
        csv_download(csv_filename)
        
    elif operation == "y":
        playlist_url = input("Playlist URL: ")#https://www.youtube.com/watch?v=q3tG-1yONdU&list=PLs6QjtyrwVUZLgfAkvF8DdnNC7cYFHdTq
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
        #Gather Input
        print("---Adhoc Download---")
        n = input("How many songs/videos do you want? [just press enter to return to main menu]: ")
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

    if download_fails:
        download_fails_fn()
    
    close()

def adhoc_download(names):
    print("Downloading" , len(names), "files")
    for name in names:
        yt_download(name)
    convert_vid_to_audio(vid_dir, audio_dir)


def spotify_download(playlist_url):
    playlist = spotify_import(playlist_url)
    
    #print(playlist)
    cont = input("Continue? (y/n):  ")
    if (cont == "y"):
        try:
            for song in playlist:
                yt_download(song)
        except:
            pass
        convert_vid_to_audio(vid_dir, audio_dir)
    else:
        print ("")
        main()


def csv_download(csv_filename):
    songs = [] #songs[i] = (title, artist)
    try:
        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                songs.append((row[0], row[1]))
    except Exception as e:
        print(e)
        print("Error Occured Reading CSV, please ensure that the file exist and is formatted properly")
        return

    for index, song in enumerate(songs):
        print(index,": " + song[0])
        
    #print(songs)
    try:
        for song in songs:
            query_string = song[0] + " " + song[1]
            yt_download(query_string)
    except:
        pass
    convert_vid_to_audio(vid_dir, audio_dir)


def youtube_playlist_download(playlist_url):
    print("---Youtube Playlist Download---")
    playlist = Playlist(playlist_url)
    playlist.populate_video_urls()
    print("Number of Videos in Playlist: ", len(playlist.video_urls))
    print(playlist.video_urls)
    cont = input("Continue? (y/n):  ")
    if (cont == "y"):
        try: 
            for index, url in enumerate(playlist.video_urls):
                print(index+1, "/", len(playlist.video_urls))
                yt_url_download(url)

        except:
            pass
        convert_vid_to_audio(vid_dir, audio_dir)
    else:
        print ("")
        main()
    
def close():
    print("")
    print("************************************************************")
    if os.listdir(vid_dir) == []: #if user hasnt downloaded anything, dont quit
        main()
    print("All pending operations complete, songs stored in mp3 folder.")
    exiting = input("Would you like to exit this program? (y/n?): ")
    if(exiting == "n" or exiting ==""):
        print("")
        main()
    else:
        clear_temp_vid_files(vid_dir)
        sys.exit() #to prevent multiple queries


    
#Autorun Main Function
if __name__ == '__main__':
    main()

