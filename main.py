import logging
from typing import Union

import gi

gi.require_version("Gdk", "3.0")

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)

import handlers.marks as handle_marks
import handlers.windows as handle_windows
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
        # list of lowercase words in query
        query = event.get_query().get_argument("").lower().split()

        event_keyword = event.get_keyword()
        cmd_keyword = extension.preferences.get(handle_marks.MARKS_ID)

        if event_keyword == cmd_keyword:  # Sway Marks

            if handle_marks.MARKS_CMD_MARK in query:
                mark = query[query.index(handle_marks.MARKS_CMD_MARK) + 1 :]
                return handle_marks.collect_mark_name_for_window(mark)

            if handle_marks.MARKS_CMD_UNMARK in query:
                unmark = query[query.index(handle_marks.MARKS_CMD_UNMARK) + 1 :]
                return handle_marks.unmark_window_selection(unmark)

            return handle_marks.show_marked_windows_and_options(
                extension, event_keyword, query
            )

        else:
            return handle_windows.show_opened_windows(extension, query)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        (sub_cmd, args) = event.get_data()

        if sub_cmd == handle_marks.MARKS_EVENT_NAME:
            handle_marks.collect_mark_name_for_window(args[0])
            return
        if sub_cmd == handle_marks.MARKS_EVENT_CONFIRM:
            sway_marks.mark(args[0])
            return
        if sub_cmd == handle_marks.MARKS_EVENT_UNMARK:
            for mark in args["marks"]:
                sway_marks.unmark(mark)
            return

        handle_windows.focus_selected_window(extension, args)


if __name__ == "__main__":
    SwayWindowsExtension().run()
