# src/check/system.py
from src.ssh_utils import execute_ssh_command
from src.utils.metrics import parse_vmstat_for_high_cpu  # 변경된 위치


def check_system_health(client):
    result = "[vmstat 1 10]\n"
    vmstat_out, _ = execute_ssh_command(client, "vmstat 1 10")
    result += vmstat_out

    if parse_vmstat_for_high_cpu(vmstat_out):
        result += "\n[High CPU detected! top 실행]\n"
        top_out, _ = execute_ssh_command(client, "top -b -n 1 | head -n 20")
        result += top_out

    result += "\n[df -k]\n"
    df_out, _ = execute_ssh_command(client, "df -k")
    result += df_out
    return result


def parse_vmstat_for_high_cpu(vmstat_output):
    lines = vmstat_output.strip().splitlines()
    data_lines = lines[2:]
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 15:
            idle = int(parts[14])
            if idle < 50:
                return True
    return False
