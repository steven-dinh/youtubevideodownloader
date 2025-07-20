import yt_dlp
import tkinter as tk
from tkinter import messagebox
#functions
#def
def properUrl(url):
    if url.startswith('https://www.youtube.com/watch?v='):
        return True
    else:
        messagebox.showerror('Error', 'Invalid URL')
        return False

def getEntry(entryName, updateLabel):
    entry = entryName.get()
    if properUrl(entry):
        if len(entry) >= 37:
            spliced_entry = entry[:37] + "..."
            updateLabel.config(text=f"Current url: {spliced_entry}")
        else:
            updateLabel.config(text=f"Current url: {entry}")
        try:

            videoTitleLabel.config(text=f"Video Title: {}")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to fetch video:\n{str(e)}')


root = tk.Tk()
root.geometry("350x400")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.title("Youtube Video Downloader")

#url part of gui
enterUrlLabel = tk.Label(root, text="Enter url")
enterUrlLabel.grid(row=0, column=0)

urlEntry = tk.Entry(root, width=40)
urlEntry.grid(row=1, column=0, padx=(10, 0), sticky='ew')

urlLabel = tk.Label(root, text="Current url: ", justify='right') # 13
urlLabel.grid(row=2, column=0, padx=(10, 0), sticky="w",)

entryButton = tk.Button(root, text="Enter", command=lambda: getEntry(urlEntry, urlLabel))
entryButton.grid(row=1, column=1, sticky='w')

videoTitleLabel = tk.Label(root, text="Video Title: ")
videoTitleLabel.grid(row=3, column=0,sticky="w",padx=(10, 0))

#selection box


root.mainloop()