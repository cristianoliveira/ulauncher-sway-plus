from typing import List

from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction


def filter_result_list(render_result_list: RenderResultListAction, query: List[str]):
    """
    Filters the result list based on the query.

    :param list result_list: list of :class:`~ulauncher.api.shared.item.ResultItem.ResultItem` objects
    :param str query: query string to filter the result list
    :return: filtered result list
    :rtype: list
    """
    if not isinstance(render_result_list, RenderResultListAction):
        raise TypeError("Expected RenderResultListAction instance")

    if not query:
        return render_result_list

    items = render_result_list.result_list

    filtered_result_list = []
    for item in items:
        if all(word in item.get_name().lower() for word in query):
            filtered_result_list.append(item)

    return RenderResultListAction(filtered_result_list)
