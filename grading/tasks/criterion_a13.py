from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG


def task_A13_01(task: Task) -> Result:
    """Check if reverse proxy is listening on port 80"""
    command = "curl -vs --connect-timeout 2 http://127.0.0.1/ 2>&1 ; curl -vs --connect-timeout 2 http://[::1]/ 2>&1"
    score = 0
    cmd_result = None
    msg = f"Reverse proxy {task.host} is not listening on port 80"
    try:
        cmd_result = run_command(task=task, command=command)
        if (
            "Connected to 127.0.0.1" in cmd_result.result
            and "Connected to ::1" in cmd_result.result
        ):
            msg = f"Reverse proxy  {task.host} is listening on port 80"
            score = 0.1
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.1,
    )


def task_A13_02(task: Task) -> Result:
    """Check if reverse proxy is listening on port 443"""
    command = "curl -kvs --connect-timeout 2 https://127.0.0.1/ 2>&1 ; curl -kvs --connect-timeout 2 https://[::1]/ 2>&1"
    score = 0
    cmd_result = None
    msg = f"Reverse proxy {task.host} is not listening on port 443"
    try:
        cmd_result = run_command(task=task, command=command)
        if (
            "Connected to 127.0.0.1" in cmd_result.result
            and "Connected to ::1" in cmd_result.result
        ):
            msg = f"Reverse proxy  {task.host} is listening on port 443"
            score = 0.1
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.1,
    )


def task_A13_03(task: Task) -> Result:
    """Check if reverse proxy is load balancing"""
    command = "curl -ks --connect-timeout 2 https://www.dmz.worldskills.org/whoami 2>&1"
    score = 0
    commands = []
    command_outputs = []
    msg = "Reverse proxy not load balancing web traffic"
    responses = set()
    try:
        for round in range(4):
            commands.append(command)
            cmd_result = run_command(task=task, command=command)
            web_response = cmd_result.result
            command_outputs.append(web_response)
            if "web01" in web_response and "web02" not in web_response:
                responses.add("web01")
            if "web01" not in web_response and "web02" in web_response:
                responses.add("web02")
        if len(responses) > 1:
            msg = "Reverse proxy is load balancing web traffic"
            score = 0.25
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.25,
    )


def task_A13_04(task: Task) -> Result:
    """Check if header is set by haproxy"""
    command = (
        "curl -kvs --connect-timeout 2 https://www.dmz.worldskills.org/whoami 2>&1"
    )
    score = 0
    cmd_result = None
    msg = "Reverse proxy is NOT setting via-proxy header"
    try:
        cmd_result = run_command(task=task, command=command)
        if "via-proxy: ha-prx" in cmd_result.result:
            msg = "Reverse proxy has set via-proxy header"
            score = 0.5
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.5,
    )


def task_A13_05(task: Task) -> Result:
    """Check HTTPS redirect"""
    command = "curl -kvs -I --connect-timeout 2 http://www.dmz.worldskills.org/ 2>&1"
    score = 0
    cmd_result = None
    msg = "Reverse proxy is NOT redirecting HTTP to HTTPS"
    try:
        cmd_result = run_command(task=task, command=command)
        if (
            "HTTP/1.1 301" in cmd_result.result or "HTTP/1.1 302" in cmd_result.result
        ) and "location: https://" in cmd_result.result.lower():
            msg = "Reverse proxy is redirecting HTTP to HTTPS"
            score = 0.25
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.25,
    )


def task_A13_06a(task: Task) -> Result:
    """Pretask to get certificate fingerprint"""
    command = "openssl x509 -fingerprint -in /opt/grading/ca/web.pem -noout"
    cmd_result = None
    fingerprint = ""
    try:
        cmd_result = run_command(task=task, command=command)
        fingerprint = cmd_result.result.replace("SHA1 Fingerprint=", "")
    except Exception:
        # Exit code 1
        pass
    return Result(
        host=task.host,
        result=fingerprint,
        command=f"root@{task.host} $ {command}",
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
    )


def task_A13_06(
    task: Task,
    certificate_fingerprint: str,
    check_command: str,
    check_command_output: str,
) -> Result:
    """Check HTTPS certificate"""
    command = "timeout 2 openssl s_client -connect www.dmz.worldskills.org:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -noout -in /dev/stdin"
    score = 0
    cmd_result = None
    msg = "TLS certificate is not signed by CA"
    try:
        cmd_result = run_command(task=task, command=command)
        if certificate_fingerprint in cmd_result.result:
            msg = "TLS certificate is signed by CA"
            score = 0.3
    except Exception:
        # Exit code 1
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=[check_command, command],
        command_output=[
            check_command_output,
            cmd_result.result if cmd_result else UNKNOWN_MSG,
        ],
        score=score,
        max_score=0.3,
    )


def task_A13_07(task: Task) -> Result:
    """Check VIP is listening to web traffic"""
    command = "curl -4vks --connect-timeout 2 https://www.dmz.worldskills.org 2>&1 ; curl -6vks --connect-timeout 2 https://www.dmz.worldskills.org 2>&1"
    score = 0
    cmd_result = None
    msg = "Virtual IP is NOT reachable over IPv4 & IPv6"
    try:
        cmd_result = run_command(task=task, command=command)
        if (
            "10.1.20.20" in cmd_result.result
            and "2001:db8:1001:20::20" in cmd_result.result
        ):
            msg = "Virtual IP is reachable over IPv4 & IPv6"
            score = 0.5
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.5,
    )
