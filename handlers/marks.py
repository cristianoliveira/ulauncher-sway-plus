from typing import List

from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

import sway.marks as sway_marks

# Enum
MARKS_ID = "sway-marks"
MARKS_EVENT_NAME = "sway-marks-name"
MARKS_EVENT_CONFIRM = "sway-marks-confirm"
MARKS_EVENT_FOCUS = "sway-marks-focus"
MARKS_EVENT_UNMARK = "sway-marks-unmark"

MARKS_CMD_MARK = "mark:"
MARKS_CMD_UNMARK = "unmark:"

def list_options(cmd_keyword: str):
    marks = sway_marks.get_marks()
    options = [
        ExtensionResultItem(
            icon='images/icon.png',
            name=f"[{_join_mark_name(mark['marks'])}] {mark['name']}",
            description="Focus this window",
            on_enter=ExtensionCustomAction((MARKS_EVENT_FOCUS, mark), keep_app_open=False),
        ) for mark in marks if isinstance(mark, dict) and mark.get("name") is not None
    ]

    options.extend([
        ExtensionResultItem(
            icon=None,
            name="Mark",
            description="Mark current window",
            on_enter=SetUserQueryAction(f"{cmd_keyword} {MARKS_CMD_MARK} "),
        ),
        ExtensionResultItem(
            icon=None,
            name="Unmark",
            description="Unmark from an list of marked window",
            on_enter=SetUserQueryAction(f"{cmd_keyword} {MARKS_CMD_UNMARK} "),
        ), 
    ])

    return RenderResultListAction(options)


def collect_mark_name_for_window(mark_name: str):
    """
    Collect the mark name for the current window.

    :param mark_name: The name of the mark to set.
    """
    return RenderResultListAction([
        ExtensionResultItem(
            icon='images/icon.png',
            name="The current window will be marked as...",
            on_enter=ExtensionCustomAction((MARKS_EVENT_CONFIRM, mark_name), keep_app_open=False),
        )
    ])

def unmark_window_confirmation(mark_name: str):
    """
    Mark the current window with the given mark name.

    :param mark_name: The name of the mark to set.
    """
    marks = sway_marks.get_marks(mark_name)
    return RenderResultListAction([
        ExtensionResultItem(
            icon='images/icon.png',
            name=f"[{_join_mark_name(mark['marks'])}] {mark['name']}",
            description="Select the marked window to unmark",
            on_enter=ExtensionCustomAction((MARKS_EVENT_UNMARK, mark), keep_app_open=False),
        ) for mark in marks if isinstance(mark, dict) and mark.get("name") is not None
    ])

def _join_mark_name(name: List[str]):
    return "-".join(name).strip()

def list_marked_windows():
    """
    List all marked windows.
    """
    marks = sway_marks.get_marks()
    return RenderResultListAction([
        ExtensionResultItem(
            icon='images/icon.png',
            name=f"{_join_mark_name(mark['marks'])} {mark['name']}",
            description="Focus this window",
            on_enter=ExtensionCustomAction((MARKS_EVENT_FOCUS, mark), keep_app_open=False),
        ) for mark in marks if isinstance(mark, dict) and mark.get("name") is not None
    ])
