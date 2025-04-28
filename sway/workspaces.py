import json
import subprocess
from typing import List, Optional


def get_outputs(active: Optional[bool] = None) -> List[dict]:
    """
    List the available outputs.

    :param active: If None, return all outputs. If True, return only active outputs. If False, return only inactive outputs.
    """

    result = subprocess.check_output(["swaymsg", "-t", "get_outputs"])
    json_result = json.loads(result)

    if active is None:
        return json_result

    return [output for output in json_result if output["active"] == active]


def send_workspace_to_output(output_name: str):
    """
    Send the current workspace to the specified output.

    :param output_name: The name of the output to send the workspace to.
    """
    subprocess.check_output(
        ["swaymsg", "move", "workspace", f"to output {output_name}"]
    )
