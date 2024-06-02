from processors.score_report import PrintScoreReport
from nornir import InitNornir

from tasks import criterion_a1

nr = InitNornir(
    inventory={"plugin": "SimpleInventory", "options": {"host_file": "inventory/hosts.yaml", "defaults_file": "inventory/defaults.yaml"}}
).with_processors([PrintScoreReport()])
# Inventory filters
host_int_srv = nr.filter(name="int-srv01")
tasks_to_run_int_srv = [criterion_a1.task_A1_01, criterion_a1.task_A1_02, criterion_a1.task_A1_03, criterion_a1.task_A1_04, criterion_a1.task_A1_05]
# Run tasks
for task in tasks_to_run_int_srv:
    host_int_srv.run(
        task=task
    )
