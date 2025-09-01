import logging
from typing import List, Optional

from ytb_downloader.utils import ensure_dir
from ytb_downloader.core import ydl_opts as yopts
from ytb_downloader.core.download import download_with_cookie_retry


def download_audios_from_urls(urls: List[str], cookie_path: Optional[str]) -> None:
    ensure_dir("./music")
    opts = yopts.build_audio_opts(
        outdir="./music", cookie_path=cookie_path, playlist=False, convert_to="mp3"
    )
    logging.info(f"여러 음성(mp3, 최고 품질) 다운로드 - {len(urls)}개")
    download_with_cookie_retry(urls, opts)
    logging.info("✅ 모두 완료")


def download_playlist_audio_best(playlist_url: str, cookie_path: Optional[str]) -> None:
    ensure_dir("./music")
    opts = yopts.build_audio_opts(
        outdir="./music", cookie_path=cookie_path, playlist=True, convert_to="mp3"
    )
    logging.info("재생목록 음성 전체(mp3, 최고 품질) 다운로드 시작")
    download_with_cookie_retry([playlist_url], opts)
    logging.info("✅ 재생목록 완료")

