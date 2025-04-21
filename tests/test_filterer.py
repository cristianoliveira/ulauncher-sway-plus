import unittest
from utils.filterer import filter_result_list
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

class TestFilterer(unittest.TestCase):
    def test_filter_result_list(self):
        # Create a mock RenderResultListAction with some items
        items = [
            {"name": "first_match"},
            {"name": "second_match"},
            {"name": "third_match"},
            {"name": "not_a_match"},
            {"name": "first_second_match"}, # This matches both "first" and "second"
        ]
        extension_result_items = [
            ExtensionResultItem(
                icon=None,
                name=item["name"],
                description=f"description for {item['name']}",
                on_enter=None,
            ) for item in items
        ]
        render_result_list = RenderResultListAction(extension_result_items)

        # Test filtering with a query that matches some items
        query = ["first", "match"]
        filtered_result_list = filter_result_list(render_result_list, query)
        self.assertEqual(len(filtered_result_list.result_list), 2)
        self.assertEqual(filtered_result_list.result_list[0].get_name(), "first_match")
        self.assertEqual(filtered_result_list.result_list[0].get_description(""), "description for first_match")
        self.assertEqual(filtered_result_list.result_list[1].get_name(), "first_second_match")
        self.assertEqual(filtered_result_list.result_list[1].get_description(""), "description for first_second_match")

        query = ["second"]

        filtered_result_list = filter_result_list(render_result_list, query)
        self.assertEqual(len(filtered_result_list.result_list), 2)
        self.assertEqual(filtered_result_list.result_list[0].get_name(), "second_match")
        self.assertEqual(filtered_result_list.result_list[0].get_description(""), "description for second_match")
        self.assertEqual(filtered_result_list.result_list[1].get_name(), "first_second_match")
        self.assertEqual(filtered_result_list.result_list[1].get_description(""), "description for first_second_match")
        
    def test_throws_type_error(self):
        # Create a mock object that is not a RenderResultListAction
        class MockObject:
            pass

        mock_object = MockObject()
        query = ["first", "match"]

        # Check if TypeError is raised
        with self.assertRaises(TypeError):
            filter_result_list(mock_object, query)
