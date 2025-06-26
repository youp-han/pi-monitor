# src/utils/log_helpers.py
import os
from datetime import datetime

def save_log_to_file(host, content):
    # logs 디렉터리가 없으면 생성
    os.makedirs("logs", exist_ok=True)
    # 현재 날짜와 시간을 이용해 파일명 생성
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/monitor_{host}_{now}.log"
    # 파일에 모니터링 결과 저장
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    # 저장 완료 메시지 출력
    print(f"📄 로그 저장 완료: {filename}")
