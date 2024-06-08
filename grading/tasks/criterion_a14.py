from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A14_01(task: Task) -> Result:
    """Check if main.html is served"""
    command = "curl -s --connect-timeout 2 http://127.0.0.1/ 2>&1"
    score = 0
    msg = f"main.html is NOT served as index page on {task.host}"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "7ecb4e033421b96f88e2111fe97cdad4ddceacc6" in cmd_result.result:
            msg = f"main.html is served as index page on {task.host}"
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


def task_A14_02(task: Task) -> Result:
    """Check if main.html is served"""
    command = "curl -s --connect-timeout 2 http://127.0.0.1/loremipsum 2>&1"
    score = 0
    msg = f"404.html is NOT served as 404 page on {task.host}"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "Sorry, but something went wrong" in cmd_result.result:
            msg = f"404.html is served as 404 page on {task.host}"
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
