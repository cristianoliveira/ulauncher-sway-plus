from typing import Union

from sway import windows as sw
from sway.types import SwayNode
from utils.json_querier import find, find_all


def unmark(tag: str):
    """
    Unmark the current window with the given mark tag.
    :param tag: The tag of the mark to unmark.
    """

    # Get the current window ID
    def find_marked(node: SwayNode):
        if not isinstance(node, dict):
            return False
        if not isinstance(node.get("marks"), list):
            return False

        return tag in node["marks"]

    node: SwayNode = find(sw.get_tree_object(), find_marked)

    # Unmark the window using swaymsg
    sw.unmark(node["id"], tag)


def mark(tag: str):
    """
    Mark the current window with the given mark tag.
    :param tag: The tag of the mark to set.
    """

    # Get the current window ID
    def find_focused(node: SwayNode):
        if not isinstance(node, SwayNode):
            return False
        return node.get("focused", False)

    con = find(sw.get_tree_object(), find_focused)

    if con is None:
        raise ValueError("No focused window found")
    if not isinstance(con, dict):
        raise ValueError("Focused window is not a valid container object")

    # Set the mark using swaymsg
    sw.mark(con["id"], tag)


def focus(tag: str):
    """
    Focus the window with the given mark tag.
    :param tag: The tag of the mark to focus.
    """

    # Get the current window ID
    def find_marked(node):
        if not isinstance(node, dict):
            return False
        if not isinstance(node.get("marks"), list):
            return False

        return tag in node["marks"]

    con_id = find(sw.get_tree_object(), find_marked)

    # Focus the window using swaymsg
    sw.focus(con_id)


def get_marks(tag: Union[str, None] = None):
    """
    Get the list of marks.
    :return: A list of marks.
    """

    # Get the current window ID
    def find_marked(node: SwayNode):
        if not isinstance(node, dict):
            return False
        if not isinstance(node.get("marks"), list):
            return False
        if tag is not None and len(tag) > 0:
            return tag in node["marks"]

        return len(node.get("marks", [])) > 0

    return find_all(sw.get_tree_object(), find_marked)
