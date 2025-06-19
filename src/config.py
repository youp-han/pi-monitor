import os
import json
from dotenv import load_dotenv

# .env 파일의 환경변수들을 로드
load_dotenv()

def load_server_configs(env: str = "dev"):
    """
    주어진 환경(env)에 맞는 서버 설정 파일을 로드하고,
    각 서버에 환경변수에서 불러온 관리자 계정 정보를 추가하여 반환합니다.
    """
    # 환경에 따라 서버 설정 파일명 결정 (예: servers.dev.json)
    filename = f"servers.{env}.json"
    # 파일이 존재하지 않으면 예외 발생
    if not os.path.exists(filename):
        raise FileNotFoundError(f"서버 설정 파일 '{filename}'이 존재하지 않습니다.")
    
    # 서버 설정 파일을 읽어서 JSON 파싱
    with open(filename, "r", encoding="utf-8") as f:
        servers = json.load(f)

    # 각 서버에 환경변수에서 불러온 관리자 계정 정보 추가
    for s in servers:
        s["user"] = os.getenv("ADMIN_USER")
        s["pass"] = os.getenv("ADMIN_PASS")
    return servers
