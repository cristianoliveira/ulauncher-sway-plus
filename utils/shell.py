import json
import subprocess
from typing import List


def execute_command(command: List[str]) -> str:
    """
    Execute a shell command and return the output and attempt to parse it as JSON.

    :param command: The shell command to execute.
    :return: The output of the command as a string or an empty string if the command fails.

    """
    try:
        result = subprocess.check_output(command)
        return json.loads(result.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        raise e
