# YouTube Video Downloader

A simple, user-friendly desktop application built with Python and Tkinter to download YouTube videos and audio. It uses the powerful `yt-dlp` library for media extraction and downloading.

## Features

- **Download Formats**: Choose between full video (with audio) or audio-only downloads.
- **Resolution Options**: Select from multiple resolutions (480p, 720p, 1080p).
- **Quality Control**: Specify 'best' or 'worst' quality for video and audio bitrates.
- **Real-time Info**: Fetches video title, duration, and estimated file size before downloading.
- **Custom Download Path**: Easily select your preferred download directory via a folder browser.
- **Simple GUI**: Clean and intuitive interface.

## Prerequisites

- Python 3.x
- `yt-dlp` library

## Installation

1. **Clone the repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd youtube-downloader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python GUI.py
   ```
2. **Enter the YouTube URL**: Paste the link into the input field and click **Enter**.
3. **Select Format**: Choose "Video" or "Audio Only" from the dropdown.
4. **Choose Quality**: Select your desired resolution and bitrate quality.
5. **Set Download Path**: Click **BROWSE** to choose where to save your file.
6. **Download**: Click the **DOWNLOAD** button to start the process.

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): A feature-rich command-line audio/video downloader.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): Python's built-in GUI toolkit.

## License

This project is open-source and available under the [MIT License](LICENSE).