import unittest
from utils.json_querier import find

class TestMostUsed(unittest.TestCase):
    def test_it_does_throw_when_empty(self):
        node = {
            "key1": {
                "type": "test",
                "key2": {
                    "type": "test2",
                    "value": "first_match"
                },
                "key4": "value2"
            },
            "key5": [
                {
                    "type": "test3",
                    "value": "not_a_match"
                },
                {
                    "type": "test4",
                    "value": "second_match"
                }
            ]
        }

        def test_predicate(x):
            if not isinstance(x, dict):
                return False
            return x.get("type") == "test2"

        found_value = find(node, test_predicate)
        self.assertIsNotNone(found_value)
        self.assertEqual(found_value.get("type"), "test2")
        self.assertEqual(found_value.get("value"), "first_match")

        def test_predicate2(x):
            if not isinstance(x, dict):
                return False
            return x.get("type") == "test4"

        found_value = find(node, test_predicate2)
        self.assertIsNotNone(found_value)
        self.assertEqual(found_value.get("type"), "test4")
        self.assertEqual(found_value.get("value"), "second_match")
