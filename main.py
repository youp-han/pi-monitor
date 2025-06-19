import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.config import load_server_configs  # 서버 설정 로드 함수
from src.monitor import monitor_server, save_log_to_file  # 모니터링 및 로그 저장 함수

def run_all_monitors(env_name: str):
    """
    모든 서버에 대해 모니터링을 병렬로 실행하고 결과를 출력 및 파일로 저장.
    """
    servers = load_server_configs(env_name)  # 환경에 맞는 서버 설정 불러오기
    with ThreadPoolExecutor(max_workers=len(servers)) as executor:  # 서버 수만큼 스레드풀 생성
        results = executor.map(monitor_server, servers)  # 각 서버에 대해 모니터링 실행
        for server, output in zip(servers, results):
            print(output)  # 결과 콘솔 출력
            save_log_to_file(server["host"], output)  # 결과 파일로 저장

if __name__ == "__main__":
    # 실행 시 인자로 환경(dev, prod 등) 지정, 없으면 기본값은 dev
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    run_all_monitors(env)
