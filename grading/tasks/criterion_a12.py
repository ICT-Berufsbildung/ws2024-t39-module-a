from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.dns_checks import (
    DNS_RECORD_TYPE,
    check_dns_port_listen,
    check_dns_record,
    check_host_record,
)


def task_A12_01(task: Task) -> Result:
    """DNS port check"""
    result = check_dns_port_listen(task)

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.1,
    )


def task_A12_02(task: Task) -> Result:
    """DNS zone check"""
    command = "rndc zonestatus dmz.worldskills.org."
    score = 0
    msg = f"{task.host.name} is NOT secondary name server for dmz.worldskills.org"
    if task.host.name == "ha-prx01":
        msg = f"{task.host.name} is NOT primary name server for dmz.worldskills.org"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if task.host.name == "ha-prx01" and "type: primary" in cmd_result.result:
            msg = f"{task.host.name} is primary name server for dmz.worldskills.org"
            score += 1
        if task.host.name == "ha-prx02" and "type: secondary" in cmd_result.result:
            msg = f"{task.host.name} is secondary name server for dmz.worldskills.org"
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


def task_A12_03(task: Task) -> Result:
    """Recurse resolver check"""
    command = "dig +recurse +time=2 +tries=1 @127.0.0.1 int.worldskills.org SOA"
    score = 0
    msg = f"{task.host} is a recursive name server!"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "recursion requested but not available" in cmd_result.result:
            msg = f"{task.host} is a not a recursive name server"
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


def task_A12_04(task: Task) -> Result:
    """A record for mail check"""
    hostname = "mail.dmz.worldskills.org."
    ip_addr = "10.1.20.10"
    result = check_host_record(
        task=task, record_type=DNS_RECORD_TYPE.A, hostname=hostname, ip_address=ip_addr
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_05(task: Task) -> Result:
    """A record for prx-vrrp check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="prx-vrrp.dmz.worldskills.org.",
        ip_address="10.1.20.20",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_06(task: Task) -> Result:
    """A record for ha-prx01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="ha-prx01.dmz.worldskills.org.",
        ip_address="10.1.20.21",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_07(task: Task) -> Result:
    """A record for ha-prx02 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="ha-prx02.dmz.worldskills.org.",
        ip_address="10.1.20.22",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_08(task: Task) -> Result:
    """A record for web01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="web01.dmz.worldskills.org.",
        ip_address="10.1.20.31",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_09(task: Task) -> Result:
    """A record for web02 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.A,
        hostname="web02.dmz.worldskills.org.",
        ip_address="10.1.20.32",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_10(task: Task) -> Result:
    """AAAA record for mail check"""
    hostname = "mail.dmz.worldskills.org."
    ip_addr = "2001:db8:1001:20::10"
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname=hostname,
        ip_address=ip_addr,
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_11(task: Task) -> Result:
    """AAAA record for prx-vrrp check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="prx-vrrp.dmz.worldskills.org.",
        ip_address="2001:db8:1001:20::20",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_12(task: Task) -> Result:
    """AAAA record for ha-prx01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="ha-prx01.dmz.worldskills.org.",
        ip_address="2001:db8:1001:20::21",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_13(task: Task) -> Result:
    """AAAA record for ha-prx02 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="ha-prx02.dmz.worldskills.org.",
        ip_address="2001:db8:1001:20::22",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_14(task: Task) -> Result:
    """AAAA record for web01 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="web01.dmz.worldskills.org.",
        ip_address="2001:db8:1001:20::31",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_15(task: Task) -> Result:
    """AAAA record for web02 check"""
    result = check_host_record(
        task=task,
        record_type=DNS_RECORD_TYPE.AAAA,
        hostname="web02.dmz.worldskills.org.",
        ip_address="2001:db8:1001:20::32",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.2,
    )


def task_A12_16(task: Task) -> Result:
    """CNAME record for web check"""
    result = check_dns_record(
        task=task,
        record_type=DNS_RECORD_TYPE.CNAME,
        query="www.dmz.worldskills.org.",
        expected="prx-vrrp.dmz.worldskills.org.",
    )

    return Result(
        host=task.host,
        result=result["msg"],
        command_run=result["command"],
        score=result["score"] / 10,
        max_score=0.1,
    )
