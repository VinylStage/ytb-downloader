import os
import shutil
import subprocess
import logging
from typing import Iterable

SUPPORTED_MEDIA_EXTS = {
    ".mp4",
    ".mkv",
    ".webm",
    ".m4v",
    ".mov",
    ".avi",
    ".flv",
    ".3gp",
    ".m4a",
    ".aac",
    ".opus",
    ".ogg",
    ".wav",
    ".flac",
}


def convert_directory_to_mp3(
    dir_path: str, *, recursive: bool = True, bitrate: str = "320k", overwrite: bool = False
) -> None:
    """Convert all media files under dir_path to mp3 using ffmpeg."""
    if not os.path.isdir(dir_path):
        raise ValueError("유효한 디렉토리 경로가 아닙니다.")
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg를 찾을 수 없습니다. 설치 후 다시 시도하세요.")

    def iter_files() -> Iterable[str]:
        if recursive:
            for root, _, files in os.walk(dir_path):
                for name in files:
                    yield os.path.join(root, name)
        else:
            for name in os.listdir(dir_path):
                p = os.path.join(dir_path, name)
                if os.path.isfile(p):
                    yield p

    total = converted = skipped = failed = 0
    for path in iter_files():
        base, ext = os.path.splitext(path)
        ext_low = ext.lower()
        if ext_low == ".mp3":
            skipped += 1
            continue
        if ext_low not in SUPPORTED_MEDIA_EXTS:
            continue
        total += 1
        out_path = base + ".mp3"
        if os.path.exists(out_path) and not overwrite:
            logging.info(f"이미 mp3가 존재하여 건너뜀: {out_path}")
            skipped += 1
            continue
        cmd = [
            "ffmpeg",
            "-y" if overwrite else "-n",
            "-i",
            path,
            "-vn",
            "-acodec",
            "libmp3lame",
            "-b:a",
            bitrate,
            out_path,
        ]
        logging.info(f"변환: {path} -> {out_path}")
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                converted += 1
            else:
                failed += 1
                logging.error(
                    f"변환 실패: {path}\n{proc.stderr.decode(errors='ignore')}"
                )
        except Exception as e:
            failed += 1
            logging.error(f"변환 예외: {path} - {e}")

    logging.info(
        f"변환 요약 - 대상:{total}, 성공:{converted}, 건너뜀:{skipped}, 실패:{failed}"
    )

