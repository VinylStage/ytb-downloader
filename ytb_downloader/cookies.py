import os
import logging
import webbrowser
from typing import Optional

COOKIE_HINT_URL = "https://www.youtube.com"
COOKIE_DOWNLOAD_INFO = (
    "브라우저가 열리면 로그인한 뒤\n"
    "크롬 확장 프로그램 'Get cookies.txt'를 사용해 쿠키 파일을 추출해주세요.\n"
    "👉 https://chrome.google.com/webstore/detail/get-cookiestxt/hdnnodkdnapdkenbkbjjjiimeonhmiog\n"
)


def prompt_login_and_get_cookie() -> Optional[str]:
    logging.warning("이 영상은 고화질 다운로드를 위해 로그인된 쿠키가 필요합니다.")
    print(COOKIE_DOWNLOAD_INFO)
    webbrowser.open(COOKIE_HINT_URL)
    cookie_path = input("로그인 후 저장한 cookies.txt의 경로를 입력하세요: ").strip()
    if not os.path.isfile(cookie_path):
        logging.error("쿠키 파일을 찾을 수 없습니다.")
        return None
    return cookie_path

