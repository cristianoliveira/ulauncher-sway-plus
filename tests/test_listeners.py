import pickle
import unittest
from unittest.mock import patch

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.search.Query import Query

import handlers.outputs as handle_outputs
import handlers.workspaces as handle_workspaces
from handlers.marks import MARKS_ID
from main import ItemEnterEventListener, KeywordQueryEventListener, SwayWindowsExtension
from tests.mocks import mock_keyword_query_event_input as mocked_input


class TestKeywordQueryEventListener(unittest.TestCase):
    def setUp(self):
        self.extension = SwayWindowsExtension()
        self.extension.preferences = {
            "sort_by": "default",
            MARKS_ID: "wm",
            handle_workspaces.HANDLER_ID: "ws",
            handle_outputs.HANDLER_ID: "wo",
        }

    def test_subcommand_confirm_with_empty_space(self):
        input_text = "wm mark"  # No empty space at the end

        with patch("sway.marks.get_marks") as get_marks:
            get_marks.return_value = []
            listener = KeywordQueryEventListener()
            key_event = KeywordQueryEvent(Query(input_text))

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertIsInstance(result.result_list, list)
            self.assertEqual(len(result.result_list), 2)
            # Still show options
            self.assertEqual(result.result_list[0].get_name(), "Mark")
            self.assertEqual(result.result_list[1].get_name(), "Unmark")

            ### testing subcommand trigger
            input_text = "wm mark "  # No empty space at the end

            listener = KeywordQueryEventListener()
            key_event = KeywordQueryEvent(Query(input_text))

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertIsInstance(result.result_list, list)
            self.assertEqual(len(result.result_list), 1)
            # Still show options
            self.assertIn("The current window", result.result_list[0].get_name())

    def test_marking_window(self):
        input_text = "wm mark foo"

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        result = listener.on_event(key_event, self.extension)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, RenderResultListAction)

        self.assertIsInstance(result.result_list, list)
        self.assertEqual(len(result.result_list), 1)
        nextevent = result.result_list[0].on_enter("")
        self.assertIsInstance(nextevent, ExtensionCustomAction)

    def test_filtering_unmark_windows(self):
        input_text = "wm unmark qux"

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        with patch("sway.marks.get_marks") as get_marks:
            get_marks.return_value = [
                {"name": "bar", "marks": ["foo"]},
                {"name": "baz", "marks": ["qux"]},
                {"name": "foo", "marks": ["bar"]},
            ]

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertEqual(len(result.result_list), 1)
            self.assertEqual(result.result_list[0].get_name(), "[qux] baz")

    def test_list_marked_windows(self):
        input_text = "wm"
        with patch("sway.marks.get_marks") as get_marks:
            get_marks.return_value = [
                {"name": "foo", "marks": ["bar"]},
                {"name": "baz", "marks": ["qux"]},
            ]

            listener = KeywordQueryEventListener()
            key_event = KeywordQueryEvent(Query(input_text))

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertIsInstance(result.result_list, list)
            self.assertEqual(len(result.result_list), 4)
            self.assertEqual(result.result_list[0].get_name(), "[bar] foo")
            self.assertEqual(result.result_list[1].get_name(), "[qux] baz")
            self.assertEqual(result.result_list[2].get_name(), "Mark")
            self.assertEqual(result.result_list[3].get_name(), "Unmark")

    def test_filtering_marked_windows(self):
        input_text = "wm qux"

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        with patch("sway.marks.get_marks") as get_marks:
            get_marks.return_value = [
                {"name": "bar", "marks": ["foo"]},
                {"name": "baz", "marks": ["qux"]},
                {"name": "foo", "marks": ["bar"]},
            ]

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertEqual(len(result.result_list), 1)
            self.assertEqual(result.result_list[0].get_name(), "[qux] baz")

    @patch("sway.icons.get_icon")
    @patch("sway.windows.get_windows")
    def test_showing_windows(self, mock_get_windows, mock_get_icon):
        # Test the show command
        input_text = "w bar"

        mock_get_icon.return_value = "icon_path"
        mock_get_windows.return_value = [
            {
                "name": "foo bar 1",
                "app_id": "foo bar",
                "pid": "foo",
                "focused": False,
                "id": "id1",
            },
            {
                "name": "baz bar",
                "app_id": "baz bar",
                "pid": "foo",
                "focused": True,
                "id": "id2",
            },
            {
                "name": "bar baz",
                "app_id": "bar baz",
                "pid": "foo",
                "focused": False,
                "id": "id3",
            },
        ]

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        result = listener.on_event(key_event, self.extension)
        self.assertEqual(len(result.result_list), 2)

    def test_check_missing_argument(self):
        input_text = "wm unmark "

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        with patch("sway.marks.get_marks") as get_marks:
            get_marks.return_value = [
                {"name": "bar", "marks": ["foo"]},
                {"name": "baz", "marks": ["qux"]},
            ]

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertEqual(len(result.result_list), 2)
            self.assertEqual(result.result_list[0].get_name(), "[foo] bar")

    def test_list_available_outputs(self):
        input_text = "ws send"

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        with patch("sway.workspaces.get_outputs") as get_outputs:
            get_outputs.return_value = [
                {"name": "output DP-1", "active": True},
                {"name": "output DP-2", "active": True},
            ]

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertEqual(len(result.result_list), 2)
            self.assertEqual(result.result_list[0].get_name(), "output DP-1")
            self.assertEqual(result.result_list[1].get_name(), "output DP-2")
            self.assertEqual(
                result.result_list[0].get_description(""),
                "Send current workspace to this output",
            )

            trigger = result.result_list[0].on_enter
            # NOTE: ExtensionCustomAction isn't too open for testing
            self.assertIsInstance(trigger(""), ExtensionCustomAction)
            self.assertEqual(
                pickle.loads(trigger("")._data),
                (
                    handle_workspaces.EVENT_SEND_TO_OUTPUT,
                    {"name": "output DP-1", "active": True},
                ),
            )

    def test_send_workspace_to_output(self):
        event_data = pickle.dumps(
            (
                handle_workspaces.EVENT_SEND_TO_OUTPUT,
                {"name": "output DP-1", "active": True},
            )
        )

        listener = ItemEnterEventListener()
        key_event = ItemEnterEvent(event_data)

        with patch("sway.workspaces.send_workspace_to_output") as send_workspace:
            send_workspace.return_value = None

            result = listener.on_event(key_event, self.extension)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, HideWindowAction)

            # Check if send_workspace_to_output was called with the correct argument
            send_workspace.assert_called_once_with("output DP-1")

    def test_enablin_disabling_outputs(self):
        input_text = "wo "

        listener = KeywordQueryEventListener()
        key_event = KeywordQueryEvent(Query(input_text))

        result = listener.on_event(key_event, self.extension)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, RenderResultListAction)

        self.assertEqual(len(result.result_list), 2)
        self.assertEqual(result.result_list[0].get_name(), "Enable")
        self.assertEqual(result.result_list[1].get_name(), "Disable")

    def test_enablin_disabling_outputs_filtering(self):
        input_text = "wo ena"

        result = mocked_input(input_text, self.extension)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, RenderResultListAction)

        self.assertEqual(len(result.result_list), 1)
        self.assertEqual(result.result_list[0].get_name(), "Enable")

    def test_output_enable_filter_by_name(self):
        input_text = "wo enable DP-1"
        with patch("handlers.outputs.sway_outputs") as so:
            so.get_outputs.return_value = [
                {"name": "DP-1", "active": True},
                {"name": "DP-2", "active": True},
                {"name": "eDP-1", "active": True},
            ]
            result = mocked_input(input_text, self.extension)

            self.assertIsNotNone(result)
            self.assertIsInstance(result, RenderResultListAction)

            self.assertEqual(len(result.result_list), 2)
