from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A10_01(task: Task) -> Result:
    """Check if mail server is listening on port 143"""
    command = "ss -tulpen | grep 143"
    score = 0
    msg = "No mail server listening on port 143"
    v4_enabled = False
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "0.0.0.0:143" in cmd_result.result:
            msg = "Mail server is reachable over IPv4 on tcp/143"
            score += 1
            v4_enabled = True
        if "[::]:143" in cmd_result.result:
            msg = (
                "Mail server is reachable over IPv4 & IPv6 on tcp/143"
                if v4_enabled
                else "Mail server is reachable over IPv6 only on tcp/143"
            )
            score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )
