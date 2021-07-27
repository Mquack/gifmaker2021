#!/usr/bin/python3

from moviepy.editor import *
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import sys
import subprocess
from time import sleep

cwd = os.getcwd()

fileName = ""
dirName = ""
vidLen = 0

window = tk.Tk()

window.title("GifMaker 2021 v 0.1")
window.minsize(650,550)

class toTextWidget():

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)

    def flush(self):
        pass


def moveEndSlider(val):
    minValue = float(val) + 1.0
    endSlider.configure(from_=(minValue))

def moveStartSlider(val):
    maxValue = float(val) - 1.0
    startSlider.configure(to=maxValue)

def calcNewSize(val):
    videoFile = VideoFileClip(fileName)
    height = int(val)
    width = videoFile.w * (height / videoFile.h)
    newSizeLabel.configure(text = str(int(width)) + "x" + str(height))


def popup(msg):
    popup = tk.Tk()
    popup.wm_title("Unexpected problem")
    popInfo = "You haven't filled out all the information. Please "
    popInfo += msg
    label = Label(popup, text=popInfo)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def convertFile():
    global fileName
    global dirName

    gifName = gifText.get("1.0", "end-1c")
    if len(gifName) < 1:
        gifName = "default"
    gifName += ".gif"

    if len(fileName) < 1:
        popup("chose a file.")
        return
    if len(dirName) < 1:
        popup("chose a directory.")
        return

    outputText.insert("end", "Starting...\nPlease wait..\n")
    window.update_idletasks()

    video = (VideoFileClip(fileName))
    if video.h != sizeSlide.get():
        video = video.resize(height=sizeSlide.get())

    os.chdir(dirName)
    video.write_gif(gifName, fps=fpsSlider.get(), program = "ffmpeg")
    os.chdir(cwd)

    #print(gifName, "\n", fileName, "\n", dirName, "\n", startSlider.get(), "\n", endSlider.get(), "\n", fpsSlider.get(), "\n", sizeSlide.get())


def browseFile():
    global fileName
    global vidLen

    fileName = filedialog.askopenfilename(initialdir = "/home/ubuvirt/Videos", title = "Select video file", filetypes = (("mp4", "*.mp4"),("mkv", "*.mkv"), ("all", "*.*")))
    fileText.delete(1.0,END)
    fileText.insert(tk.END, fileName)

    videoFile = VideoFileClip(fileName)
    vidLen = videoFile.duration

    startSlider.configure(to=vidLen)

    endSlider.configure(to=vidLen)
    endSlider.set(vidLen)

    fpsSlider.set(15)

    sizeSlide.configure(to = videoFile.h)
    sizeSlide.set(videoFile.h)
    newSizeLabel.configure(text = (str(videoFile.w) + "x" + str(videoFile.h) ))

    settingsFrame.grid(column = 0, row = 2)

def browseDir():
    global dirName
    dirName = filedialog.askdirectory(initialdir = "/home")
    dirText.delete(1.0,END)
    dirText.insert(tk.END, dirName)

emptyLabel = Label(window, text = "\n")

runButton = Button(window, text = "Convert!", command = convertFile)

outputLabel = Label(window, text = "Output:")
outputText = Text(window, height = 18, width = 70)

#---------------------------------------------GRID--------------------------------------

#Frame for video file info
fileInfoFrame = Frame(window)
fileInfoFrame.grid(column = 0, row = 1)

fileLabel = Label(fileInfoFrame, text = "Choose a file to convert:")
fileText = Text(fileInfoFrame, height = 1, width = 60)
fileText.insert(tk.END, "Browse for a file to convert.->")
browseForVid = Button(fileInfoFrame, text = "Choose video", command = browseFile)

fileLabel.grid(column = 0, row = 0)
fileText.grid(column = 0, row = 1)
browseForVid.grid(column = 1, row = 1)

#Frame for settings inside fileInfoFrame
settingsFrame = Frame(fileInfoFrame)
esLabel = Label(settingsFrame, text = "End GIF at:")
endSlider = Scale(settingsFrame, from_ = 1, to = vidLen, length = 500, resolution = .01, orient = HORIZONTAL, command = moveStartSlider)
ssLabel = Label(settingsFrame, text = "Start GIF at:")
startSlider = Scale(settingsFrame, from_ = 0, to = vidLen, length = 500, resolution = .01, orient = HORIZONTAL, command = moveEndSlider)
fpsLabel = Label(settingsFrame, text = "Set FPS for GIF:")
fpsSlider = Scale(settingsFrame, from_ = 5, to = 24, length = 300, resolution = 1.0, orient = HORIZONTAL)

sizeLabel = Label(settingsFrame, text = "GIF size:")
sizeSlide = Scale(settingsFrame, to = 1080, from_ = 360, length = 300, resolution = 1.0, orient = HORIZONTAL, command = calcNewSize)
newSizeLabel = Label(settingsFrame)

ssLabel.pack()
startSlider.pack()
esLabel.pack()
endSlider.pack()
fpsLabel.pack()
fpsSlider.pack()
sizeLabel.pack()
sizeSlide.pack()
newSizeLabel.pack()
#------------------------------------------------------

#Frame for gif directory
dirInfoFrame = Frame(window)
dirInfoFrame.grid(column = 0, row = 3)
dirLabel = Label(dirInfoFrame, text = "Choose a directory for GIF:")
dirText = Text(dirInfoFrame, height = 1, width = 60)
dirText.insert(tk.END, "Browse for a destination for GIF. ->")
browseDestination = Button(dirInfoFrame, text = "Choose destination", command = browseDir)

dirLabel.grid(column = 0, row = 0)
dirText.grid(column = 0, row = 1)
browseDestination.grid(column = 1, row = 1)

#Frame for GIF name
gifInfoFrame = Frame(window)
gifInfoFrame.grid(column = 0, row = 4)

gifLabel = Label(gifInfoFrame, text = "Name your GIF:")
gifText = Text(gifInfoFrame, height = 1, width = 20)
gifLabel.grid(column = 0, row = 0)
gifText.grid(column = 1, row = 0)

emptyLabel.grid(column = 1, row = 5)
runButton.grid(column = 0, row = 6)


outputLabel.grid(column = 0, row = 7)
outputText.grid(column = 0, row = 8)

sys.stdout = toTextWidget(outputText)



#TODO: fix time frame
#TODO: make it look good?





















window.mainloop()
