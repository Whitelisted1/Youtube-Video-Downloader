from pytube import YouTube, Playlist
from os.path import dirname, join, isdir
from sys import argv

directory = dirname(argv[0])

open(join(directory, "async.txt"), "a").close()
f = open(join(directory, "async.txt"), "r")
asyncenabled = f.read()
f.close()
if asyncenabled == "":
    f = open(join(directory, "async.txt"), "w")
    f.write("False")
    f.close()

asyncenabled = asyncenabled.replace(" ", "")
if asyncenabled == "True" or asyncenabled == "true" or asyncenabled == "1":
    asyncenabled = True
    from threading import Thread
else:
    asyncenabled = False

if not isdir(join(directory, "videos")):
    from os import mkdir
    mkdir(join(directory, "videos"))


def asyncdownloadvid(video, audioOnly):
    if not audioOnly:
        YouTube(video).streams.get_highest_resolution().download(join(directory, "videos"))
    else:
        yt = YouTube(video)
        t=yt.streams.filter(only_audio=True)
        t[0].download(join(directory, "videos"))

def downloadvid(video, audioOnly):
    if not asyncenabled:
        if not audioOnly:
            YouTube(video).streams.get_highest_resolution().download(join(directory, "videos"))
        else:
            yt = YouTube(video)
            t=yt.streams.filter(only_audio=True)
            t[0].download(join(directory, "videos"))
    else:
        Thread(target=asyncdownloadvid, args=(video, audioOnly)).start()

def main():
    while True:
        print("\nYoutube Downloader made by Whitelisted (https://bit.ly/WhitelistedYT)")
        userinput = input("What would you like to do?\n1) Download a video\n2) Download a playlist\n$ ")
        if userinput == "1":
            section = "1"
            break
        elif userinput == "2":
            section = "2"
            break
        else:
            print("That is not a correct input value!")

    while True:
        userinput = input("\nWould you like the video to be audio only?\n1) No\n2) Yes\n$ ")
        if userinput == "1":
            audio = False
            break
        elif userinput == "2":
            audio = True
            break
        else:
            print("That is not a correct input value!")

    printdone = True
    if section == "1":
        try:
            video = input("Please enter the full video URL (Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n$ ")
            print("Downloading video...")
            downloadvid(video, audio)
        except Exception as e:
            print(e)
            print("An error occured. (Invalid link?)")
            printdone = False
    elif section == "2":
        try:
            playlist = input("Please enter the playlist URL (Example: https://www.youtube.com/playlist?list=PLyDpmmtP4fWVoj8HaQffdDrGCuUX_52tn)\n$ ")
            playlist = Playlist(playlist)
            playlistlen = len(playlist.video_urls)
            print(f'Number of videos in playlist: {playlistlen}')
            done = 0
            for video_url in playlist.video_urls:
                downloadvid(video_url, audio)
                done += 1
                print(f'Downloaded {video_url} ({done}/{playlistlen})', end="\r")
        except Exception as e:
            print(e)
            print("An error occured. (Invalid link?)")
            printdone = False
    
    if printdone and not asyncenabled:
        print("Done downloading video(s)")
    elif asyncenabled:
        print("\nDownloading video(s) in the background..")
    main()


while True:
    main()