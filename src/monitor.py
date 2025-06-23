import os
from datetime import datetime, timedelta
from src.ssh_utils import execute_ssh_command  # SSH 명령 실행 함수 임포트

def parse_vmstat_for_high_cpu(vmstat_output):
    """
    vmstat 명령 결과에서 CPU idle 값이 50 미만인 경우가 있는지 확인.
    CPU 사용률이 높은 상태를 감지.
    """
    lines = vmstat_output.strip().splitlines()
    data_lines = lines[2:]  # 헤더 이후 데이터 라인만 추출
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 15:
            idle = int(parts[14])  # 15번째 컬럼이 idle 값
            if idle < 50:
                return True
    return False

def check_apache_log(client, s_where, s_envFile):
    """
    Apache 에러 로그 파일을 찾아 에러 라인 수와 내용을 반환.
    오늘/어제 로그 파일을 우선적으로 확인.
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
        return "Apache 로그 파일 없음 또는 찾을 수 없음\n"

    # 에러 라인 추출
    cmd_lines = f"sudo grep -i 'error' {log_path}"
    error_lines, _ = execute_ssh_command(client, cmd_lines)

    # 에러 라인 수 카운트
    cmd_count = f"grep -i 'error' {log_path} | wc -l"
    count_out, _ = execute_ssh_command(client, cmd_count)
    filename = os.path.basename(log_path)

    result = f"[Apache Log Errors - {filename}]\n에러 라인 수: {count_out.strip()}"
    result += f"\n[에러 라인 내용]\n{error_lines.strip()}\n" if error_lines.strip() else "\n(에러 내용 없음)\n"
    return result

def check_tomcat_log_errors(client):
    """
    Tomcat catalina 로그에서 에러 라인과 개수를 추출.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    log_path = f"/appwas/tomcat/apache-tomcat-9.0.87/logs/catalina.{today}.log"

    cmd_lines = f"sudo grep -i 'error' {log_path}"
    error_lines, _ = execute_ssh_command(client, cmd_lines)

    cmd_count = f"sudo grep -i 'error' {log_path} | wc -l"
    count_out, _ = execute_ssh_command(client, cmd_count)

    result = f"[Tomcat Log Errors - {today}]\n에러 라인 수: {count_out.strip()}\n"
    result += f"\n[에러 라인 내용]\n{error_lines.strip()}\n" if error_lines.strip() else "\n(에러 내용 없음)\n"
    return result

def check_tomcat_log_details(client):
    """
    Tomcat 로그 디렉터리의 파일 목록, logrotate 동작 여부, catalina.out 용량 확인.
    """
    log_dir = "/appwas/tomcat/apache-tomcat-9.0.87/logs"
    result = "\n[Tomcat 로그 디렉터리 상태]\n"

    # catalina.* 로그 파일 목록 확인
    cmd_ls = f"ls -altr {log_dir}/catalina.* 2>/dev/null"
    ls_output, err = execute_ssh_command(client, cmd_ls)
    if not ls_output:
        result += "[ERROR] 로그 디렉토리를 읽을 수 없거나 파일이 없음\n"
        return result

    result += ls_output

    # logrotate 동작 여부 판단 (압축 파일 존재 여부)
    logrotate_hint = any(".gz" in line for line in ls_output.splitlines())
    result += "\n[logrotate 판단 결과]\n"
    result += "✅ logrotate 작동 중 (압축 로그 파일 존재)\n" if logrotate_hint else "❌ logrotate 미작동 또는 설정 없음\n"

    # catalina.out 파일 용량 확인
    cmd_size = f"du -m {log_dir}/catalina.out 2>/dev/null || echo 'catalina.out 없음 또는 권한 부족'"
    size_out, _ = execute_ssh_command(client, cmd_size)
    result += "\n[catalina.out 용량 (MB)]\n" + size_out.strip() + " (MB)\n"

    return result

def check_port_status(client, ports):
    """
    지정한 포트들이 LISTEN 상태인지 확인.
    """
    result = "\n[포트 상태 확인]\n"
    for port in ports:
        cmd = f"ss -tan | grep {port}"
        out, _ = execute_ssh_command(client, cmd)
        if out.strip():
            result += f"포트 {port} → LISTEN 중\n{out.strip()}\n"
        else:
            result += f"포트 {port} → ❌ LISTEN 아닌 또는 비어 있음\n"
    return result

def check_tomcat_context_resource(client):
    """
    Tomcat context.xml에서 특정 JNDI 리소스(PIS_JNDI) 설정을 추출.
    """
    context_path = "/appwas/tomcat/apache-tomcat-9.0.87/conf/context.xml"
    cmd = r'''sudo awk '/<Resource/{block=""; capture=1}
    capture {block = block $0 "\n"}
    /\/>/ && capture {
        if (block ~ /name="PIS_JNDI"/) print block
        capture=0
    }' ''' + context_path

    out, err = execute_ssh_command(client, cmd)
    result = "\n[context.xml Resource 설정 확인]\n"
    if out.strip():
        result += out.strip()
    else:
        result += f"⚠️ Resource 설정 없음 또는 파일 권한 문제\n{err.strip()}"
    return result

def monitor_server(server):
    """
    서버 한 대에 대해 여러 상태(리소스, 로그, 서비스 등)를 점검하고 결과를 문자열로 반환.
    """
    host = server["host"]
    user = server["user"]
    password = server["pass"]
    s_type = server["type"]
    s_where = server["where"]
    s_envFile = server["envFile"]

    result = f"\n=== [{host}] ({s_type}) ===\n"

    try:
        import paramiko  # 동적으로 paramiko 임포트
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password, timeout=10)

        # vmstat로 시스템 리소스 확인
        result += "[vmstat 1 10]\n"
        vmstat_out, _ = execute_ssh_command(client, "vmstat 1 10")
        result += vmstat_out

        # CPU 사용률이 높으면 top 명령 실행
        if parse_vmstat_for_high_cpu(vmstat_out):
            result += "\n[High CPU detected! top 실행]\n"
            top_out, _ = execute_ssh_command(client, "top -b -n 1 | head -n 20")
            result += top_out

        # 디스크 사용량 확인
        result += "\n[df -k]\n"
        df_out, _ = execute_ssh_command(client, "df -k")
        result += df_out

        if s_type == "tomcat":
            # tomcat 프로세스 및 서비스 상태, 로그 등 점검
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

        elif s_type == "apache":
            # apache 프로세스 및 서비스 상태, 로그 등 점검
            result += "\n[ps -ef | grep httpd]\n"
            out, _ = execute_ssh_command(client, "ps -ef | grep httpd")
            result += out

            result += "\n[systemctl status httpd]\n"
            out, _ = execute_ssh_command(client, "systemctl status httpd | head -n 10")
            result += out

            result += "\n[Apache 로그 에러 확인]\n"
            result += check_apache_log(client, s_where, s_envFile)
            result += check_port_status(client, [80, 443])

        # 방화벽 서비스 상태 확인
        result += "\n[systemctl status firewalld]\n"
        out, _ = execute_ssh_command(client, "systemctl status firewalld | head -n 10")
        result += out

    except Exception as e:
        result += f"\n[오류 발생] {e}"
    finally:
        client.close()

    return result

def save_log_to_file(host, content):
    """
    모니터링 결과를 logs 디렉터리에 파일로 저장.
    """
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/monitor_{host}_{now}.log"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 로그 저장 완료: {filename}")
