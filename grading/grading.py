from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

from tasks import criterion_a1

nr = InitNornir(
    inventory={"plugin": "SimpleInventory", "options": {"host_file": "inventory/hosts.yaml", "defaults_file": "inventory/defaults.yaml"}}
)
host_int_srv = nr.filter(name="int-srv01")
results = host_int_srv.run(
    task=criterion_a1.task_A1_01
)
print_result(results, vars=["point"])