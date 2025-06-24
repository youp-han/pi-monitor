# src/monitor.py
from src.check.apache import check_apache_services
from src.check.tomcat import check_tomcat_services
from src.check.network import check_firewalld_status
from src.check.system import check_system_health

def monitor_server(server):
    host = server["host"]
    user = server["user"]
    password = server["pass"]
    s_type = server["type"]
    s_where = server["where"]
    s_envFile = server["envFile"]

    result = f"\n=== [{host}] ({s_type}) ===\n"

    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password, timeout=10)

        result += check_system_health(client)

        if s_type == "tomcat":
            result += check_tomcat_services(client)
        elif s_type == "apache":
            result += check_apache_services(client, s_where, s_envFile)

        result += check_firewalld_status(client)

    except Exception as e:
        result += f"\n[오류 발생] {e}"
    finally:
        client.close()

    return result
