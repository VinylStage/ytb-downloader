import sys
import logging
from typing import Optional, List

from ytb_downloader.ui.prompts import (
    prompt_urls,
    prompt_video_same_or_each,
    prompt_height_from_list,
)
from ytb_downloader.core import video as video_core
from ytb_downloader.core import audio as audio_core
from ytb_downloader.core.convert import convert_directory_to_mp3


def _prompt_and_convert_directory() -> None:
    dir_path = input("변환할 디렉토리 경로를 입력하세요: ").strip()
    if not dir_path:
        print("경로를 입력하세요.")
        return
    recurse = input("하위 폴더까지 모두 변환할까요? (Y/n): ").strip().lower()
    recursive = recurse in ("", "y", "yes")
    bitrate = input("MP3 비트레이트를 입력하세요 (기본 320k): ").strip() or "320k"
    try:
        convert_directory_to_mp3(
            dir_path, recursive=recursive, bitrate=bitrate, overwrite=False
        )
    except Exception as e:
        logging.error(f"디렉토리 변환 실패: {e}")


def _try_suggest_heights_from_url(url: str, cookie_path: Optional[str]) -> Optional[List[int]]:
    try:
        streams, _ = video_core.extract_unique_mp4_streams(url, cookie_path=cookie_path)
        heights = [s.get("height") for s in streams if s.get("height")]
        return heights if heights else None
    except Exception:
        return None


def interactive_video_flow(cookie_path: Optional[str]) -> None:
    while True:
        print("\n[영상 모드]")
        print(" 1) 여러 URL 입력해서 받기")
        print(" 2) 재생목록 URL로 한 번에 받기 (최고 화질)")
        print(" b) 이전으로")
        sel = input("선택: ").strip().lower()
        if sel == "1":
            urls = prompt_urls()
            if not urls:
                continue
            same = prompt_video_same_or_each()
            try:
                if same:
                    suggested = _try_suggest_heights_from_url(urls[0], cookie_path)
                    height = prompt_height_from_list(suggested)
                    video_core.download_videos_same_quality(urls, height, cookie_path)
                else:
                    for idx, url in enumerate(urls, 1):
                        streams, info = video_core.extract_unique_mp4_streams(
                            url, cookie_path=cookie_path
                        )
                        title = info.get("title", "video")
                        if not streams:
                            logging.warning(
                                f"[{idx}/{len(urls)}] {title}: MP4 비디오 스트림 없음. 건너뜀"
                            )
                            continue
                        print(f"\n[{idx}/{len(urls)}] {title} - 해상도 선택")
                        for i, s in enumerate(streams, 1):
                            h = s.get("height")
                            size = s.get("filesize") or s.get("filesize_approx") or 0
                            size_mb = size / 1024 / 1024 if size else 0
                            print(f" {i}. {h}p - 약 {size_mb:.2f}MB")
                        while True:
                            choice = input("원하는 번호 입력: ").strip()
                            if not choice.isdigit() or not (
                                1 <= int(choice) <= len(streams)
                            ):
                                print("유효한 번호를 입력하세요.")
                                continue
                            break
                        chosen = streams[int(choice) - 1]
                        fmt = f"{chosen['format_id']}+bestaudio/best"
                        video_core.download_single_video_with_format(
                            url, fmt, cookie_path
                        )
            except Exception as e:
                logging.error(f"영상 다운로드 실패: {e}")
        elif sel == "2":
            pl = input("재생목록 URL: ").strip()
            if pl:
                try:
                    video_core.download_playlist_videos_best(pl, cookie_path)
                except Exception as e:
                    logging.error(f"재생목록 다운로드 실패: {e}")
        elif sel == "b":
            return
        else:
            print("메뉴에서 선택하세요.")


def interactive_audio_flow(cookie_path: Optional[str]) -> None:
    while True:
        print("\n[음성만 모드]")
        print(" 1) 여러 URL 입력해서 받기 (최고 음질 mp3)")
        print(" 2) 재생목록 URL로 한 번에 받기 (최고 음질 mp3)")
        print(" 3) 저장된 폴더의 파일들을 mp3로 변환")
        print(" b) 이전으로")
        sel = input("선택: ").strip().lower()
        if sel == "1":
            urls = prompt_urls()
            if urls:
                try:
                    audio_core.download_audios_from_urls(urls, cookie_path)
                except Exception as e:
                    logging.error(f"음성 다운로드 실패: {e}")
        elif sel == "2":
            pl = input("재생목록 URL: ").strip()
            if pl:
                try:
                    audio_core.download_playlist_audio_best(pl, cookie_path)
                except Exception as e:
                    logging.error(f"재생목록 음성 다운로드 실패: {e}")
        elif sel == "3":
            _prompt_and_convert_directory()
        elif sel == "b":
            return
        else:
            print("메뉴에서 선택하세요.")


def main() -> None:
    try:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        print("YouTube 다운로더")
        cookie_path: Optional[str] = None
        while True:
            print("\n시작 모드 선택")
            print(" 1) 영상 다운로드")
            print(" 2) 음성만 다운로드")
            print(" 3) 음성 변환 (디렉토리→MP3)")
            print(" q) 종료")
            choice = input("선택: ").strip().lower()
            if choice == "1":
                interactive_video_flow(cookie_path)
            elif choice == "2":
                interactive_audio_flow(cookie_path)
            elif choice == "3":
                _prompt_and_convert_directory()
            elif choice == "q":
                print("종료합니다.")
                break
            else:
                print("메뉴에서 선택하세요.")
    except KeyboardInterrupt:
        print("\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.error(f"예외 발생: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
