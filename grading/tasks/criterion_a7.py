from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command
from nornir_paramiko.exceptions import CommandError

# Wireguard


def task_A7_01(task: Task) -> Result:
    """Check wireguard interface"""
    command = "wg show"
    score = 0
    msg = "wg0 interface is not up"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "interface: wg0" in cmd_result.result:
            msg = "wg0 interface is up"
            score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A7_02(task: Task) -> Result:
    """Check if PSK is configured for wg0"""
    command = "wg show wg0 preshared-keys"
    score = 0
    msg = "PSK is not configured for wg0"
    try:
        task.run(task=paramiko_command, command=command)
        msg = "PSK is configured for wg0"
        score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )


def task_A7_03(task: Task) -> Result:
    """Check IPv4 & IPv6 availabilties"""
    command = "wg show interfaces"
    score = 0
    vpn_interface_name = ""
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        vpn_interface_name = cmd_result.result.strip()
    except Exception:
        pass

    msg = "jamie-ws01 is not able to reach DNS over IPv4 & IPv6"

    if vpn_interface_name:
        command = f"(ip route get 10.1.10.10 ; ip -6 route get 2001:db8:1001:10::10) | grep {vpn_interface_name} | wc -l"
        try:
            cmd_result = task.run(task=paramiko_command, command=command)
            # Route through wireguard per route has been found (IPv4 & IPv6)
            if "2" in cmd_result.result:
                score += 1
                msg = "jamie-ws01 is not able to reach DNS over IPv4 & IPv6, but routes are available"
        except Exception:
            pass

    # End-to-End test
    command = "dig +time=2 +tries=1 +short @10.1.10.10 int.worldskills.org SOA"
    v4_reachable = False
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "worldskills.org" in cmd_result.result:
            msg = "jamie-ws01 is able to reach DNS over IPv4 only"
            score += 1
            v4_reachable = True
    except Exception:
        pass

    command = (
        "dig +time=2 +tries=1 +short @2001:db8:1001:10::10 int.worldskills.org SOA"
    )
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "worldskills.org" in cmd_result.result:
            msg = (
                "jamie-ws01 is able to reach DNS over IPv4 & IPv6"
                if v4_reachable
                else "jamie-ws01 is able to reach DNS over IPv6 only"
            )
            score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.3,
    )


def task_A7_04(task: Task) -> Result:
    """Check if wireguard is configured as systemd service"""
    command = "systemctl is-active wg-quick@wg0.service"
    score = 0
    msg = "systemd service for wireguard not available nor active"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "active" in cmd_result.result:
            msg = "systemd service for wireguard is active"
            score += 1
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.1,
    )
