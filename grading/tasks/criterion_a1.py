from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.ldap_checks import (
    check_ldap_login,
    check_ldap_user_attributes,
    check_ldap_user_exists,
)
from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


BASE_DN = "dc=int,dc=worldskills,dc=org"
ADMIN_DN = "cn=admin,dc=int,dc=worldskills,dc=org"
ADMIN_PW = "Skill39"


def task_A01_01(task: Task) -> Result:
    """LDAP check"""
    command = r"""timeout 2 bash -c "echo -e '\x1dclose\x0d' | telnet 127.0.0.1 389" && timeout 2 bash -c "echo -e '\x1dclose\x0d' | telnet ::1 389" """
    try:
        task.run(task=paramiko_command, command=command)
        # Exit code is 0
        got_mark = True
    except Exception:
        # Exit code is 1
        got_mark = False

    return Result(
        host=task.host,
        result="LDAP port tcp/389 is reachable"
        if got_mark
        else "LDAP port tcp/389 is NOT reachable",
        command_run=command,
        command_output=process_result_exit_code(got_mark),
        score=0.1 if got_mark else 0.0,
        max_score=0.1,
    )


def task_A01_02(task: Task) -> Result:
    """OU Employees exists"""
    ou_name = "Employees"
    base_command = f'ldapsearch -H ldap://localhost -b {BASE_DN} -x "(&(objectclass=organizationalunit)(ou={ou_name}))"'
    command = f"{base_command} -D {ADMIN_DN} -w {ADMIN_PW}"

    got_mark = False
    cmd_result = None
    try:
        # Redirect stderr to stdout
        cmd_result = task.run(
            task=paramiko_command, command=f"({command} || {base_command}) 2>&1"
        )
        # Check if ou exits
        got_mark = (
            True
            if "dn: ou=Employees,dc=int,dc=worldskills,dc=org" in cmd_result.result
            else False
        )
    except Exception:
        got_mark = False

    return Result(
        host=task.host,
        result="OU Employees exists" if got_mark else "OU Employees DOES NOT exists",
        command_run=command,
        command_output=cmd_result.result if cmd_result else UNKNOWN_MSG,
        score=0.25 if got_mark else 0.0,
        max_score=0.25,
    )


def task_A01_03(task: Task) -> Result:
    """Check if user jamie, peter and admin exists"""
    results = [check_ldap_user_exists(task=task, username="jamie")]
    results.append(check_ldap_user_exists(task=task, username="peter"))
    results.append(check_ldap_user_exists(task=task, username="admin"))

    return Result(
        host=task.host,
        result=", ".join([res["msg"] for res in results]),
        command_run=[res["command"] for res in results],
        command_output=[res["command_output"] for res in results],
        score=0.2 if sum([res["score"] for res in results]) == 3 else 0.0,
        max_score=0.2,
    )


def task_A01_04(task: Task) -> Result:
    """Check if user jamie and peter have correct attributes"""

    results = [
        check_ldap_user_attributes(
            task=task, username="jamie", mail="jamie.oliver@dmz.worldskills.org"
        )
    ]
    results.append(
        check_ldap_user_attributes(
            task=task, username="peter", mail="peter.fox@dmz.worldskills.org"
        )
    )

    return Result(
        host=task.host,
        result=", ".join([res["msg"] for res in results]),
        command_run=[res["command"] for res in results],
        command_output=[res["command_output"] for res in results],
        score=0.4 if sum([res["score"] for res in results]) == 2 else 0.0,
        max_score=0.4,
    )


def task_A01_05(task: Task) -> Result:
    """Check if ldap users can login"""
    results = [check_ldap_login(task=task, username="jamie")]
    results.append(check_ldap_login(task=task, username="peter"))
    results.append(check_ldap_login(task=task, username="admin"))

    return Result(
        host=task.host,
        result=", ".join([res["msg"] for res in results]),
        command_run=[item for res in results for item in res["command"]],
        command_output=[item for res in results for item in res["command_output"]],
        score=0.25 if sum([res["score"] for res in results]) == 3 else 0.0,
        max_score=0.25,
    )
