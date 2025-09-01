import logging
from typing import List, Optional, Tuple

import yt_dlp

from ytb_downloader.utils import ensure_dir
from ytb_downloader.core import ydl_opts as yopts
from ytb_downloader.core.download import download_with_cookie_retry


def extract_unique_mp4_streams(
    video_url: str, cookie_path: Optional[str] = None
) -> Tuple[List[dict], dict]:
    """Return list of unique-height MP4 video streams and original info."""
    info_opts = yopts.build_info_opts(for_playlist=False)
    if cookie_path:
        info_opts["cookiefile"] = cookie_path
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get("formats", [])
    video_streams = [
        f for f in formats if f.get("vcodec") != "none" and f.get("ext") == "mp4"
    ]
    seen, unique_streams = set(), []
    for f in sorted(video_streams, key=lambda f: f.get("height", 0), reverse=True):
        h = f.get("height")
        if h and h not in seen:
            seen.add(h)
            unique_streams.append(f)
    return unique_streams, info


def format_selector_for_height(height: int) -> str:
    return f"bestvideo[ext=mp4][height<={height}]+bestaudio/best"


def download_single_video_with_format(
    url: str, fmt: str, cookie_path: Optional[str]
) -> None:
    ensure_dir("./videos")
    opts = yopts.build_video_opts(
        fmt=fmt, outdir="./videos", cookie_path=cookie_path, playlist=False
    )
    logging.info(f"영상 다운로드: {url}")
    download_with_cookie_retry([url], opts)
    logging.info("✅ 완료")


def download_videos_same_quality(
    urls: List[str], height: int, cookie_path: Optional[str]
) -> None:
    fmt = format_selector_for_height(height)
    ensure_dir("./videos")
    opts = yopts.build_video_opts(
        fmt=fmt, outdir="./videos", cookie_path=cookie_path, playlist=False
    )
    logging.info(f"여러 영상 동일 화질({height}p 이하) 다운로드 - {len(urls)}개")
    download_with_cookie_retry(urls, opts)
    logging.info("✅ 모두 완료")


def download_playlist_videos_best(
    playlist_url: str, cookie_path: Optional[str]
) -> None:
    ensure_dir("./videos")
    fmt = "bestvideo+bestaudio/best"
    opts = yopts.build_video_opts(
        fmt=fmt, outdir="./videos", cookie_path=cookie_path, playlist=True
    )
    logging.info("재생목록 전체(최고 화질) 다운로드 시작")
    download_with_cookie_retry([playlist_url], opts)
    logging.info("✅ 재생목록 완료")

