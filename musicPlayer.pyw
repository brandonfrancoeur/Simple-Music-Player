from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
from fileinput import filename


#create window
window = Tk()

#Create the menu bar
menuBar = Menu(window)
window.config(menu=menuBar)


#Command Functions
def play():
    try:
        #check if paused variable was created
        paused

    #if paused has not been created, start playing the file
    except NameError:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusBar['text'] = "Playing Music File - " + os.path.basename(filename)
        except:
           tkinter.messagebox.showerror("File not found", "Simple Music Player could not find the file")

    #if paused has been created, unpause the music
    else:
        mixer.music.unpause()
        statusBar['text'] = "Music Unpaused- " + os.path.basename(filename)

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

def openFile():
    global filename
    filename = filedialog.askopenfilename()

#Create submenu
subMenu = Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command = openFile)
subMenu.add_command(label="Exit", command = window.destroy)

subMenu = Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command = about)

#Change window dimensions and title
window.geometry('300x300')
window.title("Simple Music Player")

#set up pygame mixer
mixer.init()

#change the icon
window.iconbitmap(r'musical-note.ico')
text = Label(window, text="let's do something with this")
text.pack()

#create buttons
playImage= PhotoImage(file='play-button.png')
playButton = Button(window, image =playImage, command = play)
playButton.pack()

stopImage= PhotoImage(file='stop.png')
stopButton = Button(window, image =stopImage, command = stop)
stopButton.pack()

pauseImage= PhotoImage(file='pause.png')
pauseButton = Button(window, image =pauseImage, command = pause)
pauseButton.pack()

#create the volume scale
volumeScale = Scale(window, from_=0, to=100, orient=HORIZONTAL, command = setVolume)

#set the default volume to 75%
volumeScale.set(75)
mixer.music.set_volume(0.75)
volumeScale.pack()

#create the status bar
statusBar = Label(window, text="Welcome to Simple Music Player", relief = GROOVE, anchor = W)
statusBar.pack(side = BOTTOM, fill = X)


window.mainloop()

