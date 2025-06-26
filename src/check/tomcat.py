from src.ssh_utils import execute_ssh_command
from src.check.tomcat_log import (
    check_tomcat_log_errors,
    check_tomcat_log_details,
    check_tomcat_context_resource
)
from src.check.network import check_port_status

def check_tomcat_services(client):
    """
    Tomcat 서버의 주요 서비스 상태, 로그, 포트, 리소스 설정을 점검하는 함수.
    """
    result = "\n[Tomcat 서비스 확인]\n"

    result += "\n[ps -ef | grep tomcat]\n"
    out, _ = execute_ssh_command(client, "ps -ef | grep tomcat")  # tomcat 프로세스 확인
    result += out

    result += "\n[systemctl status tomcat]\n"
    out, _ = execute_ssh_command(client, "systemctl status tomcat | head -n 10")  # tomcat 서비스 상태 확인
    result += out

    result += "\n[Tomcat 로그 에러 확인]\n"
    result += check_tomcat_log_errors(client)         # Tomcat 로그 에러 라인 확인
    result += check_tomcat_log_details(client)        # Tomcat 로그 디렉터리 및 logrotate 상태 확인
    result += check_port_status(client, [8080, 443])  # 8080, 443 포트 상태 확인
    result += check_tomcat_context_resource(client)   # context.xml의 리소스 설정 확인

    return result
