# src/check/apache.py
import os
from datetime import datetime, timedelta
from src.ssh_utils import execute_ssh_command
from src.check.network import check_port_status

def check_apache_services(client, s_where, s_envFile):
    """
    Apache 서버의 주요 서비스 상태와 로그, 포트 상태를 점검하는 함수.
    """
    result = "\n[Apache 서비스 확인]\n"
    result += "\n[ps -ef | grep httpd]\n"
    out, _ = execute_ssh_command(client, "ps -ef | grep httpd")  # httpd 프로세스 확인
    result += out + "\n"

    result += "\n[systemctl status httpd]\n"
    out, _ = execute_ssh_command(client, "systemctl status httpd | head -n 10")  # httpd 서비스 상태 확인
    result += out + "\n"

    result += "\n[Apache 로그 에러 확인]\n"
    result += check_apache_log(client, s_where, s_envFile)  # Apache 에러 로그 확인
    result += check_port_status(client, [80, 443])  # 80, 443 포트 상태 확인
    return result + "\n"

def check_apache_log(client, s_where, s_envFile):
    """
    Apache 에러 로그 파일에서 에러 라인 수와 내용을 추출하는 함수.
    오늘 또는 어제의 로그 파일을 우선적으로 확인.
    """
    today = datetime.today().strftime("%Y%m%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
    log_path_today = f"/appweb/{s_where}/logs/{s_envFile}_error.log.{today}"
    log_path_yesterday = f"/appweb/{s_where}/logs/{s_envFile}_error.log.{yesterday}"

    # 오늘 로그 파일이 있으면 사용, 없으면 어제 로그 파일 사용
    check_cmd = f"""
if [ -f \"{log_path_today}\" ]; then
    echo \"{log_path_today}\"
elif [ -f \"{log_path_yesterday}\" ]; then
    echo \"{log_path_yesterday}\"
else
    echo "NONE"
fi
"""
    out, _ = execute_ssh_command(client, check_cmd)
    log_path = out.strip()

    if log_path == "NONE":
        return "Apache 로그 파일 없음 또는 찾을 수 없음\n" + "\n"

    # 에러 라인 추출
    cmd_lines = f"sudo grep -i 'error' {log_path}"
    error_lines, _ = execute_ssh_command(client, cmd_lines)

    # 에러 라인 수 카운트
    cmd_count = f"grep -i 'error' {log_path} | wc -l"
    count_out, _ = execute_ssh_command(client, cmd_count)
    filename = os.path.basename(log_path)

    result = f"[Apache Log Errors - {filename}]\n에러 라인 수: {count_out.strip()}" + "\n"
    result += f"\n[에러 라인 내용]\n{error_lines.strip()}\n" if error_lines.strip() else "\n(에러 내용 없음)\n"
    return result