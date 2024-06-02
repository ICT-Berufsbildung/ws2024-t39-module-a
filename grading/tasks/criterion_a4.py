from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A4_01(task: Task) -> Result:
    """DNS port check"""
    command = "echo -e '\x1dclose\x0d' | telnet 127.0.0.1 53 && echo -e '\x1dclose\x0d' | telnet ::1 53"
    score = 0
    msg = "DNS is not listening on IPv4 AND IPv6"
    try:
        task.run(task=paramiko_command, command=command)
        msg = "DNS is listening on IPv4 & IPv6."
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


def task_A4_02(task: Task) -> Result:
    """A int-srv01 check"""
    command = "dig +short +time=2 +tries=1 @127.0.0.1 int-srv01.int.worldskills.org A"
    score = 0
    msg = "A record for int-srv01.int.worldskills.org does not exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "10.1.10.10" in cmd_result.result:
            msg = "A record for int-srv01.int.worldskills.org exist"
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


def task_A4_03(task: Task) -> Result:
    """AAAA int-srv01 check"""
    command = (
        "dig +short +time=2 +tries=1 @127.0.0.1 int-srv01.int.worldskills.org AAAA"
    )
    score = 0
    msg = "AAAA record for int-srv01.int.worldskills.org does not exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "2001:db8:1001:10::10" in cmd_result.result:
            msg = "AAAA record for int-srv01.int.worldskills.org exist"
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


def task_A4_04(task: Task) -> Result:
    """PTR int-srv01 for IPv4 check"""
    command = "dig +short +time=2 +tries=1 @127.0.0.1 -x 10.1.10.10"
    score = 0
    msg = "IPv4 PTR record for int-srv01.int.worldskills.org does not exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "int-srv01.int.worldskills.org." in cmd_result.result:
            msg = "IPv4 PTR record for int-srv01.int.worldskills.org exists"
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


def task_A4_05(task: Task) -> Result:
    """PTR int-srv01 for IPv4 check"""
    command = "dig +short +time=2 +tries=1 @127.0.0.1 -x 2001:db8:1001:10::10"
    score = 0
    msg = "IPv6 PTR record for int-srv01.int.worldskills.org does not exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "int-srv01.int.worldskills.org." in cmd_result.result:
            msg = "IPv6 PTR record for int-srv01.int.worldskills.org exists"
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


def task_A4_06(task: Task) -> Result:
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


def task_A4_07(task: Task) -> Result:
    """SRV int-srv01 check"""
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


def task_A4_08(task: Task) -> Result:
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


def task_A4_09(task: Task) -> Result:
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


def task_A4_10(task: Task) -> Result:
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
