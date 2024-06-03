from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A08_01(task: Task) -> Result:
    """Check transparent proxy"""
    command = "curl -s -I --connect-timeout 3 http://10.1.20.10 2>&1"
    score = 0
    msg = "IPv4 traffic not intercepted by transparent proxy"
    v4_intercepted = False
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "x-secured-by: clearsky-proxy" in cmd_result.result:
            msg = "Only IPv4 traffic intercepted by transparent proxy"
            score += 1
            v4_intercepted = True
    except Exception:
        score += 0
    command = "curl -s -I --connect-timeout 3 http://[2001:db8:1001:20::20] 2>&1"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "x-secured-by: clearsky-proxy" in cmd_result.result:
            msg = (
                "IPv4 & IPv6 traffic intercepted by transparent proxy"
                if v4_intercepted
                else "Only IPv6 traffic intercepted by transparent proxy"
            )
            score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=f"Web traffic from {task.host} - {msg}",
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )
