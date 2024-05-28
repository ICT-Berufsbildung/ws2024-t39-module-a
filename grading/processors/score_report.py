import logging
import threading
from typing import Union, cast

from colorama import Fore, Style, init

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Result, Task

init(autoreset=True, strip=False)


def _get_color(result: Union[MultiResult, Result]) -> str:
    color = Fore.GREEN
    if result.failed:
        color = Fore.RED
        
    return cast(str, color)


class PrintScoreReport:
    """
    Prints score report.
    """

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.even = False
        self.lock = threading.Lock()
        banner = """
_ _ _ ____ ____    _  _ ____ ___  _  _ _    ____    ____ 
| | | [__  |       |\/| |  | |  \ |  | |    |___    |__| 
|_|_| ___] |___    |  | |__| |__/ |__| |___ |___    |  |

____ ____ ____ ____ ____    ____ ____ ___  ____ ____ ___ 
[__  |    |  | |__/ |___    |__/ |___ |__] |  | |__/  |  
___] |___ |__| |  \ |___    |  \ |___ |    |__| |  \  |                                                                                                                   
"""
        print(f"{Style.BRIGHT}{Fore.BLUE}{banner}")
        print(f"{'=' * (75)}")

    def task_started(self, task: Task) -> None:
        return

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        return

    def task_instance_started(self, task: Task, host: Host) -> None:
        return

    def task_instance_completed(
        self, task: Task, host: Host, results: MultiResult
    ) -> None:
        self.lock.acquire()
        for res in results:
            # Skip any non WSC marking tasks
            if not hasattr(res, "id") and not hasattr(res, "score"):
                continue

            # Get attributes
            id = getattr(results, "id", "??")
            score = getattr(results, "score", 0.0)
            max_score = getattr(results, "max_score", 0.0)
            color = Fore.GREEN if score == max_score else Fore.RED

            # print task
            msg = f"=> [{id}] {results.result}:{''.ljust(60 - len(results.result))}{Style.BRIGHT}{color}{score}"
            print(msg)
            placeholder = "=" if self.even else "-"
            self.even = not self.even
            print(f"{placeholder * (75)}")

        self.lock.release()

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        self.task_instance_started(task, host)

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        self.task_instance_completed(task, host, result)