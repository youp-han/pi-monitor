# main.py
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.config import load_server_configs
from src.monitor import monitor_server
from src.utils.log_helpers import save_log_to_file

def run_all_monitors(env_name: str):
    servers = load_server_configs(env_name)
    with ThreadPoolExecutor(max_workers=len(servers)) as executor:
        results = executor.map(monitor_server, servers)
        for server, output in zip(servers, results):
            print(output)
            save_log_to_file(server["host"], output)

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "dev"
    run_all_monitors(env)