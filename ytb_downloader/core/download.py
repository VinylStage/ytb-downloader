import logging
from typing import List, Dict

import yt_dlp

from ytb_downloader.cookies import prompt_login_and_get_cookie


def download_with_cookie_retry(urls: List[str], ydl_opts: Dict) -> None:
    """Download list of URLs with yt-dlp, retrying once after cookie prompt on 403.

    Raises yt_dlp.utils.DownloadError on final failure.
    """
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download(urls)
            if isinstance(ret, int) and ret > 0:
                raise yt_dlp.utils.DownloadError(f"yt-dlp reported {ret} error(s)")
    except yt_dlp.utils.DownloadError as e:
        if "403" in str(e):
            logging.warning("❗403 오류: 로그인 쿠키가 필요합니다. 쿠키 입력을 요청합니다.")
            new_cookie = prompt_login_and_get_cookie()
            if new_cookie:
                ydl_opts_retry = dict(ydl_opts)
                ydl_opts_retry["cookiefile"] = new_cookie
                with yt_dlp.YoutubeDL(ydl_opts_retry) as ydl:
                    ret = ydl.download(urls)
                    if isinstance(ret, int) and ret > 0:
                        raise yt_dlp.utils.DownloadError(
                            f"yt-dlp reported {ret} error(s) after retry"
                        )
            else:
                raise
        else:
            raise

