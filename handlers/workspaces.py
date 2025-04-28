from typing import Optional

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import sway.workspaces as sway_ws

HANDLER_ID = "sway-workspaces"

CMD_SEND_TO_OUTPUT = "send"
EVENT_SEND_TO_OUTPUT = "sway-send-to-output"


def handle(query: str, extension) -> Optional[RenderResultListAction]:
    """
    Handle the query and return the result list action.
    """
    if not query:
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=CMD_SEND_TO_OUTPUT,
                    description="Send current workspace to another output",
                    on_enter=SetUserQueryAction(
                        f"{extension.preferences[HANDLER_ID]} {CMD_SEND_TO_OUTPUT} "
                    ),
                ),
            ]
        )

    if CMD_SEND_TO_OUTPUT not in query:
        return RenderResultListAction([])

    outputs = sway_ws.get_outputs(active=True)

    if not outputs:
        raise ValueError("No outputs found")

    options = [
        ExtensionResultItem(
            icon="images/icon.png",
            name=output["name"],
            description="Send current workspace to this output",
            on_enter=ExtensionCustomAction(
                (EVENT_SEND_TO_OUTPUT, output),
                keep_app_open=False,
            ),
        )
        for output in outputs
    ]

    return RenderResultListAction(options)


def is_workspace_event(sub_cmd: str) -> bool:
    """
    Check if the sub command is a workspace event.
    """
    return [EVENT_SEND_TO_OUTPUT].count(sub_cmd) > 0


def handle_event(sub_cmd: str, args: dict) -> Optional[HideWindowAction]:
    """
    Handle the event and return the action.
    """
    if sub_cmd == EVENT_SEND_TO_OUTPUT:
        output_name = args["name"]
        sway_ws.send_workspace_to_output(output_name)

    return HideWindowAction()
