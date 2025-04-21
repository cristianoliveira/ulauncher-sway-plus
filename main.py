from typing import Union

import logging
import gi
gi.require_version('Gdk', '3.0')

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.event import PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import sway.windows as windows
import sway.marks as sway_marks
import sway.icons as sway_icons
from utils.sorter import sort_strategy
from utils.filterer import filter_result_list
import handlers.marks as handle_marks


logger = logging.getLogger(__name__)


class SwayWindowsExtension(Extension):

    sorter = sort_strategy("default")

    def __init__(self):
        super(SwayWindowsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(
            PreferencesEvent, PreferencesEventListener()
        )

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
        extension.sorter = sort_strategy(
            extension.preferences["sort_by"]
        )


class KeywordQueryEventListener(EventListener):
    '''Generates items for display on query'''

    def on_event(self, event, extension):
        # list of lowercase words in query
        query = event.get_query().get_argument("").lower().split()

        event_keyword = event.get_keyword()
        cmd_keyword = extension.preferences.get(handle_marks.MARKS_ID)

        if event_keyword == cmd_keyword: # Sway Marks
            if handle_marks.MARKS_CMD_MARK in query:
                mark = query[query.index(handle_marks.MARKS_CMD_MARK) + 1:]
                ls = handle_marks.collect_mark_name_for_window(mark)
                return ls
            if handle_marks.MARKS_CMD_UNMARK in query:
                unmark = query[query.index(handle_marks.MARKS_CMD_UNMARK) + 1:]
                return handle_marks.unmark_window_confirmation(unmark)

            sorted_list = extension.sorter.sort(
                sway_marks.get_marks(), by_key="app_id"
            )

            result_list = handle_marks.list_options(event_keyword, sorted_list)

            return filter_result_list(result_list, query)

        opened_windows = windows.get_windows()
        most_used_windows = extension.sorter.sort(opened_windows, by_key="app_id")

        items = list([self.get_result_item(w)
                      for w in most_used_windows
                      # Don't include the ulauncher dialog in the list,
                      # since it already has focus
                      if not w["focused"]])

        # Sort the items by usage
        return filter_result_list(RenderResultListAction(items), query)

    def get_result_item(self, con):
        (_, appName, winTitle) = windows.app_details(con)

        return ExtensionResultItem(
                icon=sway_icons.get_icon(con),
                name=winTitle,
                description=appName,
                # This only works because con is a dict, and therefore pickleable
                on_enter=ExtensionCustomAction(("sway-windows", con)))


class ItemEnterEventListener(EventListener):
    '''Executes the focus event, using the data provided in ExtensionCustomAction'''

    def on_event(self, event, extension):
        (sub_cmd, args) = event.get_data()

        if sub_cmd == handle_marks.MARKS_EVENT_NAME:
            handle_marks.collect_mark_name_for_window(args[0])
            return
        if sub_cmd == handle_marks.MARKS_EVENT_CONFIRM:
            sway_marks.mark(args[0])
            return 
        if sub_cmd == handle_marks.MARKS_EVENT_UNMARK:
            for mark in args['marks']:
                sway_marks.unmark(mark)
            return

        extension.sorter.add(args["app_id"])
        windows.focus(args)

if __name__ == '__main__':
    SwayWindowsExtension().run()
