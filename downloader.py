import os
import yt_dlp
import logging

# 1. Configure logging
# Set the default logging level to DEBUG. You can change this to logging.INFO for less verbose output.
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_video():
    """
    Main function to handle the video download process.
    """
    try:
        # 2. Get YouTube URL from user
        video_url = input("Enter the YouTube video URL: ")
        logging.info(f"User provided URL: {video_url}")

        # 3. Get video info using yt-dlp
        logging.debug(f"Fetching video info for URL: {video_url}")
        ydl_opts_info = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])
        
        video_title = info_dict.get('title', 'video')
        logging.debug(f"Successfully extracted video info for '{video_title}'")
        logging.debug(f"Found {len(formats)} available formats.")

        # 4. Filter for unique video streams and sort by resolution
        video_streams = [f for f in formats if f.get('vcodec') != 'none' and f.get('ext') == 'mp4']
        
        # Remove duplicates based on resolution, keeping the best quality version
        seen_resolutions = set()
        unique_streams = []
        for stream in sorted(video_streams, key=lambda f: f.get('height', 0), reverse=True):
            resolution = stream.get('height')
            if resolution and resolution not in seen_resolutions:
                unique_streams.append(stream)
                seen_resolutions.add(resolution)

        if not unique_streams:
            logging.warning("No downloadable MP4 video streams found.")
            return
            
        logging.debug(f"Found {len(unique_streams)} unique displayable video streams.")

        # 5. Display available resolutions to the user
        logging.info("\nAvailable resolutions:")
        for i, stream in enumerate(unique_streams):
            resolution = f"{stream.get('height')}p"
            note = "video only" if stream.get('acodec') == 'none' else "video+audio"
            filesize_mb = stream.get('filesize') or stream.get('filesize_approx')
            
            display_line = f"{i+1}. {resolution} ({note})"
            if filesize_mb:
                filesize_str = f"{filesize_mb / 1024 / 1024:.2f} MB"
                display_line += f" - {filesize_str}"
            
            logging.info(display_line)

        # 6. Get user's choice
        choice = int(input("\nEnter the number of the resolution you want to download: "))
        selected_stream = unique_streams[choice - 1]
        video_format_id = selected_stream['format_id']
        resolution_str = f"{selected_stream.get('height')}p"
        logging.info(f"User selected resolution: {resolution_str} (Format ID: {video_format_id})")

        # 7. Set download path and options
        download_path = os.path.expanduser("./videos")
        logging.debug(f"Download path set to: {download_path}")

        # Set output template with resolution suffix
        output_template = os.path.join(download_path, '%(title)s-%(height)sp.%(ext)s')

        ydl_opts_download = {
            'format': f'{video_format_id}+bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'progress_hooks': [lambda d: logging.debug(f"yt-dlp hook: {d['status']}") if d['status'] in ['finished', 'error'] else None],
        }
        logging.debug(f"Using yt-dlp download options: {ydl_opts_download}")

        # 8. Download the video
        logging.info(f"Downloading '{video_title}' in {resolution_str}...")
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([video_url])

        logging.info("Download completed successfully!")
        logging.info(f"Video saved to folder: {download_path}")

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"A download error occurred: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    download_video()
