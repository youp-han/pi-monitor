# main.py
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.config import load_server_configs  # 서버 설정을 불러오는 함수
from src.monitor import monitor_server      # 서버 모니터링 함수
from src.utils.log_helpers import save_log_to_file  # 로그 파일 저장 함수

def run_all_monitors(env_name: str):
    """
    지정한 환경(env_name)에 있는 모든 서버를 병렬로 모니터링하고,
    결과를 출력 및 파일로 저장합니다.
    """
    servers = load_server_configs(env_name)  # 환경에 맞는 서버 설정 불러오기
    with ThreadPoolExecutor(max_workers=len(servers)) as executor:  # 서버 수만큼 스레드풀 생성
        results = executor.map(monitor_server, servers)  # 각 서버에 대해 모니터링 실행
        for server, output in zip(servers, results):
            print(output)  # 결과를 콘솔에 출력
            save_log_to_file(server["host"], output)  # 결과를 파일로 저장

if __name__ == "__main__":
    # 실행 시 환경(dev, prod 등) 인자를 받으며, 없으면 기본값은 dev
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    run_all_monitors(env)