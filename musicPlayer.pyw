from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
from fileinput import filename
from mutagen.mp3 import MP3
import time
import threading

#create mainWindowW
mainWindow = Tk()

#create the status bar
statusBar = Label(mainWindow, text="Welcome to Simple Music Player", relief = GROOVE, anchor = W)
statusBar.pack(side = BOTTOM, fill = X)

#Create the menu bar
menuBar = Menu(mainWindow)
mainWindow.config(menu=menuBar)

#create frames for the layout

#left frame contains song list
leftFrame = Frame(mainWindow)
leftFrame.pack(side=LEFT, padx=30)

#right frame contains time info, main buttons and volume slider
rightFrame = Frame(mainWindow)
rightFrame.pack()

#top frame contains the time info
rightTopFrame = Frame(rightFrame)
rightTopFrame.pack()

#middle frame contains play, pause and stop buttons
rightMiddleFrame = Frame(rightFrame)
rightMiddleFrame.pack(padx=25, pady=25)

#bottom frame contains mute, rewind and volume scale
rightBottomFrame = Frame(mainWindow)
rightBottomFrame.pack()

#Command Functions

def showDetails():
    fileEXT = os.path.splitext(filename)

    if fileEXT[1] == '.mp3':
        song = MP3(filename)
        totalLength = song.info.length
    else:
        song = mixer.Sound(filename)
        totalLength = song.get_length()

    #store the minutes and seconds and round out the decimals
    m, s = divmod(totalLength, 60)
    m = round(m)
    s = round(s)
    timeFormat = '{:02d}:{:02d}'.format(m,s)
    lengthText['text'] = "Song Length- " + timeFormat

    #Threading is used to make sure the countdown is always running when the song is playing
    t1 = threading.Thread(target=calculateTimeElapsed, args=(totalLength,))
    t1.start()


def calculateTimeElapsed(length):
    #using the getbusy() function to keep track of the music stopping
    global paused
    timeElapsed = 0
    while timeElapsed <= length and mixer.music.get_busy():
        if paused:
            continue
        else:
            m, s = divmod(timeElapsed, 60)
            m = round(m)
            s = round(s)
            timeFormat = '{:02d}:{:02d}'.format(m,s)
            currentTime['text'] = "Time Elapsed- " + timeFormat
            time.sleep(1)
            timeElapsed += 1

#create a variable to keep track of the status of the music
paused = FALSE

def play():
    global paused

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Unpaused- " + os.path.basename(filename)
        paused = FALSE
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            showDetails()
            statusBar['text'] = "Playing Music File - " + os.path.basename(filename)
        except:
           tkinter.messagebox.showerror("File not found", "Simple Music Player could not find the file")

def stop():
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"

def pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "Music Paused"

def setVolume(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

def about():
    tkinter.messagebox.showinfo('About Simple Music Player', 'This is a simple audio player that I created using python. I utilized the pygame mixer library for the functionality' )

#keep track of how many songs have been added to the playlist
playListIndex = 0

#add a song to the playlist box
def addToPlaylist(file):
    global playListIndex
    file = os.path.basename(file)
    playList.insert(playListIndex, file)
    playListIndex+=1

#open a file dialog
def openFile():
    global filename
    filename = filedialog.askopenfilename()
    addToPlaylist(filename)

def rewind():
    play()
    statusBar['text'] = "Music Restarted"

#keep track of whether the music has been muted or not
muted=FALSE
def mute():
    global muted

    #unmute music
    #TODO: make it go back to whatever the volume was before muting
    if muted:
        muted=FALSE
        mixer.music.set_volume(.75)
        volumeButton.configure(image=volumeImage)
        volumeScale.set(75)

    #mute the music
    else:
        muted=TRUE
        mixer.music.set_volume(0)
        volumeButton.configure(image=muteImage)
        volumeScale.set(0)

#exit the function without throwing an exception
def exitFunction():
    stop()
    mainWindow.destroy()

#Create text boxes for Song length and time elapsed
lengthText = Label(rightTopFrame, text="Song Length- --:--")
lengthText.pack(pady=10)
currentTime = Label(rightTopFrame, text="Time Elapsed- --:--")
currentTime.pack()

#Display the next songs in the queue
playList = Listbox(leftFrame)
playList.pack()

#Create submenu
subMenu = Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command = openFile)
subMenu.add_command(label="Exit", command = mainWindow.destroy)

subMenu = Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command = about)

#Change mainWindow  title
mainWindow.title("Simple Music Player")

#set up pygame mixer
mixer.init()

#change the icon
mainWindow.iconbitmap(r'icons/musical-note.ico')

#create buttons
playImage= PhotoImage(file='icons/play-button.png')
playButton = Button(rightMiddleFrame, image =playImage, command = play)
playButton.pack(side=LEFT, padx=10)

stopImage= PhotoImage(file='icons/stop.png')
stopButton = Button(rightMiddleFrame, image =stopImage, command = stop)
stopButton.pack(side=LEFT, padx=10)

pauseImage= PhotoImage(file='icons/pause.png')
pauseButton = Button(rightMiddleFrame, image =pauseImage, command = pause)
pauseButton.pack(side=LEFT, padx=10)

rewindImage= PhotoImage(file='icons/rewind.png')
rewindButton = Button(rightBottomFrame, image =rewindImage, command = rewind)
rewindButton.grid(row=0, column=0)

volumeImage = PhotoImage(file='icons/volume.png')
muteImage = PhotoImage(file='icons/mute.png')
volumeButton = Button(rightBottomFrame, image =volumeImage, command = mute)
volumeButton.grid(row=0, column=1)

addSongButton = Button(leftFrame, text="+ Add", command = openFile)
addSongButton.pack(side = LEFT)

removeSongButton = Button(leftFrame, text="- Remove")
removeSongButton.pack(side = RIGHT)

#create the volume scale
volumeScale = Scale(rightBottomFrame, from_=0, to=100, orient=HORIZONTAL, command = setVolume)

#set the default volume to 75%
volumeScale.set(75)
mixer.music.set_volume(0.75)
volumeScale.grid(row=0, column = 2,pady=10, padx=25)



mainWindow.protocol("WM_DELETE_WINDOW", exitFunction)
mainWindow.mainloop()

