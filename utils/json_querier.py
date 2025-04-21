from typing import Callable, Dict, Any, Union, Self, List

Node = Union[Dict[str, Any], List, None, str, int, float, bool]

def find(node: Node, fn_predicate: Callable) -> Node:

    """
    Finds the first occurrence of a key in a nested dictionary or list
    """
    if not callable(fn_predicate):
        raise TypeError("fn_predicate must be a callable")

    if node is None:
        return None

    if isinstance(node, str):
        return node if fn_predicate(node) else None

    if isinstance(node, dict):
        for value in node.values():

            if fn_predicate(value):
                return value
            result = find(value, fn_predicate)
            if result is not None:
                return result

    elif isinstance(node, list):
        for item in node:
            if fn_predicate(item):
                return item
            result = find(item, fn_predicate)
            if result is not None:
                return result

    return None

def find_all(node: Node, fn_predicate: Callable) -> List[Node]:
    """
    Finds all occurrences of a key in a nested dictionary or list
    """
    if not callable(fn_predicate):
        raise TypeError("fn_predicate must be a callable")

    if node is None:
        return []

    if isinstance(node, str):
        return [node] if fn_predicate(node) else []

    results = []
    if isinstance(node, dict):
        for value in node.values():
            if fn_predicate(value):
                results.append(value)
            results.extend(find_all(value, fn_predicate))

    elif isinstance(node, list):
        for item in node:
            if fn_predicate(item):
                results.append(item)
            results.extend(find_all(item, fn_predicate))

    return results
