import unittest

from utils.sorter import MostVisited, RecentUsed


class TestMostUsed(unittest.TestCase):
    def test_it_does_throw_when_empty(self):
        most_used = MostVisited()
        items = []

        sorted_items = most_used.sort(items, "name")

        # Simulate usage
        most_used.add("item1")
        most_used.add("item2")

        # Sort items by usage
        sorted_items = most_used.sort(items, "name")

        # Verify the order
        self.assertEqual(sorted_items, [])

    def test_sort_by_usage(self):
        most_used = MostVisited()
        items = [{"name": "item1"}, {"name": "item2"}, {"name": "item3"}]

        no_changes = most_used.sort(items, "name")

        self.assertEqual(items[0]["name"], no_changes[0]["name"])

        # Simulate usage
        most_used.add(items[0].get("name"))
        most_used.add(items[1].get("name"))
        most_used.add(items[1].get("name"))
        most_used.add(items[2].get("name"))
        most_used.add(items[2].get("name"))
        most_used.add(items[2].get("name"))

        # Sort items by usage
        sorted_items = most_used.sort(items, "name")

        # Verify the order
        self.assertEqual(sorted_items[0]["name"], "item3")
        self.assertEqual(sorted_items[1]["name"], "item2")
        self.assertEqual(sorted_items[2]["name"], "item1")


class TestRecentUsed(unittest.TestCase):
    def test_it_does_throw_when_empty(self):
        recent_used = RecentUsed()
        items = []

        sorted_items = recent_used.sort(items, "name")

        # Simulate usage
        recent_used.add("item1")
        recent_used.add("item2")

        # Sort items by usage
        sorted_items = recent_used.sort(items, "name")

        # Verify the order
        self.assertEqual(sorted_items, [])

    def test_sort_by_recent_usage(self):
        recent_used = RecentUsed()
        items = [{"name": "item1"}, {"name": "item2"}, {"name": "item3"}]

        # Simulate usage
        recent_used.add(items[0].get("name"))
        recent_used.add(items[1].get("name"))
        recent_used.add(items[1].get("name"))
        recent_used.add(items[2].get("name"))
        recent_used.add(items[2].get("name"))
        recent_used.add(items[2].get("name"))
        recent_used.add(items[1].get("name"))

        # Sort items by usage
        sorted_items = recent_used.sort(items, "name")

        # Verify the order
        self.assertEqual(sorted_items[0]["name"], "item2")
        self.assertEqual(sorted_items[1]["name"], "item3")
        self.assertEqual(sorted_items[2]["name"], "item1")


if __name__ == "__main__":
    unittest.main()
