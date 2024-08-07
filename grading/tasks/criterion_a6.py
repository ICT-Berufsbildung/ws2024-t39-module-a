from nornir.core.task import Task, Result
from tasks.common.command_controller import run_command

from tasks.common.helper import UNKNOWN_MSG

# Firewall


def task_A06_01(task: Task) -> Result:
    """Port forwarding tcp/80 & 443 check"""
    command = "curl -sv --connect-timeout 2 http://1.1.1.10 2>&1"
    commands = [command]
    score = 0
    cmd_result = None
    command_outputs = []
    msg = "tcp/80 & tcp/443 are NOT reachable over WAN"
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "Connected to 1.1.1.10" in cmd_result.result:
            score = 0.1
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = "curl -ksv --connect-timeout 2 https://1.1.1.10 2>&1"
    commands.append(command)

    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "Connected to 1.1.1.10" in cmd_result.result:
            score += 0.1
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    if score > 0:
        msg = "Only tcp/80 or tcp/443 are reachable over WAN"     

    return Result(
        host=task.host,
        result="tcp/80 & tcp/443 are reachable over WAN" if score == 0.2 else msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.2,
    )


def task_A06_02(task: Task) -> Result:
    """Port forwarding udp/53 check"""
    command = "dig +short +time=2 +tries=1 @1.1.1.10 dmz.worldskills.org SOA"
    second_command = (
        "dig +tcp +short +time=2 +tries=1 @1.1.1.10 dmz.worldskills.org SOA"
    )
    score = 0
    commands = [command, second_command]
    command_outputs = []
    msg = "udp/53 and tcp/53 are NOT reachable over WAN"
    try:
        cmd_result = run_command(task=task, command=command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org" in cmd_result.result:
            msg = "udp/53 is reachable over WAN"
            score += 0.05
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    try:
        cmd_result = run_command(task=task, command=second_command)
        command_outputs.append(cmd_result.result)
        if "dmz.worldskills.org" in cmd_result.result:
            msg = (
                "udp/53 & tcp/53 are reachable over WAN"
                if score == 1
                else "tcp/53 are reachable over WAN"
            )
            score += 0.05
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.1,
    )


def task_A06_03a(task: Task) -> Result:
    """SNAT precheck"""
    command = "ip route show default"
    cmd_result = None
    cheated = False
    try:
        cmd_result = run_command(task=task, command=command)
        if "1.1.1.10" in cmd_result.result:
            cheated = True
    except Exception:
        pass

    return Result(
        host=task.host,
        result=cheated,
        command=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
    )


def task_A06_03(
    task: Task, cheated: bool, check_command: str, check_command_output: str
) -> Result:
    """SNAT check"""
    if cheated:
        return Result(
            host=task.host,
            msg="SNAT is probably not working on fw01 as default route exists on jamie-ws01",
            command_run=check_command,
            command_output=check_command_output,
            score=0,
            max_score=0.1,
        )

    command = r"""timeout 2  bash -c "echo -e '\x1dclose\x0d' | telnet 1.1.1.20 22" """
    score = 0
    cmd_result = None
    msg = "SNAT is not working on fw01"
    try:
        cmd_result = run_command(task=task, command=command)
        if "Connected to 1.1.1.20" in cmd_result.result:
            msg = "SNAT is working on fw01"
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
