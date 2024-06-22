import enum
import re
from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command

from tasks.common.helper import UNKNOWN_MSG, process_result_exit_code


BASE_DN = "dc=int,dc=worldskills,dc=org"
ADMIN_DN = "cn=admin,dc=int,dc=worldskills,dc=org"
ADMIN_PW = "Skill39"


class LDAP_ATTR(enum.StrEnum):
    MAIL_EXISTS = "mail"
    OU_EXISTS = "ou"
    UID_EXISTS = "uid"
    CN_EXISTS = "cn"
    LOGIN_FAILED = "login"


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
    """User Jamie exists"""
    username = "jamie"
    base_command = f'ldapsearch -H ldap://localhost -b {BASE_DN} -x "(&(objectclass=inetOrgPerson)(uid={username}))"'
    command_with_user = f"{base_command} -D {ADMIN_DN} -w {ADMIN_PW}"
    command = f"({command_with_user} || {base_command}) 2>&1"
    missing_attr = []
    cn = ""
    score = 0
    commands = [command]
    command_outputs = []
    try:
        # Redirect stderr to stdout
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        # Check if ou exits
        if "uid: jamie\n" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.UID_EXISTS)

        # Mail attribute is set
        if "mail: jamie.oliver@dmz.worldskills.org\n" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.MAIL_EXISTS)

        # member of OU Employees
        if "ou=Employees,dc=int,dc=worldskills,dc=org" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.OU_EXISTS)

        if len(missing_attr) == 0:
            score = 0.2

        # Get configured DN for the user
        re_cn = re.findall(r"^dn: (.*)$", str(cmd_result.result), re.MULTILINE)
        if len(re_cn) > 0:
            cn = re_cn[0]
        else:
            missing_attr.append(LDAP_ATTR.CN_EXISTS)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    login_works = False
    if cn:
        # Try to login
        login_command = f"{base_command} -D {cn} -w {ADMIN_PW}"
        commands.append(login_command)
        try:
            task.run(task=paramiko_command, command=f"{login_command}")
            score += 0.1
            login_works = True
        except Exception:
            # Login failed
            missing_attr.append(LDAP_ATTR.LOGIN_FAILED)
        command_outputs.append(process_result_exit_code(login_works))
    # Prepare message
    msg = "User jamie DOES NOT exists"
    if login_works and cn:
        msg = "User Jamie exists and can login"
    elif cn and not login_works:
        msg = "User Jamie exists, but cannot login"
    elif score != 0:
        msg = (
            f"User jamie exists, but attributes are missing: {', '.join(missing_attr)}"
        )
    else:
        msg = "User jamie DOES NOT exists"

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.3,
    )


def task_A01_04(task: Task) -> Result:
    """User peter exists"""
    username = "peter"
    base_command = f'ldapsearch -H ldap://localhost -b {BASE_DN} -x "(&(objectclass=inetOrgPerson)(uid={username}))"'
    command_with_user = f"{base_command} -D {ADMIN_DN} -w {ADMIN_PW}"
    command = f"({command_with_user} || {base_command}) 2>&1"
    missing_attr = []
    cn = ""
    score = 0
    commands = [command]
    command_outputs = []
    try:
        # Redirect stderr to stdout
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)
        # Check if ou exits
        if "uid: peter\n" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.UID_EXISTS)

        # Mail attribute is set
        if "mail: peter.fox@dmz.worldskills.org\n" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.MAIL_EXISTS)

        # member of OU Employees
        if "ou=Employees,dc=int,dc=worldskills,dc=org" not in cmd_result.result:
            missing_attr.append(LDAP_ATTR.OU_EXISTS)

        if len(missing_attr) == 0:
            score = 0.2

        # Get configured DN for the user
        re_cn = re.findall(r"^dn: (.*)$", str(cmd_result.result), re.MULTILINE)
        if len(re_cn) > 0:
            cn = re_cn[0]
        else:
            missing_attr.append(LDAP_ATTR.CN_EXISTS)
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    login_works = False
    if cn:
        # Try to login
        login_command = f"{base_command} -D {cn} -w {ADMIN_PW}"
        commands.append(login_command)
        try:
            task.run(task=paramiko_command, command=f"{login_command}")
            score += 0.1
            login_works = True
        except Exception:
            # Login failed
            missing_attr.append(LDAP_ATTR.LOGIN_FAILED)
        command_outputs.append(process_result_exit_code(login_works))
    # Prepare message
    msg = "User peter DOES NOT exists"
    if login_works and cn:
        msg = "User peter exists and can login"
    elif cn and not login_works:
        msg = "User peter exists, but cannot login"
    elif score != 0:
        msg = (
            f"User peter exists, but attributes are missing: {', '.join(missing_attr)}"
        )
    else:
        msg = "User peter DOES NOT exists"

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.3,
    )


def task_A01_05(task: Task) -> Result:
    """User admin exists"""
    username = "admin"
    base_command = f'ldapsearch -H ldap://localhost -b cn={username},{BASE_DN} -x "(objectclass=*)"'
    command_with_user = f"{base_command} -D {ADMIN_DN} -w {ADMIN_PW}"
    command = f"({command_with_user} || {base_command}) 2>&1"
    missing_attr = []
    cn = ""
    score = 0
    commands = [command]
    command_outputs = []
    try:
        # Redirect stderr to stdout
        cmd_result = task.run(task=paramiko_command, command=command)
        command_outputs.append(cmd_result.result)

        # Get configured DN for the user
        re_cn = re.findall(r"^dn: (.*)$", str(cmd_result.result), re.MULTILINE)
        if len(re_cn) > 0:
            cn = re_cn[0]
        else:
            missing_attr.append(LDAP_ATTR.CN_EXISTS)
        # Check if ou exits
        if f"dn: cn={username},{BASE_DN}\n" in cmd_result.result:
            score += 0.1
    except Exception:
        command_outputs.append(UNKNOWN_MSG)

    login_works = False
    if cn:
        # Try to login
        login_command = f"{base_command} -D {cn} -w {ADMIN_PW}"
        commands.append(login_command)
        try:
            task.run(task=paramiko_command, command=f"{login_command}")
            score += 0.1
            login_works = True
        except Exception:
            # Login failed
            missing_attr.append(LDAP_ATTR.LOGIN_FAILED)
        command_outputs.append(process_result_exit_code(login_works))
    # Prepare message
    msg = "User admin DOES NOT exists"
    if login_works and cn:
        msg = "User admin exists and can login"
    elif cn and not login_works:
        msg = "User admin exists, but cannot login"
    elif score != 0:
        msg = (
            f"User admin exists, but attributes are missing: {', '.join(missing_attr)}"
        )
    else:
        msg = "User admin DOES NOT exists"

    return Result(
        host=task.host,
        result=msg,
        command_run=commands,
        command_output=command_outputs,
        score=score,
        max_score=0.2,
    )
