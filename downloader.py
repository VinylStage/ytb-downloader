import os
import yt_dlp
import logging
import webbrowser

COOKIE_HINT_URL = "https://www.youtube.com"
COOKIE_DOWNLOAD_INFO = (
    "브라우저가 열리면 로그인한 뒤\n"
    "크롬 확장 프로그램 'Get cookies.txt'를 사용해 쿠키 파일을 추출해주세요.\n"
    "👉 https://chrome.google.com/webstore/detail/get-cookiestxt/hdnnodkdnapdkenbkbjjjiimeonhmiog\n"
)

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def prompt_login_and_get_cookie():
    logging.warning("이 영상은 고화질 다운로드를 위해 로그인된 쿠키가 필요합니다.")
    print(COOKIE_DOWNLOAD_INFO)
    webbrowser.open(COOKIE_HINT_URL)
    cookie_path = input("로그인 후 저장한 cookies.txt의 경로를 입력하세요: ").strip()
    if not os.path.isfile(cookie_path):
        logging.error("쿠키 파일을 찾을 수 없습니다.")
        return None
    return cookie_path


def download_video(cookie_path=None):
    try:
        video_url = input("Enter the YouTube video URL: ").strip()
        if not video_url:
            logging.error("URL이 입력되지 않았습니다.")
            return

        logging.info(f"User provided URL: {video_url}")

        # 추출용 옵션 (cookie 포함 X)
        info_opts = {
            "quiet": True,
            "extractor_args": {"youtube": ["player_client=android"]},
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
            },
        }

        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])
            title = info.get("title", "video")

        # 고유 해상도 필터링
        video_streams = [
            f for f in formats if f.get("vcodec") != "none" and f.get("ext") == "mp4"
        ]
        seen, unique_streams = set(), []
        for f in sorted(video_streams, key=lambda f: f.get("height", 0), reverse=True):
            h = f.get("height")
            if h and h not in seen:
                seen.add(h)
                unique_streams.append(f)

        if not unique_streams:
            logging.warning("다운로드 가능한 MP4 영상 포맷이 없습니다.")
            return

        print("\n[해상도 선택]")
        for i, stream in enumerate(unique_streams):
            height = stream.get("height")
            size = stream.get("filesize") or stream.get("filesize_approx") or 0
            print(f"{i+1}. {height}p - 약 {size / 1024 / 1024:.2f}MB")

        choice = int(input("원하는 번호 입력: "))
        selected = unique_streams[choice - 1]
        format_id = selected["format_id"]
        height = selected["height"]

        # 다운로드 옵션 구성
        download_path = "./videos"
        os.makedirs(download_path, exist_ok=True)

        ydl_opts = {
            "format": f"{format_id}+bestaudio/best",
            "outtmpl": os.path.join(download_path, "%(title)s-%(height)sp.%(ext)s"),
            "merge_output_format": "mp4",
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "extractor_args": info_opts["extractor_args"],
            "http_headers": info_opts["http_headers"],
        }

        # ✅ 쿠키 사용 시 적용
        if cookie_path:
            ydl_opts["cookiefile"] = cookie_path

        logging.info(f"Downloading '{title}' in {height}p...")

        # 다운로드 실행
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video_url])
            except yt_dlp.utils.DownloadError as e:
                if "403" in str(e):
                    logging.warning("❗403 오류 발생: 로그인된 쿠키가 필요합니다.")
                    new_cookie = prompt_login_and_get_cookie()
                    if new_cookie:
                        download_video(cookie_path=new_cookie)
                    return
                else:
                    raise e

        logging.info("✅ 다운로드 완료!")

    except KeyboardInterrupt:
        logging.warning("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.error(f"예외 발생: {e}", exc_info=True)


if __name__ == "__main__":
    download_video()
