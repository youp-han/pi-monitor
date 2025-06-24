# src/check/network.py
from src.ssh_utils import execute_ssh_command

def check_firewalld_status(client):
    result = "\n[systemctl status firewalld]\n"
    out, _ = execute_ssh_command(client, "systemctl status firewalld | head -n 10")
    result += out
    return result


def check_port_status(client, ports):
    result = "\n[포트 상태 확인]\n"
    for port in ports:
        cmd = f"ss -tan | grep {port}"
        out, _ = execute_ssh_command(client, cmd)
        if out.strip():
            result += f"포트 {port} → LISTEN 중\n{out.strip()}\n"
        else:
            result += f"포트 {port} → ❌ LISTEN 아님 또는 비어 있음\n"
    return result
