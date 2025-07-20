from pytube import YouTube
import tkinter as tk

root = tk.Tk()
root.title("Youtube Video Downloader")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

urlEntry = tk.Entry(root)
urlEntry.pack()

button = tk.Button(root, text="Close", command=root.destroy)
button.pack(expand=True,fill='x')

root.mainloop()