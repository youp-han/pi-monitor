# src/check/network.py
from src.ssh_utils import execute_ssh_command

def check_firewalld_status(client):
    """
    firewalld 서비스 상태를 확인하는 함수.
    """
    result = "\n[systemctl status firewalld]\n"
    out, _ = execute_ssh_command(client, "systemctl status firewalld | head -n 10")  # firewalld 서비스 상태 확인
    result += out + "\n"
    return result


def check_port_status(client, ports):
    """
    지정한 포트들이 LISTEN 상태인지 확인하는 함수.
    """
    result = "\n[포트 상태 확인]\n"
    for port in ports:
        cmd = f"ss -tan | grep {port}"  # 해당 포트의 LISTEN 상태 확인
        out, _ = execute_ssh_command(client, cmd)
        if out.strip():
            result += f"포트 {port} → LISTEN 중\n{out.strip()}\n" + "\n"
        else:
            result += f"포트 {port} → ❌ LISTEN 아님 또는 비어 있음\n" + "\n"
    return result
