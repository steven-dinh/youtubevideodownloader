from pytube import YouTube
import tkinter as tk

#functions
#def

def getEntry(entryName, updateLabel):
    entry = entryName.get()
    updateLabel.config(text=f"Current url: {entry}")


root = tk.Tk()
root.geometry("350x400")
root.title("Youtube Video Downloader")

#url part of gui
enterUrlLabel = tk.Label(root, text="Enter url")
enterUrlLabel.grid(row=0, column=0)

urlEntry = tk.Entry(root, width=40)
urlEntry.grid(row=1, column=0, padx=10, pady=5)

urlLabel = tk.Label(root, text="Current url: ")
urlLabel.grid(row=2, column=0, padx=(10, 0), sticky="w")

entryButton = tk.Button(root, text="Enter", command=lambda: getEntry(urlEntry, urlLabel))
entryButton.grid(row=1, column=1)


root.mainloop()