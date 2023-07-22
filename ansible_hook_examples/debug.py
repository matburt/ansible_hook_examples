from pluggy import HookimplMarker
from typing import Any

import sys

hookimpl = HookimplMarker("ansible")

breakpoints = {}


def repl(stdin_actual: Any, prompt_prefix: str, *args, **kwargs):
    for k, v in kwargs.items():
        locals()[k] = v
    print(f"Available Properties: {', '.join(kwargs.keys())}")
    try:
        while True:
            try:
                sys.stdout.write(f"{prompt_prefix}>> ")
                sys.stdout.flush()
                _in = stdin_actual.readline()
                if _in.strip() in ["exit", "c", "q", "quit"]:
                    break
                try:
                    print(eval(_in))
                except:
                    out = exec(_in)
                    if out is not None:
                        print(out)
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")


@hookimpl
def ansible_play_pre_run(vars: Any, inventory: Any, play: Any) -> None:
    repl(
        sys.stdin,
        f"pre_play[{play.get_name()}]",
        vars=vars,
        inventory=inventory,
        play=play,
    )


@hookimpl
def ansible_task_pre_run(task: Any, host: Any, executor: Any) -> None:
    if (
        task.get_variable_manager() is not None
        and host.name in task.get_variable_manager().get_vars()["hostvars"]
    ):
        actual_hostvars = task.get_variable_manager().get_vars()["hostvars"][host.name]
    else:
        actual_hostvars = {}
    repl(
        executor._new_stdin,
        f"pre_task[{task.action}({task.name}<{host.name}>)]",
        host=host,
        hostvars=actual_hostvars,
        task=task,
    )
