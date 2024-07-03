from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


def task_A10_01(task: Task) -> Result:
    """Check if LUKS exists on sdb"""
    command = "cryptsetup isLuks /dev/sdb"
    score = 0
    msg = "/dev/sdb is NOT encrypted"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code 0
        msg = "/dev/sdb is encrypted"
        score = 0.25
    except Exception:
        # Exit code 1
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0),
        score=score,
        max_score=0.25,
    )


def task_A10_02(task: Task) -> Result:
    """Check passphrase for LUKS"""
    command = 'printf "Skill39" | cryptsetup luksOpen --test-passphrase /dev/sdb'
    score = 0
    msg = "/dev/sdb CANNOT be opened using passphrase"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code 0
        msg = "/dev/sdb can be opened using passphrase"
        score = 0.25
    except Exception:
        # not exit code 0
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0),
        score=score,
        max_score=0.25,
    )


def task_A10_03(task: Task) -> Result:
    """Check keyfile for LUKS"""
    command = (
        "cryptsetup luksOpen --key-file /etc/keys/backup.key --test-passphrase /dev/sdb"
    )
    score = 0
    msg = "/dev/sdb CANNOT be opened using keyfile"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code 0
        msg = "/dev/sdb can be opened using keyfile"
        score = 0.25
    except Exception:
        # not exit code 0
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0),
        score=score,
        max_score=0.25,
    )


def task_A10_04(task: Task) -> Result:
    """Check crypttab"""
    command = "lsblk /dev/sdb -no UUID -I 8 -d"
    score = 0
    commands = [command]
    command_outputs = []
    msg = "crypttab is NOT configured for auto-unlock"
    disk_id = ""
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        disk_id = cmd_result.result.strip()
    except Exception:
        pass

    if disk_id:
        command = "cat /etc/crypttab"
        commands.append(command)
        try:
            cmd_result = task.run(task=paramiko_command, command=command)
            command_outputs.append(cmd_result.result)
            if (
                disk_id in cmd_result.result
                and "/etc/keys/backup.key" in cmd_result.result
            ):
                msg = "crypttab is configured for auto-unlock"
                score = 0.3
        except Exception:
            # not exit code 0
            pass

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.3,
    )


def task_A10_05(task: Task) -> Result:
    """Check fstab"""
    command = "cat /etc/fstab"
    score = 0
    cmd_result = None
    msg = "/opt/backup is missing in fstab"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "/opt/backup" in cmd_result.result:
            msg = "/opt/backup exists in fstab"
            score = 0.2
    except Exception:
        # not exit code 0
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=score,
        max_score=0.2,
    )


def task_A10_06(task: Task) -> Result:
    """Check backup script"""
    command = "rm -rf /opt/backup/* ; bash /opt/backup.sh"
    score = 0
    cmd_result = None
    commands = [command]
    command_outputs = []
    msg = "Backup script not found"
    categories = []
    try:
        task.run(task=paramiko_command, command=command)
        command_outputs.append(process_result_exit_code(True))
    except Exception:
        command_outputs.append(process_result_exit_code(False))

    command = (
        "find /opt/backup/ -name dovecot.conf -o -name main.cf -o -name dovecot.index*"
    )
    commands.append(command)
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        if "main.cf" in cmd_result.result:
            score += 0.5
            categories.append("postfix")
        if "dovecot.conf" in cmd_result.result:
            score += 0.5
            categories.append("dovecot")
        if "dovecot.index" in cmd_result.result:
            score += 1
            categories.append("mailboxes")
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = "cat /opt/backup.sh"
    commands.append(command)
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    if categories:
        msg = f"Backup script is working. {', '.join(categories)} are backed up"

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=2.0,
    )
