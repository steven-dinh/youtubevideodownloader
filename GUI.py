import yt_dlp as ytdlp
import tkinter as tk
from tkinter import messagebox
#functions
#def
def properUrl(url):
    urlFormats = [
        'https://www.youtube.com/watch?v=',
        'https://youtube.com/watch?v=',
        'https://youtu.be/',
        'https://m.youtube.com/watch?v='
    ]
    if any(url.startswith(validUrl) for validUrl in urlFormats):
        return True
    else:
        messagebox.showerror('Error', 'Invalid URL')
        return False

def getURLEntry(entryName, updateLabel):
    entry = entryName.get()
    if properUrl(entry):
        if len(entry) >= 37:
            spliced_entry = entry[:37] + "..."
            updateLabel.config(text=f"Current url: {spliced_entry}")
        else:
            updateLabel.config(text=f"Current url: {entry}")
        try:

            ydl_opts = {
                'format': 'worst',
                'quiet': True,
                'skip_download': True
            }
            with ytdlp.YoutubeDL(ydl_opts) as ydl: #update gui
                info = ydl.extract_info(entry,download=False)
                # update title
                title = info.get('title', 'unknown title')
                videoTitleLabel.config(text=f"Video Title: {title}")
                # update length
                length = info.get('duration', 'unknown length')
                hours = length // 3600
                minutes = (length % 3600) // 60
                seconds = length % 60
                if hours:
                    videoLengthLabel.config(text=f"Video Length: {hours}:{minutes:02}:{seconds:02}")
                else:
                    videoLengthLabel.config(text=f"Video Length: {minutes}:{seconds:02}")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to fetch video:\n{str(e)}')

def getDropdownEntry(entryName, updateLabel):
    entry = entryName.get()
    if updateLabel == qualityLabel:
        updateLabel.config(text=f'Selected Resolution: {entry}')

def onFormatChange(*args):
    Format = selectedFormat.get()
    if Format == 'Video':
        qualityLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
        qualityDropdown.grid(row=9, column=0, sticky="w", padx=(10, 0))
    else:
        qualityLabel.grid_remove()  # hide label
        qualityDropdown.grid_remove()  # hide dropdown

def onQualityChange(*args):
    selected = selectedResolution.get()
    qualityLabel.config(text=f'Selected Resolution: {selected}')

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

entryButton = tk.Button(root, text="Enter", command=lambda: getURLEntry(urlEntry, urlLabel))
entryButton.grid(row=1, column=1, sticky='w')

videoTitleLabel = tk.Label(root, text="Video Title: ")
videoTitleLabel.grid(row=3, column=0,sticky="w",padx=(10, 0))

videoLengthLabel = tk.Label(root, text="Video Length: ")
videoLengthLabel.grid(row=4, column=0,sticky="w",padx=(10, 0))

#selections

#select formate
formatLabel = tk.Label(root, text="Select Format")
formatLabel.grid(row=6, column=0,sticky="w",padx=(10, 0))
formatOptions = ['','Video','MP3']
selectedFormat = tk.StringVar(value=formatOptions[0])
formatDropdown = tk.OptionMenu(root, selectedFormat, *formatOptions)
formatDropdown.grid(row=7, column=0,sticky="w",padx=(10, 0))

selectedFormat.trace_add('write', onFormatChange)
#video quality
qualityLabel = tk.Label(root, text="Selected Resolution: ")
resolutions = ['','144p','480p','720p','1080p']
selectedResolution = tk.StringVar(value=resolutions[0])
qualityDropdown = tk.OptionMenu(root, selectedResolution, *resolutions)

selectedResolution.trace_add('write', onQualityChange)




#main
root.mainloop()