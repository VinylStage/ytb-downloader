from typing import Optional


def _ua_desktop() -> str:
    return (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )


def _ua_mobile() -> str:
    return (
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.91 Mobile Safari/537.36"
    )


def build_info_opts(*, for_playlist: bool = False) -> dict:
    """Build common yt-dlp info options.

    - Desktop UA for playlist extraction (youtube:tab) for stability
    - Android player client hint for single videos sometimes yields better results
    """
    http_headers = {"User-Agent": _ua_desktop() if for_playlist else _ua_mobile()}
    opts: dict = {"quiet": True, "http_headers": http_headers}
    if not for_playlist:
        opts["extractor_args"] = {"youtube": ["player_client=android"]}
    return opts


def build_video_opts(
    fmt: str,
    outdir: str,
    cookie_path: Optional[str] = None,
    playlist: bool = False,
) -> dict:
    info_opts = build_info_opts(for_playlist=playlist)
    import os

    outtmpl = os.path.join(
        outdir,
        ("%(playlist_title)s/" if playlist else "") + "%(title)s-%(height)sp.%(ext)s",
    )
    opts = {
        "format": fmt,
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "http_headers": info_opts["http_headers"],
        "noplaylist": not playlist,
        "ignoreerrors": True,
    }
    if "extractor_args" in info_opts:
        opts["extractor_args"] = info_opts["extractor_args"]
    if cookie_path:
        opts["cookiefile"] = cookie_path
    return opts


def build_audio_opts(
    outdir: str,
    cookie_path: Optional[str] = None,
    playlist: bool = False,
    convert_to: str = "mp3",
) -> dict:
    info_opts = build_info_opts(for_playlist=playlist)
    import os

    outtmpl = os.path.join(
        outdir, ("%(playlist_title)s/" if playlist else "") + "%(title)s.%(ext)s"
    )
    opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "http_headers": info_opts["http_headers"],
        "noplaylist": not playlist,
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": convert_to,
                "preferredquality": "0",
            }
        ],
        "keepvideo": False,
    }
    if "extractor_args" in info_opts:
        opts["extractor_args"] = info_opts["extractor_args"]
    if cookie_path:
        opts["cookiefile"] = cookie_path
    return opts

