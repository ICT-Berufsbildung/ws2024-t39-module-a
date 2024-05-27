from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command
from nornir_paramiko.exceptions import CommandError

def task_A1_01(task: Task) -> Result:
    command = "nc -z -w3 localhost 389"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code is 0
        got_mark = True
    except CommandError:
        # Exit code is 1
        got_mark = False
    """LDAP check"""
    return Result(
        host=task.host,
        result=f"LDAP port tcp/389 is reachable" if got_mark else "LDAP port tcp/389 is NOT reachable",
        command_run=command,
        point=0.1 if got_mark else 0.0,
        max_point=0.1
    )