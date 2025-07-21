import yt_dlp as ytdlp
import tkinter as tk
from tkinter import messagebox, filedialog


#functions
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
        currentUrl.set(entry)
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

def removeVideoGui():
    videoResolutionLabel.grid_remove()
    videoResolutionDropdown.grid_remove()
    videoQualityLabel.grid_remove()
    videoQualityDropdown.grid_remove()
    videoSizeLabel.grid_remove()

def removeAudioGui():
    audioQualityLabel.grid_remove()
    audioQualityDropdown.grid_remove()

def onFormatChange(*args):
    formating = selectedFormat.get()
    if formating == 'Video':
        videoResolutionLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
        videoResolutionDropdown.grid(row=9, column=0, sticky="w", padx=(10, 0))
        videoQualityLabel.grid(row=10, column=0, sticky="w", padx=(10, 0))
        videoQualityDropdown.grid(row=11, column=0, sticky="w", padx=(10, 0))
        videoSizeLabel.grid(row=12, column=0, sticky="w", padx=(10, 0))

        removeAudioGui()
    if formating == 'Audio Only':
        audioQualityLabel.grid(row=8, column=0, sticky="w", padx=(10, 0))
        audioQualityDropdown.grid(row=9, column=0, sticky="w", padx=(10, 0))
        removeVideoGui()
    if formating == '':
        removeAudioGui()
        removeVideoGui()

def updateVideoFileSize():
    if selectedResolution.get() != '' and selectedVideoQuality.get() != '':
        url = currentUrl.get()
        resolution = selectedResolution.get()
        quality = selectedVideoQuality.get()
        reso_height = int(resolution.replace('p', ''))

        ytdlp_opts = {'quiet': True,
                      'skip_download': True,
                      'format': f'bestvideo[height<={reso_height}]+bestaudio/best[height<={reso_height}]'
                      }

        try:
            with ytdlp.YoutubeDL(ytdlp_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info['formats']

                # Find best video format matching the resolution
                best_video = None
                for format in formats:
                    if format.get('height') == reso_height and format.get('vcodec') != 'none':
                        if quality == 'best' or best_video is None:
                            best_video = format
                        elif quality == 'worst' and (best_video.get('filesize') or best_video.get('filesize_approx', 0)) > (format.get('filesize') or format.get('filesize_approx', 0)):
                            best_video = format

                # Find best audio format
                best_audio = None
                for format in formats:
                    if format.get('acodec') != 'none' and format.get('vcodec') == 'none':
                        if best_audio is None:
                            best_audio = format
                        elif quality == 'best' and (format.get('tbr') or 0) > (best_audio.get('tbr') or 0):
                            best_audio = format
                        elif quality == 'worst' and (format.get('tbr') or 0) < (best_audio.get('tbr') or 0):
                            best_audio = format

                # Calculate total size
                total_size_bytes = 0

                if best_video:
                    video_size = best_video.get('filesize') or best_video.get('filesize_approx', 0)
                    total_size_bytes += video_size

                if best_audio:
                    audio_size = best_audio.get('filesize') or best_audio.get('filesize_approx', 0)
                    total_size_bytes += audio_size

                if total_size_bytes > 0:
                    size_mb = total_size_bytes / (1024 * 1024)
                    videoSizeLabel.config(text=f"Video Size: {size_mb:.2f} MB")
                else:
                    videoSizeLabel.config(text="Video Size: Size unavailable")
        except Exception as e:
            videoSizeLabel.config(text="Video Size: Error calculating size")
            print(f"Error in updateVideoFileSize: {str(e)}")


def onVideoResolutionChange(*args):
    selected = selectedResolution.get()
    videoResolutionLabel.config(text=f'Selected Resolution: {selected}')
    updateVideoFileSize()

def onVideoQualityChange(*args):
    selected = selectedVideoQuality.get()
    videoQualityLabel.config(text=f'Selected Quality: {selected}')
    updateVideoFileSize()

def onAudioQualityChange(*args):
    selected = selectedAudioQuality.get()
    audioQualityLabel.config(text=f'Selected Audio Quality: {selected}')


def selectDownloadDirectory():
    folder = filedialog.askdirectory()
    if folder:
        folderDirectoryLabel.config(text=f"Selected Directory: {folder}")
        selectedDownloadDirectory.set(folder)

def downloadFile():
    url = currentUrl.get()
    formating = selectedFormat.get()

    folder = selectedDownloadDirectory.get()

    if not url or not formating or folder == "":
        messagebox.showerror("Error", "Please complete all required fields.")
        return

    try:
        if formating == 'Video' and selectedResolution.get() and selectedVideoQuality.get():
            reso = int(selectedResolution.get().replace("p", ""))
            quality = selectedVideoQuality.get()

            format_selector = f"{quality}[height<={reso}][vcodec!=none][acodec!=none]"

            ydl_opts = {
                'format': format_selector,
                'outtmpl': f'{folder}/%(title)s.%(ext)s',
                'noplaylist': True,
                'merge_output_format': None
            }

        elif formating == 'Audio Only' and selectedAudioQuality.get():
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
                'outtmpl': f'{folder}/%(title)s.%(ext)s',
                'noplaylist': True,
                'postprocessors': []
            }

        else:
            messagebox.showerror("Error", "Please select appropriate quality options.")
            return

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", "Download completed!")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{str(e)}")
#GUI
root = tk.Tk()
root.geometry("350x400")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.title("Youtube Video Downloader")

#url part of gui
currentUrl = tk.StringVar(value='')
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

#select format
formatLabel = tk.Label(root, text="Select Format")
formatLabel.grid(row=6, column=0,sticky="w",padx=(10, 0))
formatOptions = ['','Video','Audio Only']
selectedFormat = tk.StringVar(value=formatOptions[0])
formatDropdown = tk.OptionMenu(root, selectedFormat, *formatOptions)
formatDropdown.grid(row=7, column=0,sticky="w",padx=(10, 0))

selectedFormat.trace_add('write', onFormatChange)
#--VIDEO--
#video quality
videoResolutionLabel = tk.Label(root, text="Selected Resolution: ")
resolutions = ['','144p','480p','720p','1080p']
selectedResolution = tk.StringVar(value=resolutions[0])
videoResolutionDropdown = tk.OptionMenu(root, selectedResolution, *resolutions)

selectedResolution.trace_add('write', onVideoResolutionChange)
#video bitrate quality

videoQualityLabel = tk.Label(root, text="Selected Video Quality: ")
videoQualityOptions = ['','best','worst']
selectedVideoQuality = tk.StringVar(value=videoQualityOptions[0])
videoQualityDropdown = tk.OptionMenu(root, selectedVideoQuality, *videoQualityOptions)

selectedVideoQuality.trace_add('write',onVideoQualityChange)

#video size
videoSizeLabel = tk.Label(root, text="Video Size: ")

#----------

#--AUDIO--
#Audio Only quality
audioQualityLabel = tk.Label(root, text="Selected Audio Quality: ")
audioQualities = ['','128','192','320']
selectedAudioQuality = tk.StringVar(value=audioQualities[0])
audioQualityDropdown = tk.OptionMenu(root, selectedAudioQuality, *audioQualities)

selectedAudioQuality.trace_add('write', onAudioQualityChange)

#select folder directory
folderDirectoryLabel = tk.Label(root, text="Select Install Directory: ")
browseFoldersButton = tk.Button(root,text='BROWSE', command=lambda: selectDownloadDirectory())
selectedDownloadDirectory = tk.StringVar(value='')


folderDirectoryLabel.grid(row=13, column=0,sticky="w",padx=(10, 0))
browseFoldersButton.grid(row=14, column=0,sticky="w",padx=(10, 0))

#download
downloadButton = tk.Button(root, text='DOWNLOAD', command=lambda: downloadFile())
downloadButton.grid(row=15, column=0,sticky="w",padx=(10, 0))
#main
root.mainloop()
