# src/check/apache.py
import os
from datetime import datetime, timedelta
from src.ssh_utils import execute_ssh_command
from src.check.network import check_port_status

def check_apache_services(client, s_where, s_envFile):
    result = "\n[Apache 서비스 확인]\n"
    result += "\n[ps -ef | grep httpd]\n"
    out, _ = execute_ssh_command(client, "ps -ef | grep httpd")
    result += out

    result += "\n[systemctl status httpd]\n"
    out, _ = execute_ssh_command(client, "systemctl status httpd | head -n 10")
    result += out

    result += "\n[Apache 로그 에러 확인]\n"
    result += check_apache_log(client, s_where, s_envFile)
    result += check_port_status(client, [80, 443])
    return result

def check_apache_log(client, s_where, s_envFile):
    today = datetime.today().strftime("%Y%m%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
    log_path_today = f"/appweb/{s_where}/logs/{s_envFile}_error.log.{today}"
    log_path_yesterday = f"/appweb/{s_where}/logs/{s_envFile}_error.log.{yesterday}"

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
        return "Apache 로그 파일 없음 또는 찾을 수 없음\n"

    cmd_lines = f"sudo grep -i 'error' {log_path}"
    error_lines, _ = execute_ssh_command(client, cmd_lines)

    cmd_count = f"grep -i 'error' {log_path} | wc -l"
    count_out, _ = execute_ssh_command(client, cmd_count)
    filename = os.path.basename(log_path)

    result = f"[Apache Log Errors - {filename}]\n에러 라인 수: {count_out.strip()}"
    result += f"\n[에러 라인 내용]\n{error_lines.strip()}\n" if error_lines.strip() else "\n(에러 내용 없음)\n"
    return result