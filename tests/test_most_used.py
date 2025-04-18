import unittest
from lib.most_used import MostUsed

class TestMostUsed(unittest.TestCase):
    def test_it_does_throw_when_empty(self):
        most_used = MostUsed()
        items = []

        sorted_items = most_used.sort_by_usage(items, 'name')

        # Simulate usage
        most_used.add('item1')
        most_used.add('item2')

        # Sort items by usage
        sorted_items = most_used.sort_by_usage(items, 'name')

        # Verify the order
        self.assertEqual(sorted_items, [])

    def test_sort_by_usage(self):
        most_used = MostUsed()
        items = [
            {'name': 'item1'},
            {'name': 'item2'},
            {'name': 'item3'}
        ]

        # Simulate usage
        most_used.add(items[0].get('name'))
        most_used.add(items[1].get('name'))
        most_used.add(items[1].get('name'))
        most_used.add(items[2].get('name'))
        most_used.add(items[2].get('name'))
        most_used.add(items[2].get('name'))

        # Sort items by usage
        sorted_items = most_used.sort_by_usage(items, 'name')

        # Verify the order
        self.assertEqual(sorted_items[0]['name'], 'item3')
        self.assertEqual(sorted_items[1]['name'], 'item2')
        self.assertEqual(sorted_items[2]['name'], 'item1')

if __name__ == '__main__':
    unittest.main()
