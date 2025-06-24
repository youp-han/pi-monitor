import os
from datetime import datetime
from src.ssh_utils import execute_ssh_command

def check_tomcat_log_errors(client):
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
    log_dir = "/appwas/tomcat/apache-tomcat-9.0.87/logs"
    result = "\n[Tomcat 로그 디렉터리 상태]\n"

    cmd_ls = f"ls -altr {log_dir}/catalina.* 2>/dev/null"
    ls_output, err = execute_ssh_command(client, cmd_ls)
    if not ls_output:
        result += "[ERROR] 로그 디렉토리를 읽을 수 없거나 파일이 없음\n"
        return result

    result += ls_output

    logrotate_hint = any(".gz" in line for line in ls_output.splitlines())
    result += "\n[logrotate 판단 결과]\n"
    result += "✅ logrotate 작동 중 (압축 로그 파일 존재)\n" if logrotate_hint else "❌ logrotate 미작동 또는 설정 없음\n"

    cmd_size = f"du -m {log_dir}/catalina.out 2>/dev/null || echo 'catalina.out 없음 또는 권한 부족'"
    size_out, _ = execute_ssh_command(client, cmd_size)
    result += "\n[catalina.out 용량 (MB)]\n" + size_out.strip() + " (MB)\n"

    return result

def check_tomcat_context_resource(client):
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
