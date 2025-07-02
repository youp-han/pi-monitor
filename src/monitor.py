# src/monitor.py
from src.check.apache import check_apache_services
from src.check.tomcat import check_tomcat_services
from src.check.network import check_firewalld_status
from src.check.system import check_system_health
from src.check.service import check_changeFlow_services, check_ecredible_services

def monitor_server(server):
    # 서버 정보에서 각 항목 추출
    host = server.get("host", "")
    user = server.get("user", "")
    password = server.get("pass", "")
    s_type = server.get("type", "")
    s_where = server.get("where", "")
    s_envFile = server.get("envFile", "")
    s_service = server.get("service", "")

    # 결과 문자열 초기화
    result = f"\n=== [{host}] ({s_type}) ===\n"

    try:
        import paramiko  # paramiko 라이브러리 동적 임포트
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 호스트키 자동 추가
        client.connect(hostname=host, username=user, password=password, timeout=10)  # SSH 접속

        result += check_system_health(client)  # 시스템 상태 점검

        if s_type == "tomcat":
            result += check_tomcat_services(client)  # Tomcat 점검
            if s_service == "cfagent":
                result += check_changeFlow_services(client)
            elif s_service == "ecredible":
                result += check_ecredible_services(client)

        elif s_type == "apache":
            result += check_apache_services(client, s_where, s_envFile)  # Apache 점검

        result += check_firewalld_status(client)  # 방화벽 상태 점검

    except Exception as e:
        result += f"\n[오류 발생] {e}"  # 예외 발생 시 오류 메시지 추가
    finally:
        client.close()  # SSH 연결 종료

    return result  # 결과 반환
