#!/usr/bin/python3

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize
import tkinter as tk
from tkinter import filedialog
import os
from platform import system as thisSystemIs


class Giffer:

    def __init__(self, mainWindow):
        self.fileName = ""
        self.dirName = ""
        self.videoLength = 1
        self.continueConversion = True
        self.cwd = os.getcwd()

        mainFrame = tk.Frame(mainWindow)
        mainFrame.pack()

        fileFrame = tk.Frame(mainFrame)
        fileFrame.pack(padx=(20, 20))
        self.fileLabel = tk.Label(fileFrame, text="Choose a file to convert:")
        self.fileLabel.pack(fill=tk.BOTH, expand=1, pady=(20, 0))

        self.fileText = tk.Text(fileFrame, height=1, width=60)
        self.fileText.configure(state='normal')
        self.fileText.insert(tk.END, "Browse for a file to convert.->", )
        self.fileText.configure(state='disabled')
        self.fileText.pack(side=tk.LEFT)

        self.browseFile = tk.Button(fileFrame, text="Choose video", command=self.browseFile)
        self.browseFile.pack(side=tk.LEFT)

        settingsFrame = tk.Frame(mainFrame)
        settingsFrame.pack()

        self.startSliderLabel = tk.Label(settingsFrame, text="GIF start point: ")
        self.startSlider = tk.Scale(settingsFrame, from_=0, to=self.videoLength, length=500, resolution=.01,
                                    orient=tk.HORIZONTAL, command=self.moveEndSlider)
        self.endSliderLabel = tk.Label(settingsFrame, text="GIF end point: ")
        self.endSlider = tk.Scale(settingsFrame, from_=1, to=self.videoLength, length=500, resolution=.01,
                                  orient=tk.HORIZONTAL, command=self.moveStartSlider)
        self.fpsSliderLabel = tk.Label(settingsFrame, text="GIF FPS: ")
        self.fpsSlider = tk.Scale(settingsFrame, from_=5, to=24, length=300, resolution=1.0, orient=tk.HORIZONTAL)
        self.sizeSlideLabel = tk.Label(settingsFrame, text="GIF resolution: ")
        self.sizeSlide = tk.Scale(settingsFrame, to=1080, from_=360, length=300, resolution=1.0, orient=tk.HORIZONTAL,
                                  command=self.calcNewSize)
        self.newSizeLabel = tk.Label(settingsFrame)

        dirFrame = tk.Frame(mainFrame)
        dirFrame.pack()

        self.dirLabel = tk.Label(dirFrame, text="Choose a DIR for GIF:")
        self.dirLabel.pack(fill=tk.BOTH, expand=1, pady=(20, 0))
        self.dirText = tk.Text(dirFrame, height=1, width=60)
        self.dirText.configure(state='normal')
        self.dirText.insert(tk.END, "Browse for a destination for GIF. ->", )
        self.dirText.configure(state='disabled')
        self.dirText.pack(side=tk.LEFT)
        self.dirDestination = tk.Button(dirFrame, text="Choose DIR", command=self.browseDir)
        self.dirDestination.pack(side=tk.LEFT)

        gifNameFrame = tk.Frame(mainFrame)
        gifNameFrame.pack(pady=(20, 0))
        self.gifNameLabel = tk.Label(gifNameFrame, text="Name your GIF: ")
        self.gifNameLabel.pack(side=tk.LEFT)
        self.gifNameText = tk.Text(gifNameFrame, height=1, width=30)
        self.gifNameText.pack(side=tk.LEFT)
        self.dotGifLabel = tk.Label(gifNameFrame, text=".gif")
        self.dotGifLabel.pack(side=tk.LEFT)

        outPutFrame = tk.Frame(mainFrame)
        outPutFrame.pack()

        self.bgImg = tk.PhotoImage(file="vis_gust_text.png")

        self.outPutLabel = tk.Label(outPutFrame, text="Output: ")
        self.outPutLabel.pack(pady=(20, 0))
        self.outputText = tk.Text(outPutFrame, height=18, width=70)

        self.outputText.configure(state='normal')
        self.outputText.insert(tk.END, "                ")
        self.outputText.image_create(tk.END, image=self.bgImg)
        self.outputText.insert(tk.END, "\n")
        self.outputText.configure(state='disabled')

        self.outputText.pack(pady=(0, 20))

        self.convertBtn = tk.Button(mainFrame, text="Convert!", command=self.convertFile)
        self.convertBtn.pack(side=tk.LEFT, padx=(30, 440), pady=(0, 20))

        self.quitBtn = tk.Button(mainFrame, text="Quit", command=mainWindow.quit)
        self.quitBtn.pack(side=tk.LEFT, pady=(0, 20))

    def calcNewSize(self, val):
        videoFile = VideoFileClip(self.fileName)
        height = int(val)
        width = videoFile.w * (height / videoFile.h)
        self.newSizeLabel.configure(text=str(int(width)) + "x" + str(height))

    def moveStartSlider(self, val):
        maxValue = float(val) -1.0
        self.startSlider.configure(to=maxValue)

    def moveEndSlider(self, val):
        minValue = float(val) + 1.0
        self.endSlider.configure(from_=(minValue))

    def browseFile(self):
        self.fileName = filedialog.askopenfilename(initialdir="/home/x1mq/Downloads/", title="Select video file",
                                                   filetypes=(("mp4", "*.mp4"), ("mkv", "*.mkv"), ("mpeg", "*.mpeg"),
                                                              ("avi", "*.avi"), ("mov", "*.mov"), ("all", "*.*")))
        try:
            videoFile = VideoFileClip(self.fileName)
        except:
            self.fileName = ""
            self.popUps("Invalid file selected.")
            return

        self.fileText.configure(state='normal')
        self.fileText.delete(1.0, tk.END)
        self.fileText.insert(tk.END, self.fileName)
        self.fileText.configure(state='normal')
        self.videoLength = videoFile.duration

        self.startSlider.configure(to=self.videoLength)
        self.endSlider.configure(to=self.videoLength)
        self.endSlider.set(self.videoLength)

        self.fpsSlider.set(15)

        self.sizeSlide.configure(to=videoFile.h)
        self.sizeSlide.set(videoFile.h)

        self.startSliderLabel.pack(pady=(10, 0))
        self.startSlider.pack()
        self.endSliderLabel.pack(pady=(10, 0))
        self.endSlider.pack()
        self.fpsSliderLabel.pack(pady=(10, 0))
        self.fpsSlider.pack()
        self.sizeSlideLabel.pack(pady=(10, 0))
        self.sizeSlide.pack()
        self.newSizeLabel.pack()

    def browseDir(self):
        self.dirName = filedialog.askdirectory(initialdir="/home/x1mq/Downloads/")
        self.dirText.configure(state='normal')
        self.dirText.delete(1.0, tk.END)
        self.dirText.insert(tk.END, self.dirName)
        self.dirText.configure(state='disabled')

    def popUps(self, val):
        popup = tk.Toplevel()
        popup.geometry("300x125")
        popup.wm_title("Wake up!")
        popupLabel = tk.Label(popup, text="Unexpected problem..")
        popupLabel.pack(pady=(10, 10))
        popInfo = val
        label = tk.Label(popup, text=popInfo)
        label.pack()
        okBtn = tk.Button(popup, text="OK", command=popup.destroy)
        okBtn.pack(pady=(20, 20))

    def convertFile(self):
        if len(self.fileName) < 1:
            self.popUps("Select video to continue.")
            return

        if len(self.dirName) < 1:
            self.popUps("Select directory to continue.")
            return

        #Disable self.convertBtn, the button that runs the function.
        self.convertBtn.config(state=tk.DISABLED)

        nameOfGif = self.gifNameText.get("1.0", "end-1c")

        if len(nameOfGif) < 1:
            nameOfGif = "default.gif"
        else:
            nameOfGif += ".gif"

        video = VideoFileClip(self.fileName)

        videoCutDown = round(self.endSlider.get() - self.startSlider.get(), 2)

        self.outputText.configure(state='normal')
        self.outputText.insert(tk.END, "Filename: " + self.fileName + '\n')
        self.outputText.insert(tk.END, "Directory: " + self.dirName + '\n')
        self.outputText.insert(tk.END, "Video length: " + str(videoCutDown) + '\n')
        self.outputText.insert(tk.END, "FPS: " + str(self.fpsSlider.get()) + '\n')
        self.outputText.insert(tk.END, "Resolution: " + str(self.sizeSlide.get()) + '\n')
        self.outputText.insert(tk.END, "GIF name: " + nameOfGif + '\n' + '\n')
        self.outputText.see(tk.END)
        self.outputText.configure(state='disabled')

        root.update_idletasks()

        self.continueConversion = True

        if os.path.isfile(self.dirName + "/" + nameOfGif):
            self.popUps("file already exists")
            self.continueConversion = False
            self.outputText.configure(state='normal')
            self.outputText.insert(tk.END,
                                   "File already exists, conversion canceled...\n--------------------------------------------\n")
            self.outputText.configure(state='disabled')
            return

        if self.continueConversion:
            try:
                if (video.duration != videoCutDown):
                    video = VideoFileClip(self.fileName).subclip((self.startSlider.get()), (self.endSlider.get()))
                if video.h != self.sizeSlide.get():
                    newVideoHeight = self.sizeSlide.get()
                    resizedVideo = resize(video, height = newVideoHeight)

                os.chdir(self.dirName)
                resizedVideo.write_gif(nameOfGif, fps=self.fpsSlider.get(), program="ffmpeg")
                os.chdir(self.cwd)

                self.outputText.configure(state='normal')
                self.outputText.insert(tk.END, "Conversion completed successfully! *GIF GIF*\n")
                self.outputText.insert(tk.END, "--------------------------------------------\n")
                self.outputText.see(tk.END)
                self.outputText.configure(state='disabled')

                self.gifNameText.delete('1.0', tk.END)
            except Exception as e:
                print(e)
                self.outputText.insert(tk.END, "OH NO! Something went wrong! *Visible disgust*\n\n")
                self.outputText.configure(state='disabled')

            #Conversion should be complete, Enable
            self.convertBtn.config(state=tk.NORMAL)


root = tk.Tk(className='GifMaker')
root.title("GifMaker 2021 v 0.1")
myOS = thisSystemIs()

if (myOS == "Linux"):
    root.iconphoto(False, tk.PhotoImage(file='vis_gust.png'))
elif (myOS == "Windows"):
    root.iconbitmap("vis_gust_small_icon.ico")

app = Giffer(root)
root.mainloop()
