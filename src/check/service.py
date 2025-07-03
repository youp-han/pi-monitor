from src.ssh_utils import execute_ssh_command

def check_changeFlow_services(client):

    result = "\n[ChangeFlow Agent 확인]\n"
    result += "sudo systemctl status cfagent\n"
    out, _ = execute_ssh_command(client, "sudo systemctl status cfagent")
    result += out + "\n"

    return result

def check_ecredible_services(client):

    result = "\n[Ecredible Agent 확인]\n"
    result += "ls -la /appwas/opt/DTAC/logs/crontablog/\n"
    out, _ = execute_ssh_command(client, "ls -la /appwas/opt/DTAC/logs/crontablog/")
    result += out + "\n"

    result += "\n[Ecredible Agent 상태 확인]\n"
    result += "sudo crontab -l\n"
    out, _ = execute_ssh_command(client, "sudo crontab -l")
    result += out + "\n"

    return result