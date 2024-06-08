from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.dns_checks import (
    DNS_RECORD_TYPE,
    check_dns_port_listen,
    check_host_record,
)


def task_A04_01(task: Task) -> Result:
    """DNS port check"""
    result = check_dns_port_listen(task)

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.1,
    )


def task_A04_02(task: Task) -> Result:
    """A int-srv01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="int-srv01.int.worldskills.org.",
        ip_address="10.1.10.10",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A04_03(task: Task) -> Result:
    """AAAA int-srv01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="int-srv01.int.worldskills.org.",
        ip_address="2001:db8:1001:10::10",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A04_04(task: Task) -> Result:
    """SRV int-srv01 check"""
    command = (
        "dig +short +time=2 +tries=1 @127.0.0.1 _ldap._tcp.auth.int.worldskills.org SRV"
    )
    score = 0
    msg = "SRV record for int-srv01.int.worldskills.org does not exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "10 50 389 int-srv01.int.worldskills.org" in cmd_result.result:
            msg = "SRV record for int-srv01.int.worldskills.org exists"
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


def task_A04_05(task: Task) -> Result:
    """Recurse resolver check"""
    command = "dig +recurse +time=2 +tries=1 @127.0.0.1 int.worldskills.org SOA"
    score = 0
    msg = "int-srv01 is not a recursive"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "recursion requested but not available" not in cmd_result.result:
            msg = "int-srv01 is a recursive name server"
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


def task_A04_06(task: Task) -> Result:
    """Slave server check"""
    command = "rndc zonestatus dmz.worldskills.org."
    score = 0
    msg = "int-srv01 is not a secondary for dmz.worldskills.org."
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = "int-srv01 is secondary for dmz.worldskills.org."
            score += 1

        dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 dmz.worldskills.org SOA"
        cmd_result = task.run(task=paramiko_command, command=dig_command)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 1
        else:
            msg += " Cannot resolve dmz.worldskills.org on int-srv01"
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )


def task_A04_07(task: Task) -> Result:
    """Slave server for v4 reverse zone check"""
    command = "rndc zonestatus 20.1.10.in-addr.arpa."
    score = 0
    msg = "int-srv01 is not a secondary for IPv4 reverse zone in DMZ. "
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = "int-srv01 is secondary for 20.1.10.in-addr.arpa."
            score += 1
        dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 20.1.10.in-addr.arpa. SOA"
        cmd_result = task.run(task=paramiko_command, command=dig_command)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 1
        else:
            msg += " Cannot resolve 20.1.10.in-addr.arpa on int-srv01"
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )


def task_A04_08(task: Task) -> Result:
    """Slave server for v4 reverse zone check"""
    command = "rndc zonestatus 0.2.0.0.1.0.0.1.8.b.d.0.1.0.0.2.ip6.arpa."
    score = 0
    msg = "int-srv01 is not a secondary for IPv6 reverse zone in DMZ. "
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if (
            "type: secondary" in cmd_result.result
            and "next refresh" in cmd_result.result
        ):
            msg = "int-srv01 is secondary for IPv6 reverse zone in DMZ."
            score += 1
        dig_command = "dig +short +time=2 +tries=1 @127.0.0.1 0.2.0.0.1.0.0.1.8.b.d.0.1.0.0.2.ip6.arpa SOA"
        cmd_result = task.run(task=paramiko_command, command=dig_command)
        if "dmz.worldskills.org." in cmd_result.result:
            score += 1
        else:
            msg += " Cannot resolve IPv6 reverse in DMZ on int-srv01"
    except Exception:
        score += 0

    return Result(
        host=task.host,
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )
