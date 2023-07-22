from pluggy import HookimplMarker
from typing import Any

hookimpl = HookimplMarker("ansible")


@hookimpl
def ansible_pre_run(
    ansible_command: str, ansible_arguments: list, ansible_callback: Any
) -> None:
    print("HOOK: Playbook started : " + ansible_command)
    print("HOOK: Playbook arguments : " + str(ansible_arguments))
    print("HOOK: Callback : " + str(ansible_callback))
