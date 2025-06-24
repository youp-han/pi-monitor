def parse_vmstat_for_high_cpu(vmstat_output):
    """
    vmstat 명령 결과에서 CPU idle 값이 50 미만인 경우가 있는지 확인.
    CPU 사용률이 높은 상태를 감지.
    """
    lines = vmstat_output.strip().splitlines()
    data_lines = lines[2:]
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 15:
            idle = int(parts[14])
            if idle < 50:
                return True
    return False
