from datetime import datetime


class MostVisited:
    """
    This class is used to track the most used items.
    It allows adding items and sorting them based on their usage count.
    """

    def __init__(self):
        self.items = {}

    def add(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def sort(self, current_items, by_key):
        sorted_items = sorted(
            current_items, key=lambda x: self.items.get(x.get(by_key), 0), reverse=True
        )
        return sorted_items


class RecentUsed:
    """
    This class is used to track the recently used items.
    It allows adding items and sorting them based on their recent usage.
    """

    def __init__(self):
        self.items = {}

    def add(self, key):
        self.items[key] = datetime.now().timestamp()

    def sort(self, current_items, by_key):
        sorted_items = sorted(
            current_items,
            key=lambda x: self.items.get(x.get(by_key), 0.0),
            reverse=True,
        )
        return sorted_items


class NoSort:
    """
    This class is used when no sorting is needed.
    It simply returns the items as they are.
    """

    def sort(self, current_items, by_key):
        return current_items

    def add(self, by_key):
        pass


def sort_strategy(setting):
    """
    Returns the appropriate sorting strategy based on the setting.

    :param setting: The sorting setting
    :return: The sorting strategy
    """
    if setting == "most_used":
        return MostVisited()
    elif setting == "recent":
        return RecentUsed()
    else:
        return NoSort()
