from typing import List

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import sway.icons as sway_icons
import sway.windows as windows
from utils.filterer import filter_result_list


def get_result_item(con):
    (_, appName, winTitle) = windows.app_details(con)

    return ExtensionResultItem(
        icon=sway_icons.get_icon(con),
        name=winTitle,
        description=appName,
        # This only works because con is a dict, and therefore pickleable
        on_enter=ExtensionCustomAction(("sway-windows", con)),
    )


def show_opened_windows(extension, query: List[str]):
    """
    Show the most used windows

    :param extension: The extension instance
    :param query: The search query
    :return: The list of opened windows
    """

    opened_windows = windows.get_windows()
    most_used_windows = extension.sorter.sort(opened_windows, by_key="app_id")

    items = list(
        [
            get_result_item(w)
            for w in most_used_windows
            # Don't include the ulauncher dialog in the list,
            # since it already has focus
            if not w["focused"]
        ]
    )

    # Sort the items by usage
    return filter_result_list(RenderResultListAction(items), query)


SCRATCHPAD_HANDLER_ID = "sway-scratchpad"


def show_scratchpad_windows(extension, query: List[str]):
    """
    Show the most used windows in the scratchpad

    :param extension: The extension instance
    :param query: The search query
    :return: The list of scratchpad windows
    """

    scratchpads = windows.get_windows_by_workspace("__i3_scratch")
    most_used_windows = extension.sorter.sort(scratchpads, by_key="app_id")

    items = list(
        [
            get_result_item(w)
            for w in most_used_windows
            # Don't include the ulauncher dialog in the list,
            # since it already has focus
            if not w["focused"]
        ]
    )

    # Sort the items by usage
    return filter_result_list(RenderResultListAction(items), query)


def focus_selected_window(extension, con: dict[str, str]):
    """
    Focus the selected window and add it to the sorter

    :param con: The sway window container
    """

    extension.sorter.add(con["app_id"])
    windows.focus(con)
