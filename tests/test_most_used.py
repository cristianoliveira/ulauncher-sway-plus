import unittest
from lib.most_used import MostUsed

class TestMostUsed(unittest.TestCase):
    def test_sort_by_usage(self):
        most_used = MostUsed()
        items = [
            {'name': 'item1'},
            {'name': 'item2'},
            {'name': 'item3'}
        ]

        # Simulate usage
        most_used.add(items[0], 'name')
        most_used.add(items[1], 'name')
        most_used.add(items[1], 'name')
        most_used.add(items[2], 'name')
        most_used.add(items[2], 'name')
        most_used.add(items[2], 'name')

        # Sort items by usage
        sorted_items = most_used.sort_by_usage(items, 'name')

        # Verify the order
        self.assertEqual(sorted_items[0]['name'], 'item3')
        self.assertEqual(sorted_items[1]['name'], 'item2')
        self.assertEqual(sorted_items[2]['name'], 'item1')

if __name__ == '__main__':
    unittest.main()
