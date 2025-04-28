import logging
from typing import Union

import gi

gi.require_version("Gdk", "3.0")

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)

import handlers.marks as handle_marks
import handlers.outputs as handle_outputs
import handlers.windows as handle_windows
import handlers.workspaces as handle_workspaces
import sway.marks as sway_marks
from utils.sorter import sort_strategy

logger = logging.getLogger(__name__)


class SwayWindowsExtension(Extension):

    sorter = sort_strategy("default")

    def __init__(self):
        super(SwayWindowsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class PreferencesEventListener(EventListener):
    def on_event(
        self,
        event: Union[PreferencesEvent, PreferencesUpdateEvent],
        extension: "SwayWindowsExtension",
    ) -> None:
        if isinstance(event, PreferencesUpdateEvent):
            if event.id == "keyword":
                return
            extension.preferences[event.id] = event.new_value
        elif isinstance(event, PreferencesEvent):
            assert isinstance(event.preferences, dict)
            extension.preferences = event.preferences
        # Could be optimized so it only refreshes the custom paths
        extension.sorter = sort_strategy(extension.preferences["sort_by"])


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        raw_query = event.get_query()
        query = raw_query.get_argument("").lower().split()

        event_keyword = event.get_keyword()

        if event_keyword == extension.preferences.get(
            handle_marks.MARKS_ID
        ):  # Sway Marks
            subcmd = None

            if (
                handle_marks.MARKS_CMD_MARK in query
                or handle_marks.MARKS_CMD_UNMARK in query
            ):
                subcmd = query.pop(0)

            should_show_subcmd = raw_query.endswith(" ") or len(query) > 0

            if subcmd == handle_marks.MARKS_CMD_MARK and should_show_subcmd:
                return handle_marks.collect_mark_name_for_window(" ".join(query))

            if subcmd == handle_marks.MARKS_CMD_UNMARK:
                return handle_marks.unmark_window_selection(query)

            return handle_marks.show_marked_windows_and_options(
                extension, event_keyword, query
            )
        elif event_keyword == extension.preferences.get(handle_workspaces.HANDLER_ID):
            return handle_workspaces.handle(query, extension)

        elif event_keyword == extension.preferences.get(handle_outputs.HANDLER_ID):
            return handle_outputs.handle(extension, query)

        else:
            return handle_windows.show_opened_windows(extension, query)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        (sub_cmd, args) = event.get_data()

        if sub_cmd == handle_marks.MARKS_EVENT_NAME:
            return handle_marks.collect_mark_name_for_window(args[0])
        if sub_cmd == handle_marks.MARKS_EVENT_CONFIRM:
            if isinstance(args, str):
                raise ValueError("Expected a list of marks")

            sway_marks.mark(args)
            return HideWindowAction()
        if sub_cmd == handle_marks.MARKS_EVENT_UNMARK:
            for mark in args["marks"]:
                sway_marks.unmark(mark)
            return HideWindowAction()

        if handle_workspaces.is_workspace_event(sub_cmd):
            return handle_workspaces.handle_event(sub_cmd, args)

        if handle_outputs.HANDLER_ID in sub_cmd:
            if isinstance(args, str):
                raise ValueError("Expected a list of marks")
            return handle_outputs.handle_selection(extension, sub_cmd, args)

        handle_windows.focus_selected_window(extension, args)
        return HideWindowAction()


if __name__ == "__main__":
    SwayWindowsExtension().run()
