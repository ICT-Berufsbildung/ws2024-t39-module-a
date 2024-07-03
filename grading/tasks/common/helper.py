# Constants
UNKNOWN_MSG = "unknown"


def process_result_exit_code(success: bool) -> str:
    return "Exit code was 0" if success else "Exit code was NOT 0"
