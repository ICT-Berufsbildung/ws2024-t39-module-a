from processors.score_report import PrintScoreReport
from nornir import InitNornir
from nornir.core.filter import F


from tasks import (
    criterion_a1,
    criterion_a2,
    criterion_a3,
    criterion_a4,
    criterion_a5,
    criterion_a7,
    criterion_a8,
    criterion_a9,
    criterion_a10,
)

nr = InitNornir(
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "defaults_file": "inventory/defaults.yaml",
        },
    }
).with_processors([PrintScoreReport()])
# Inventory filters
host_int_srv = nr.filter(name="int-srv01")
host_fw = nr.filter(name="fw")
host_mail = nr.filter(name="mail")
host_jamie = nr.filter(name="jamie-ws01")
host_int_srv_vpn = nr.filter(F(name__eq="int-srv01") | F(name__eq="jamie-ws01"))

tasks_to_run_int_srv = [
    criterion_a1.task_A01_01,
    criterion_a1.task_A01_02,
    criterion_a1.task_A01_03,
    criterion_a1.task_A01_04,
    criterion_a1.task_A01_05,
    criterion_a2.task_A02_01,
    criterion_a2.task_A02_02,
    criterion_a2.task_A02_03,
    criterion_a2.task_A02_04,
    criterion_a2.task_A02_05,
    criterion_a2.task_A02_06,
    criterion_a3.task_A03_01,
    criterion_a3.task_A03_02,
    criterion_a3.task_A03_03,
    criterion_a3.task_A03_04,
    criterion_a3.task_A03_05,
    criterion_a3.task_A03_06,
    criterion_a4.task_A04_01,
    criterion_a4.task_A04_02,
    criterion_a4.task_A04_03,
    criterion_a4.task_A04_04,
    criterion_a4.task_A04_05,
    criterion_a4.task_A04_06,
    criterion_a4.task_A04_07,
    criterion_a4.task_A04_08,
    criterion_a4.task_A04_09,
    criterion_a4.task_A04_10,
]
# Run tasks
for task in tasks_to_run_int_srv:
    host_int_srv.run(task=task, on_failed=True)

# Firewall checks
tasks_to_run_fw = [
    criterion_a5.task_A05_01,
    criterion_a5.task_A05_02,
    criterion_a7.task_A07_01,
    criterion_a7.task_A07_02,
]
for task in tasks_to_run_fw:
    host_fw.run(task=task, on_failed=True)

# VPN - E2E check
host_jamie.run(task=criterion_a7.task_A07_03, on_failed=True)
# VPN check
host_fw.run(task=criterion_a7.task_A07_04, on_failed=True)
# Transparent Proxy checks
host_int_srv_vpn.run(task=criterion_a8.task_A08_01, on_failed=True)
# Mail test
host_mail.run(criterion_a9.task_A09_01, on_failed=True)
# E2E test
host_jamie.run(criterion_a9.task_A09_02, on_failed=True)
