from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A10_01(task: Task) -> Result:
    """Check if mail server is listening on port 143"""
    command = "cryptsetup isLuks /dev/sdb"
    score = 0
    msg = "/dev/sdb is NOT encrypted"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code 0
        msg = "/dev/sdb is encrypted"
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


def task_A10_02(task: Task) -> Result:
    """Check passphrase for LUKS"""
    command = 'printf "Skill39" | cryptsetup luksOpen --test-passphrase /dev/sdb'
    score = 0
    msg = "/dev/sdb CANNOT be opened using passphrase"
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code 0
        msg = "/dev/sdb can be opened using passphrase"
        score += 1
    except Exception:
        # not exit code 0
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
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
        score += 1
    except Exception:
        # not exit code 0
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A10_04(task: Task) -> Result:
    """Check crypttab"""
    command = "lsblk /dev/sdb -no UUID -I 8 -d"
    score = 0
    msg = "crypttab is NOT configured for auto-unlock"
    disk_id = ""
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        disk_id = cmd_result.result.strip()
    except Exception:
        pass

    if disk_id:
        command = "cat /etc/crypttab"
        try:
            cmd_result = task.run(task=paramiko_command, command=command)
            if (
                disk_id in cmd_result.result
                and "/etc/keys/backup.key" in cmd_result.result
            ):
                msg = "crypttab is configured for auto-unlock"
                score += 1
        except Exception:
            # not exit code 0
            score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A10_05(task: Task) -> Result:
    """Check fstab"""
    command = "cat /etc/fstab"
    score = 0
    msg = "/opt/backup is missing in fstab"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "/opt/backup" in cmd_result.result:
            msg = "/opt/backup exists in fstab"
            score += 1
    except Exception:
        # not exit code 0
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A10_06(task: Task) -> Result:
    """Check backup script"""
    command = "rm -rf /opt/backup/* ; bash /opt/backup.sh"
    score = 0
    msg = "Backup script not found"
    categories = []
    try:
        task.run(task=paramiko_command, command=command)
    except Exception:
        # not exit code 0
        score += 0

    command = (
        "find /opt/backup/ -name dovecot.conf -o -name main.cf -o -name dovecot.index*"
    )
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "main.cf" in cmd_result.result:
            score += 1
            categories.append("postfix")
        if "dovecot.conf" in cmd_result.result:
            score += 1
            categories.append("dovecot")
        if "dovecot.index" in cmd_result.result:
            score += 1
            categories.append("mailboxes")
    except Exception:
        # not exit code 0
        score += 0

    if categories:
        msg = f"Backup script is working. {', '.join(categories)} are backed up"

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.3,
    )
