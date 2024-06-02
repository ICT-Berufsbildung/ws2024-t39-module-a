from processors.score_report import PrintScoreReport
from nornir import InitNornir

from tasks import criterion_a1, criterion_a2, criterion_a3, criterion_a4

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
tasks_to_run_int_srv = [
    criterion_a1.task_A1_01,
    criterion_a1.task_A1_02,
    criterion_a1.task_A1_03,
    criterion_a1.task_A1_04,
    criterion_a1.task_A1_05,
    criterion_a2.task_A2_01,
    criterion_a2.task_A2_02,
    criterion_a2.task_A2_03,
    criterion_a2.task_A2_04,
    criterion_a2.task_A2_05,
    criterion_a2.task_A2_06,
    criterion_a3.task_A3_01,
    criterion_a3.task_A3_02,
    criterion_a3.task_A3_03,
    criterion_a3.task_A3_04,
    criterion_a3.task_A3_05,
    criterion_a3.task_A3_06,
    criterion_a4.task_A4_01,
    criterion_a4.task_A4_02,
    criterion_a4.task_A4_03,
    criterion_a4.task_A4_04,
    criterion_a4.task_A4_05,
    criterion_a4.task_A4_06,
    criterion_a4.task_A4_07,
    criterion_a4.task_A4_08,
    criterion_a4.task_A4_09,
    criterion_a4.task_A4_10,
]
# Run tasks
for task in tasks_to_run_int_srv:
    host_int_srv.run(task=task, on_failed=True)
