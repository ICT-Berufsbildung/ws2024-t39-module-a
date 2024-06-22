from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.helper import UNKNOWN_MSG


def task_A05_01(task: Task) -> Result:
    """IPv4 forwarding enabled check"""
    command = "sysctl -p"
    score = 0
    msg = "IPv4 forwarding is not enabled on FW"
    cmd_result = None
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "net.ipv4.ip_forward = 1" in cmd_result.result:
            msg = "IPv4 forwarding is enabled."
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


def task_A05_02(task: Task) -> Result:
    """IPv4 forwarding enabled check"""
    command = "sysctl -p"
    score = 0
    msg = "IPv6 forwarding is not enabled on FW"
    cmd_result = None
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "net.ipv6.conf.all.forwarding = 1" in cmd_result.result:
            msg = "IPv6 forwarding is enabled."
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
