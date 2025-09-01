
# YouTube Video Downloader

CLI YouTube downloader with multi-URL, playlist, and audio conversion.


## Features

- Video downloads
  - Multiple URLs at once
  - Choose same quality for all or pick per-video
  - Playlist downloads at best quality
- Audio-only downloads
  - Multiple URLs or entire playlist
  - Always saved as MP3 (best quality) under `music/`
- Audio conversion
  - Convert an existing directory of media files to MP3
  - Recursive option and customizable bitrate (default 320k)
- Reliability
  - Desktop User-Agent for playlists
  - If 403 occurs, prompts once for cookies.txt and retries


## Requirements

- Python 3.13
- ffmpeg (for merging video and extracting audio)
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt update && sudo apt install ffmpeg -y`


## Installation

Clone the repository and install dependencies via Poetry:

```bash
git clone git@github.com:VinylStage/ytb-downloader.git
cd ytb-downloader
poetry install
```


## Usage

Run the app:

```bash
poetry run python main.py
# or
poetry run python downloader.py
```

Start menu options:

1\) Video download
<br>
2\) Audio-only download
<br>
3\) Audio conversion (directory → MP3)
<br>
q\) Quit

Video mode:

- Multiple URLs: paste one per line; finish with empty line or `done`.
- Same quality for all: pick a target resolution (e.g., 1080p). Each video gets the best format at or below that height.
- Per-video choice: see available MP4 heights and pick per item.
- Playlists: paste a playlist URL to download all videos at best quality. Saved to `videos/<playlist_title>/`.

Audio-only mode:

- Multiple URLs: downloads best audio and extracts to MP3. Saved to `music/`.
- Playlist: downloads all items to MP3. Saved to `music/<playlist_title>/`.

Audio conversion mode:

- Select a directory, choose recursive or not, and bitrate (e.g., `320k`).
- Converts supported media files in-place to `.mp3` (existing `.mp3` are skipped).


## Cookies (optional)

Some content (age/region-restricted, unlisted) may require login. If a 403 error occurs during download, the app will prompt for a `cookies.txt` path and retry once.

- Export cookies with the “Get cookies.txt” browser extension and supply the file path when prompted.


## Output

- Videos: `videos/` (playlists under `videos/<playlist_title>/`)
- Audios: `music/` (playlists under `music/<playlist_title>/`)


## Author

[Vinyl Stage](https://link.vinylims.com)


## Version History

- 0.2.0
  - Modularized codebase; added multi-URL video/audio, playlist support, and directory→MP3 conversion
- 0.1.0
  - Initial release
