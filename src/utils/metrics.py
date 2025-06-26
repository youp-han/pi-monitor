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
    return False  # 모든 라인에서 idle 값이 50 이상이면 False 반환
