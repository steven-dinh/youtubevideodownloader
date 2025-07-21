import yt_dlp as ytdlp
import tkinter as tk
from tkinter import messagebox, filedialog


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

def onFormatChange(*args):
    formating = selectedFormat.get()
    if formating == 'Video':
        videoQualityLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
        videoQualityDropdown.grid(row=9, column=0, sticky="w", padx=(10, 0))
    elif formating == 'Audio':
        audioQualityLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
        audioQualityDropdown.grid(row=9, column=0, sticky="w", padx=(10, 0))
    else:
        videoQualityLabel.grid_remove()
        videoQualityDropdown.grid_remove()
        audioQualityLabel.grid_remove()
        audioQualityDropdown.grid_remove()

def onVideoQualityChange(*args):
    selected = selectedResolution.get()
    videoQualityLabel.config(text=f'Selected Resolution: {selected}')

def onAudioQualityChange(*args):
    selected = selectedAudioQuality.get()
    audioQualityLabel.config(text=f'Selected Audio Quality: {selected}')


def selectDownloadDirectory():
    folder = filedialog.askdirectory()
    if folder:
        folderDirectoryLabel.config(text=f"Selected Directory: {folder}")

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
videoQualityLabel = tk.Label(root, text="Selected Resolution: ")
resolutions = ['','144p','480p','720p','1080p']
selectedResolution = tk.StringVar(value=resolutions[0])
videoQualityDropdown = tk.OptionMenu(root, selectedResolution, *resolutions)

selectedResolution.trace_add('write', onVideoQualityChange)

#mp3 quality
audioQualityLabel = tk.Label(root, text="Selected Audio Quality: ")
audioQualities = ['','128','192','320']
selectedAudioQuality = tk.StringVar(value=audioQualities[0])
audioQualityDropdown = tk.OptionMenu(root, selectedAudioQuality, *audioQualities)

selectedAudioQuality.trace_add('write', onAudioQualityChange)

#select folder directory
folderDirectoryLabel = tk.Label(root, text="Select Install Directory: ")
browseFoldersButton = tk.Button(root,text='BROWSE', command=lambda: selectDownloadDirectory())

folderDirectoryLabel.grid(row=12, column=0,sticky="w",padx=(10, 0))
browseFoldersButton.grid(row=13, column=0,sticky="w",padx=(10, 0))
#main
root.mainloop()