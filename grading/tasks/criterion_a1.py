from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

def task_A1_01(task: Task) -> Result:
    
    task.run(task=paramiko_command, command="ip addr")
    """LDAP check"""
    return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
    )