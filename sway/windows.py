import json
import subprocess

from sway.util import get_child_or_else
from utils.json_querier import find


def unmark(con_id: str, name: str):
    """
    Unmark the current window with the given mark name.
    :param name: The name of the mark to unmark.
    """
    # Unmark the window using swaymsg
    subprocess.run(["swaymsg", f'[con_id="{con_id}"]', "unmark", name])


def mark(con_id: str, name: str):
    """
    Mark the current window with the given mark name.
    :param name: The name of the mark to set.
    """
    # Set the mark using swaymsg
    subprocess.run(["swaymsg", f'[con_id="{con_id}"]', "mark", name])


def focus_mark(name: str):
    """
    Focus the window with the given mark name.
    :param name: The name of the mark to focus.
    """
    # Focus the window using swaymsg
    subprocess.run(["swaymsg", f'[con_mark="{name}"]', "focus"])


def focus(con):
    """Returns the list of args to pass to swaymsg"""

    # Container objects have 3 different ID fields:
    #   id - the container ID, called con_id in criteria syntax
    #   app_id - specific to wayland apps
    #   ??? - specific to X11 apps, called id in criteria syntax
    con_id = con["id"]

    # invokes: '<criteria> focus' (documented in sway(5))
    subprocess.check_output(["swaymsg", f'[con_id="{con_id}"]', "focus"])


def get_focused():
    """
    Mark the current window with the given mark tag.
    :param tag: The tag of the mark to set.
    """

    # Get the current window ID
    def find_focused(node):
        if not isinstance(node, dict):
            return False
        return node.get("focused", False)

    con = find(get_tree_object(), find_focused)

    return con


def get_tree_object():
    return json.loads(subprocess.check_output(["swaymsg", "-t", "get_tree"]))


def get_windows(tree=None):
    tree = get_tree_object() if tree == None else tree
    windows = []

    for output in tree["nodes"]:
        assert output["type"] == "output", "Expected output, got" + repr(output)

        for workspace in output["nodes"]:
            assert workspace["type"] == "workspace", "Expected workspace, got" + repr(
                workspace
            )

            for container in get_child_or_else(workspace, "nodes", []):
                windows += get_container_windows(container)

            for container in get_child_or_else(workspace, "floating_nodes", []):
                windows += get_container_windows(container)

    return windows


def get_windows_by_workspace(workspace_name):
    """
    Get all windows in the specified workspace.
    :param workspace_name: The name of the workspace to search.
    :return: A list of windows in the specified workspace.
    """
    tree = get_tree_object()
    windows = []
    for output in tree["nodes"]:
        for workspace in output["nodes"]:
            assert workspace["type"] == "workspace", "Expected workspace, got" + repr(
                workspace
            )

            if workspace["name"] == workspace_name:
                for container in get_child_or_else(workspace, "nodes", []):
                    windows += get_container_windows(container)

                for container in get_child_or_else(workspace, "floating_nodes", []):
                    windows += get_container_windows(container)

    return windows


def get_container_windows(con):
    windows = []

    # Check if the container is an application in its own right
    if "app_id" in con.keys():
        windows.append(con)

    # Recurse
    for child in con["nodes"]:
        windows += get_container_windows(child)

    return windows


def app_details(con):
    # app_id is wayland only, window_properties is X11 only
    app_name = (
        con["app_id"]
        if ("app_id" in con and con["app_id"] != None)
        else con["window_properties"].get("instance", "unknown")
    )

    # (con_id, application name, window title)
    return (con["id"], app_name, con["name"])


if __name__ == "__main__":
    tree = get_tree_object()
    wins = get_windows(tree)

    for w in wins:
        print(app_details(w))
