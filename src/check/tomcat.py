from src.ssh_utils import execute_ssh_command
from src.check.tomcat_log import (
    check_tomcat_log_errors,
    check_tomcat_log_details,
    check_tomcat_context_resource
)
from src.check.network import check_port_status

def check_tomcat_services(client):
    result = "\n[Tomcat 서비스 확인]\n"

    result += "\n[ps -ef | grep tomcat]\n"
    out, _ = execute_ssh_command(client, "ps -ef | grep tomcat")
    result += out

    result += "\n[systemctl status tomcat]\n"
    out, _ = execute_ssh_command(client, "systemctl status tomcat | head -n 10")
    result += out

    result += "\n[Tomcat 로그 에러 확인]\n"
    result += check_tomcat_log_errors(client)
    result += check_tomcat_log_details(client)
    result += check_port_status(client, [8080, 443])
    result += check_tomcat_context_resource(client)

    return result
