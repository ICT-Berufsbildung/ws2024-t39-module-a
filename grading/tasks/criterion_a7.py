from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


def task_A07_01(task: Task) -> Result:
    """Check wireguard interface"""
    command = "wg show"
    score = 0
    cmd_result = None
    msg = "wg0 interface is not up"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "interface: wg0" in cmd_result.result:
            msg = "wg0 interface is up"
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


def task_A07_02(task: Task) -> Result:
    """Check if PSK is configured for wg0"""
    command = "wg show wg0 preshared-keys"
    score = 0
    msg = "PSK is not configured for wg0"
    try:
        task.run(task=paramiko_command, command=command)
        msg = "PSK is configured for wg0"
        score = 0.2
    except Exception:
        pass

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        command_output=process_result_exit_code(score != 0.0),
        score=score,
        max_score=0.2,
    )


def task_A07_03(task: Task) -> Result:
    """Check IPv4 & IPv6 availabilties"""
    command = "wg show interfaces"
    score = 0
    commands = [command]
    command_outputs = []
    vpn_interface_name = ""
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        vpn_interface_name = cmd_result.result.strip()
        command_outputs.append(cmd_result.result)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    msg = "jamie-ws01 is not configured to allow IPv4 & IPv6"

    if vpn_interface_name:
        command = f"(ip route get 10.1.10.10 ; ip -6 route get 2001:db8:1001:10::10) | grep {vpn_interface_name} | wc -l"
        commands.append(command)
        try:
            cmd_result = task.run(task=paramiko_command, command=command)
            command_outputs.append(cmd_result.result)
            # Route through wireguard per route has been found (IPv4 & IPv6)
            if "2" in cmd_result.result:
                score = 0.1
                msg = "jamie-ws01 has routes for IPv4 & IPv6 to reach int-srv01"
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


def task_A07_04(task: Task) -> Result:
    """Check if wireguard is configured as systemd service"""
    command = "systemctl is-active wg-quick@wg0.service"
    score = 0
    cmd_result = None
    msg = "systemd service for wireguard not available nor active"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "active" in cmd_result.result:
            msg = "systemd service for wireguard is active"
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


def task_A07_05(task: Task) -> Result:
    """End-to-End test"""
    command = "dig +time=2 +tries=1 +short @10.1.10.10 int.worldskills.org SOA"
    score = 0
    commands = [command]
    command_outputs = []

    msg = "jamie-ws01 is not able to reach DNS over IPv4 & IPv6"
    v4_reachable = False
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        if "worldskills.org" in cmd_result.result:
            msg = "jamie-ws01 is able to reach DNS over IPv4 only"
            score += 0.5
            v4_reachable = True
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    command = (
        "dig +time=2 +tries=1 +short @2001:db8:1001:10::10 int.worldskills.org SOA"
    )
    commands.append(command)
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        if "worldskills.org" in cmd_result.result:
            msg = (
                "jamie-ws01 is able to reach DNS over IPv4 & IPv6"
                if v4_reachable
                else "jamie-ws01 is able to reach DNS over IPv6 only"
            )
            score += 0.5
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=1.0,
    )
