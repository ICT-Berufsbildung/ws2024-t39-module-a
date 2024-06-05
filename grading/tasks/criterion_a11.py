from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A11_01(task: Task) -> Result:
    """Check if option TrustedUserCAKeys is set"""
    command = "sshd -T"
    score = 0
    msg = "TrustedUserCAKeys is NOT set on sshd"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "trustedusercakeys" in cmd_result.result:
            msg = "TrustedUserCAKeys is set on sshd"
            score += 1
    except Exception:
        # Exit code 1
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A11_02(task: Task) -> Result:
    """Check ssh cert auth"""
    command = 'timeout 2 bash -c \'ssh -vv -o StrictHostKeyChecking=no root@10.1.20.10 "lsb_release -is" 2>&1 | grep "Server accepts"\''
    score = 0
    msg = "SSH certificate based auth failed"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "CERT" in cmd_result.result:
            msg = "SSH certificate based auth was successful"
            score += 1
    except Exception:
        # Exit code 1
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )