# src/check/system.py
from src.ssh_utils import execute_ssh_command
from src.utils.metrics import parse_vmstat_for_high_cpu  # 변경된 위치


def check_system_health(client):
    """
    시스템의 주요 자원 상태를 점검하는 함수.
    vmstat로 CPU/메모리 상태를 확인하고, CPU 사용률이 높으면 top 명령도 실행.
    디스크 사용량도 함께 확인하여 결과 문자열로 반환.
    """
    result = "[vmstat 1 10]\n"
    vmstat_out, _ = execute_ssh_command(client, "vmstat 1 10")  # vmstat 명령 실행
    result += vmstat_out  + "\n"

    # CPU idle 값이 낮으면 top 명령 실행 결과 추가
    if parse_vmstat_for_high_cpu(vmstat_out):
        result += "\n[High CPU detected! top 실행]\n"
        top_out, _ = execute_ssh_command(client, "top -b -n 1 | head -n 20")
        result += top_out + "\n"

    result += "\n[df -k]\n"
    df_out, _ = execute_ssh_command(client, "df -h")  # 디스크 사용량 확인
    result += df_out + "\n"
    return result


def parse_vmstat_for_high_cpu(vmstat_output):
    """
    vmstat 명령 결과에서 CPU idle 값이 50 미만인 경우가 있는지 확인.
    CPU 사용률이 높은 상태를 감지하는 함수.
    """
    lines = vmstat_output.strip().splitlines()
    data_lines = lines[2:]  # 헤더 이후 데이터 라인만 추출
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 15:
            idle = int(parts[14])  # 15번째 컬럼이 idle 값
            if idle < 50:
                return True  # idle 값이 50 미만이면 True 반환
    return False  # 모든 라인에서 idle 값이 50 이상이면
