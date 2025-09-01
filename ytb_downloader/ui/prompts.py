from typing import List, Optional


def prompt_urls() -> List[str]:
    print("\nURL을 한 줄에 하나씩 입력하세요. 'done' 또는 빈 줄로 종료.")
    urls: List[str] = []
    while True:
        u = input("URL: ").strip()
        if u == "" or u.lower() == "done":
            break
        urls.append(u)
    return urls


def prompt_video_same_or_each() -> bool:
    """True: 동일화질, False: 각각선택"""
    choice = input("모든 영상 동일한 화질로 받을까요? (Y/n): ").strip().lower()
    return choice in ("", "y", "yes")


def prompt_height_from_list(suggested: Optional[List[int]] = None) -> int:
    base = [2160, 1440, 1080, 720, 480, 360, 240, 144]
    candidates = suggested or base
    print("\n[해상도 선택 - 지원 해상도 이하로 최적 선택]")
    for i, h in enumerate(candidates, 1):
        print(f" {i}. {h}p")
    while True:
        ans = input("번호 선택: ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(candidates):
            return candidates[int(ans) - 1]
        print("유효한 번호를 입력하세요.")

