import os
import sys
from typing import Dict

from line import Line


def handler(event: Dict, context):
    _check_envs()

    print(event)
    line: Line = Line()
    return line.message_handler(event, context)


def _check_envs():
    task_root = _check_env("LAMBDA_TASK_ROOT", is_check=False)
    home = _check_env("HOME", is_check=False)
    _check_env("LINE_CHANNEL_ACCESS_TOKEN")
    _check_env("LINE_CHANNEL_SECRET")
    _check_env("LINE_SEND_ID_1")
    _check_env("LINE_SEND_GROUP_ID_1")
    _check_env("LIBRARY_CHECK_RENTAL_FUNCTION_ARN")
    _check_env("LIBRARY_CHECK_EXPIRE_FUNCTION_ARN")
    _check_env("LIBRARY_CHECK_RESERVE_FUNCTION_ARN")
    _check_env("LIBRARY_CHECK_PREPARE_FUNCTION_ARN")

    if False:
        os.system(f"ls -al {task_root}")
        os.system(f"ls -al {home}")


def _check_env(key: str, is_check: bool = True) -> str:
    value = os.environ.get(key, "")
    if is_check:
        if not value:
            print(f"Not found environment variable: ({key} = {value})")
            sys.exit(1)
    print(f"env | {key}: {value}")
    return value
