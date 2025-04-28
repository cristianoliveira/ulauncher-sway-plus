from typing import Union

from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.search.Query import Query

from main import KeywordQueryEventListener


def mock_keyword_query_event_input(
    query: str, extension
) -> Union[RenderResultListAction, None]:
    """
    Mock the KeywordQueryEvent class for testing.

    :param query: The query to be mocked.
    :return: A mock object of RenderResultListAction.
    """
    listener = KeywordQueryEventListener()
    key_event = KeywordQueryEvent(Query(query))

    return listener.on_event(key_event, extension)
