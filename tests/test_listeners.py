import unittest
from unittest.mock import patch

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.search.Query import Query

from handlers.marks import MARKS_ID
from main import KeywordQueryEventListener, SwayWindowsExtension


class TestKeywordQueryEventListener(unittest.TestCase):
    def setUp(self):
        self.extension = SwayWindowsExtension()
        self.extension.preferences = {
            "sort_by": "default",
            MARKS_ID: "wm",
        }

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
        input_text = "wm unmark"

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
