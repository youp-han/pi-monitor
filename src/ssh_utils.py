import paramiko  # SSH 연결을 위한 라이브러리

def execute_ssh_command(client, command):
    """
    주어진 SSH client를 사용하여 원격 서버에서 명령어를 실행하고,
    표준 출력과 표준 에러를 문자열로 반환합니다.
    """
    # 명령어 실행 (stdin, stdout, stderr 반환)
    try:
        stdin, stdout, stderr = client.exec_command(command)
        # 표준 출력과 표준 에러를 읽어서 디코딩 후 반환
        return stdout.read().decode(), stderr.read().decode()
    except Exception as e:
        # 예외 발생 시 빈 문자열과 에러 메시지 반환
        return "", str(e)

