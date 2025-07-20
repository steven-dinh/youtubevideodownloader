from pytube import YouTube
import tkinter as tk
from tkinter import messagebox
#functions
#def
def properUrl(url):
    if len(url) >= 31 and url[:32] == 'https://www.youtube.com/watch?v=':
        return True
    else:
        messagebox.showerror('Error', 'Invalid URL')
        return False

def getEntry(entryName, updateLabel):
    entry = entryName.get()
    if properUrl(entry):
        updateLabel.config(text=f"Current url: {entry}")
        try:
            yt = YouTube(entry)
            videoTitleLabel.config(text=f"Video Title: {yt.title}")
        except Exception as e:
            messagebox.showerror('Error', 'Failed to fetch video')


root = tk.Tk()
root.geometry("350x400")
root.resizable(False, False)

root.title("Youtube Video Downloader")

#url part of gui
enterUrlLabel = tk.Label(root, text="Enter url")
enterUrlLabel.grid(row=0, column=0)

urlEntry = tk.Entry(root, width=40)
urlEntry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

urlLabel = tk.Label(root, text="Current url: ") # 13
urlLabel.grid(row=2, column=0, padx=(10, 0), sticky="w")

entryButton = tk.Button(root, text="Enter", command=lambda: getEntry(urlEntry, urlLabel))
entryButton.grid(row=1, column=1)

videoTitleLabel = tk.Label(root, text="Video Title: ")
videoTitleLabel.grid(row=3, column=0,sticky="w",padx=(10, 0))

#selection box


root.mainloop()