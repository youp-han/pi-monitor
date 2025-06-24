# src/utils/log_helpers.py
import os
from datetime import datetime

def save_log_to_file(host, content):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/monitor_{host}_{now}.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 로그 저장 완료: {filename}")
