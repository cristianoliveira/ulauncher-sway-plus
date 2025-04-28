from utils.json_querier import find_all
from utils.shell import execute_command


def get_outputs(active: bool = True):
    """
    Get the list of outputs (monitors) from Sway.
    Returns a list of dicts: each dict describes an output.

    :param active: If True, return only active outputs. If False, return only inactive outputs.

    :return: A list of outputs (monitors) from Sway.
    """
    data = execute_command(["swaymsg", "-t", "get_outputs"])

    def find_active(output: dict):
        if not isinstance(output, dict):
            return False
        return output["active"] == active if output.get("active") is not None else False

    return find_all(data, find_active)


def set_output_enabled(name, enabled: bool):
    """
    Enable or disable the output with the given name.
    'enabled' is True to enable, False to disable.

    :param name: The name of the output to enable/disable.
    :param enabled: True to enable, False to disable.

    :return: The result of the command execution.
    """
    status = "enable" if enabled else "disable"
    return execute_command(["swaymsg", "output", name, status])
