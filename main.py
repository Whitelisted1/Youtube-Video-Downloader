from pytube import YouTube, Playlist
from os.path import dirname, join, isdir
from sys import argv
from threading import Thread

directory = dirname(argv[0])

asyncenabled = False
if not isdir(join(directory, "videos")):
    from os import mkdir
    mkdir(join(directory, "videos"))

def downloadvid(video, audioOnly, quality, threaded=False):
    if not asyncenabled or threaded:
        if not audioOnly:
            if quality != 'highest':
                YouTube(video).streams.get_by_resolution(quality).download(join(directory, "videos"))
            elif quality == "highest":
                YouTube(video).streams.get_highest_resolution().download(join(directory, "videos"))
        else:
            yt = YouTube(video)
            t=yt.streams.filter(only_audio=True)
            t[0].download(join(directory, "videos"))
    else:
        Thread(target=downloadvid, args=(video, audioOnly, quality, True)).start()

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
            quality = None
            break
        else:
            print("That is not a correct input value!")
    
    if not audio:
        while True:
            quality = None
            userinput = input("\nWhat would you like the video quality to be?\n1) Highest\n2) 1080p\n3) 720p\n4) 360p\n$ ")
            if userinput == '1':
                quality = 'highest'
                break
            elif userinput == '2':
                quality == '1080p'
                break
            elif userinput == '3':
                quality == '720p'
                break
            elif userinput == '4':
                quality == '360p'
                break
            else:
                print(f"'{userinput}' is not a legal input!")

    printdone = True
    if section == "1":
        try:
            video = input("\nPlease enter the full video URL (Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n$ ")
            print("Downloading video...")
            downloadvid(video, audio, quality)
        except Exception as e:
            print(e)
            print("An error occured. (Invalid link?)")
            printdone = False
    elif section == "2":
        try:
            playlist = input("\nPlease enter the playlist URL (Example: https://www.youtube.com/playlist?list=PLyDpmmtP4fWVoj8HaQffdDrGCuUX_52tn)\n$ ")
            playlist = Playlist(playlist)
            playlistlen = len(playlist.video_urls)
            print(f'Number of videos in playlist: {playlistlen}')
            done = 0
            for video_url in playlist.video_urls:
                downloadvid(video_url, audio, None)
                done += 1
                print(f'Downloaded {video_url} ({done}/{playlistlen})', end="\r")
        except Exception as e:
            print(e)
            print("An error occured. (Invalid link?)")
            printdone = False
    
    if printdone and not asyncenabled: print("\nDone downloading video(s)")
    elif asyncenabled: print("\nDownloading video(s) in the background..")
    main()


while True:
    main()
