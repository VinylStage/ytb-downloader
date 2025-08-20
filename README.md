
# YouTube Video Downloader

A nerdy YouTube Video Downloader, built just for me (but you can use it too).


## Description

An easy and nerd-approved way to download high-resolution YouTube videos from your terminal.


## Getting Started

### Dependencies

- macOS
- Python 3.13

### Installation

Clone this repository to your computer:

```bash
git clone git@github.com:VinylStage/ytb-downloader.git
cd ytb-downloader
```

### Running the Program

1. Set up your Python virtual environment (using Poetry):

```bash
poetry shell
```

2. Install dependencies:

```bash
poetry install
```

3. Run the script:

```bash
python3 downloader.py
```

4. Paste the YouTube link you want to download when prompted.

```bash
# example
Enter the YouTube video URL: https://www.youtube.com/shorts/MJP92jpeyyY
2025-08-20 21:41:59,265 - INFO - User provided URL: https://www.youtube.com/shorts/MJP92jpeyyY
2025-08-20 21:41:59,265 - DEBUG - Fetching video info for URL: https://www.youtube.com/shorts/MJP92jpeyyY
WARNING: [youtube] MJP92jpeyyY: Some web client https formats have been skipped as they are missing a url. YouTube is forcing SABR streaming for this client. See  https://github.com/yt-dlp/yt-dlp/issues/12482  for more details
```

*You can safely ignore the warning above!*

5. Select the video quality you want to download and wait for the magic to happen.

```bash
# example
2025-08-20 21:42:07,822 - DEBUG - Successfully extracted video info for 'juan.'
2025-08-20 21:42:07,822 - DEBUG - Found 19 available formats.
2025-08-20 21:42:07,822 - DEBUG - Found 6 unique displayable video streams.
2025-08-20 21:42:07,822 - INFO -
Available resolutions:
2025-08-20 21:42:07,822 - INFO - 1. 1080p (video only)
2025-08-20 21:42:07,823 - INFO - 2. 720p (video only)
2025-08-20 21:42:07,823 - INFO - 3. 480p (video only)
2025-08-20 21:42:07,823 - INFO - 4. 360p (video only)
2025-08-20 21:42:07,823 - INFO - 5. 240p (video only)
2025-08-20 21:42:07,823 - INFO - 6. 144p (video only)

Enter the number of the resolution you want to download: 1
2025-08-20 21:42:11,595 - INFO - User selected resolution: 1080p (Format ID: 270)
2025-08-20 21:42:11,595 - DEBUG - Download path set to: ./videos
2025-08-20 21:42:11,595 - DEBUG - Using yt-dlp download options: {'format': '270+bestaudio/best', 'outtmpl': './videos/%(title)s-%(height)sp.%(ext)s', 'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}], 'progress_hooks': [<function download_video.<locals>.<lambda> at 0x102d6fec0>]}
2025-08-20 21:42:11,595 - INFO - Downloading 'juan.' in 1080p...
[youtube] Extracting URL: https://www.youtube.com/shorts/MJP92jpeyyY
[youtube] MJP92jpeyyY: Downloading webpage
[youtube] MJP92jpeyyY: Downloading tv client config
[youtube] MJP92jpeyyY: Downloading player 093288cd-main
[youtube] MJP92jpeyyY: Downloading tv player API JSON
[youtube] MJP92jpeyyY: Downloading ios player API JSON
WARNING: [youtube] MJP92jpeyyY: Some web client https formats have been skipped as they are missing a url. YouTube is forcing SABR streaming for this client. See  https://github.com/yt-dlp/yt-dlp/issues/12482  for more details
[youtube] MJP92jpeyyY: Downloading m3u8 information
[info] Testing format 270
[info] Testing format 234
[info] MJP92jpeyyY: Downloading 1 format(s): 270+234
[hlsnative] Downloading m3u8 manifest
[hlsnative] Total fragments: 3
[download] Destination: ./videos/juan.-1080p.f270.mp4
[download] 100% of  911.73KiB in 00:00:00 at 4.61MiB/s2025-08-20 21:42:16,916 - DEBUG - yt-dlp hook: finished

[hlsnative] Downloading m3u8 manifest
[hlsnative] Total fragments: 3
[download] Destination: ./videos/juan.-1080p.f234.mp4
[download] 100% of  251.20KiB in 00:00:00 at 1.59MiB/s2025-08-20 21:42:17,338 - DEBUG - yt-dlp hook: finished

[Merger] Merging formats into "./videos/juan.-1080p.mp4"
Deleting original file ./videos/juan.-1080p.f270.mp4 (pass -k to keep)
Deleting original file ./videos/juan.-1080p.f234.mp4 (pass -k to keep)
[VideoConvertor] Not converting media file "./videos/juan.-1080p.mp4"; already is in target format mp4
2025-08-20 21:42:17,610 - INFO - Download completed successfully!
2025-08-20 21:42:17,610 - INFO - Video saved to folder: ./videos
```

6. Check your downloaded videos:

```bash
ls -al videos
```

- example

```bash
(ytb-downloader-py3.13) ☁  ytb-downloader [main] ⚡  ls -al videos
total 2216
drwxr-xr-x@  3 vinyl  staff       96 Aug 20 21:42 .
drwxr-xr-x@ 11 vinyl  staff      352 Aug 20 21:44 ..
-rw-r--r--@  1 vinyl  staff  1133451 Jul  9 16:29 juan.-1080p.mp4
```

7. Enjoy your happy nerd time!

## Help

Any advice for common problems or issues:

```
No command to run if the program contains helper info.
```


## Author

[Vinyl Stage](https://link.vinylims.com)



## Version History

* 0.1.0
    * Initial Release
