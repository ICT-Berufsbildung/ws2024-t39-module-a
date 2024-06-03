from nornir.core.task import Task, Result
from nornir_paramiko.plugins.tasks import paramiko_command


def task_A02_01(task: Task) -> Result:
    """Root CA check"""
    command = (
        "openssl x509 -in /opt/grading/ca/ca.pem -noout -ext basicConstraints,keyUsage"
    )
    score = 0
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        # Exit code is 0
        score += 1
        msg = "Root CA exists"
        if "CA:TRUE" in cmd_result.result and "Certificate Sign" in cmd_result.result:
            score += 1
            msg = "Root CA exists and has correct attributes."
    except Exception:
        # Exit code is 1
        score += 0
        msg = "Root CA DOES NOT exist"

    return Result(
        host=task.host,
        id="A1_01",
        result=msg,
        command_run=command,
        score=score / 10,
        max_score=0.2,
    )


def task_A02_02(task: Task) -> Result:
    """Users CA check"""
    command = "openssl x509 -in /opt/grading/ca/users.pem -noout -ext basicConstraints,keyUsage"
    score = 0
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        # Exit code is 0
        score += 1
        msg = "Users Sub CA exists"
        if "CA:TRUE" in cmd_result.result and "Certificate Sign" in cmd_result.result:
            score += 1
            msg = "Users Sub CA exists and has correct attributes."
    except Exception:
        # Exit code is 1
        score += 0
        msg = "Sub CA DOES NOT exist"

    verify_command = (
        "openssl verify -CAfile /opt/grading/ca/ca.pem /opt/grading/ca/users.pem"
    )
    try:
        cmd_result = task.run(task=paramiko_command, command=verify_command)
        if "/opt/grading/ca/users.pem: OK" in cmd_result.result:
            score += 1
            msg += " Users Sub CA is signed by Root CA"
    except Exception:
        # Exit code is 1
        score += 0

    return Result(
        host=task.host, result=msg, command_run=command, score=score / 10, max_score=0.3
    )


def task_A02_03(task: Task) -> Result:
    """Services CA check"""
    command = "openssl x509 -in /opt/grading/ca/services.pem -noout -ext basicConstraints,keyUsage"
    score = 0
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        # Exit code is 0
        score += 1
        msg = "Services Sub CA exists"
        if "CA:TRUE" in cmd_result.result and "Certificate Sign" in cmd_result.result:
            score += 1
            msg = "Services Sub CA exists and has correct attributes."
    except Exception:
        # Exit code is 1
        score += 0
        msg = "Sub CA DOES NOT exist"

    verify_command = (
        "openssl verify -CAfile /opt/grading/ca/ca.pem /opt/grading/ca/services.pem"
    )
    try:
        cmd_result = task.run(task=paramiko_command, command=verify_command)
        if "/opt/grading/ca/services.pem: OK" in cmd_result.result:
            score += 1
            msg += " Services Sub CA is signed by Root CA"
    except Exception:
        # Exit code is 1
        score += 0

    return Result(
        host=task.host, result=msg, command_run=command, score=score / 10, max_score=0.3
    )


def task_A02_04(task: Task) -> Result:
    """jamie cert check"""
    command = "openssl x509 -in /opt/grading/ca/jamie.pem -noout -subject -ext keyUsage,extendedKeyUsage"
    score = 0
    msg = "jamie cert DOES NOT exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "jamie.oliver@dmz.worldskills.org" in cmd_result.result:
            # Exit code is 0
            score += 1
            msg = "jamie cert exists"
        if "TLS Web Client Authentication" in cmd_result.result:
            score += 1
            msg = "jamie cert exists and is entitled to use mTLS."
    except Exception:
        # Exit code is 1
        score += 0

    verify_command = "openssl verify -CAfile <(cat /opt/grading/ca/users.pem /opt/grading/ca/ca.pem) /opt/grading/ca/jamie.pem"
    try:
        cmd_result = task.run(task=paramiko_command, command=verify_command)
        if "/opt/grading/ca/jamie.pem: OK" in cmd_result.result:
            score += 1
            msg += " jamie cert is fully valid (signed)"
    except Exception:
        # Exit code is 1
        score += 0

    return Result(
        host=task.host, result=msg, command_run=command, score=score / 10, max_score=0.3
    )


def task_A02_05(task: Task) -> Result:
    """webserver cert check"""
    command = "openssl x509 -in /opt/grading/ca/web.pem -noout -subject"
    score = 0
    msg = "webserver cert DOES NOT exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "www.dmz.worldskills.org" in cmd_result.result:
            # Exit code is 0
            score += 1
            msg = "webserver cert exists"
    except Exception:
        # Exit code is 1
        score += 0

    verify_command = "openssl verify -CAfile <(cat /opt/grading/ca/services.pem /opt/grading/ca/ca.pem) /opt/grading/ca/web.pem"
    try:
        cmd_result = task.run(task=paramiko_command, command=verify_command)
        if "/opt/grading/ca/web.pem: OK" in cmd_result.result:
            score += 1
            msg += " webserver cert is fully valid (signed)"
    except Exception:
        # Exit code is 1
        score += 0

    return Result(
        host=task.host, result=msg, command_run=command, score=score / 10, max_score=0.2
    )


def task_A02_06(task: Task) -> Result:
    """mailserver cert check"""
    command = "openssl x509 -in /opt/grading/ca/mail.pem -noout -subject"
    score = 0
    msg = "mailserver cert DOES NOT exist"
    try:
        cmd_result = task.run(task=paramiko_command, command=command)
        if "mail.dmz.worldskills.org" in cmd_result.result:
            # Exit code is 0
            score += 1
            msg = "mailserver cert exists"
    except Exception:
        # Exit code is 1
        score += 0

    verify_command = "openssl verify -CAfile <(cat /opt/grading/ca/services.pem /opt/grading/ca/ca.pem) /opt/grading/ca/mail.pem"
    try:
        cmd_result = task.run(task=paramiko_command, command=verify_command)
        if "/opt/grading/ca/mail.pem: OK" in cmd_result.result:
            score += 1
            msg += "\nmailserver cert is fully valid (signed)"
    except Exception:
        # Exit code is 1
        score += 0

    return Result(
        host=task.host, result=msg, command_run=command, score=score / 10, max_score=0.2
    )
