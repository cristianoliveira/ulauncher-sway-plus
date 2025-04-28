from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

import sway.outputs as sway_outputs
from utils.filterer import filter_result_list

HANDLER_ID = "sway-outputs"

SUB_CMD_ENABLE = "enable"
SUB_CMD_DISABLE = "disable"


def list_options(extension, query=[]):
    """List all options to manage outputs.

    List:
        - enable <select_from_list>
        - disable <select_from_list>

    :param extension: The extension instance.
    :param query: The search query.

    """
    if len(query) == 0 and not isinstance(query, list):
        raise ValueError("Expected a list of query strings")

    items = [
        ExtensionResultItem(
            icon="images/icon.png",
            name="Enable",
            description="Enable the selected output",
            on_enter=SetUserQueryAction(
                f"{extension.preferences[HANDLER_ID]} {SUB_CMD_ENABLE} "
            ),
        ),
        ExtensionResultItem(
            icon="images/icon.png",
            name="Disable",
            description="Disable the selected output",
            on_enter=SetUserQueryAction(
                f"{extension.preferences[HANDLER_ID]} {SUB_CMD_DISABLE} "
            ),
        ),
    ]

    return filter_result_list(RenderResultListAction(items), query)


def list_outputs(_, __=None, action=None):
    """Lists all outputs (monitors), showing whether each is enabled or disabled."""
    outputs = sway_outputs.get_outputs(active=action != SUB_CMD_ENABLE)
    items = []
    for out in outputs:
        name = out["name"]
        active = out.get("active", False)
        desc = f"{'▶️ ENABLED' if active else '⛔ DISABLED'} - {out.get('make', '')} {out.get('model', '')}"
        items.append(
            ExtensionResultItem(
                icon="images/default.svg",  # You may want a display icon
                name=name,
                description=desc,
                on_enter=ExtensionCustomAction(
                    (f"{HANDLER_ID}-{action}", {"name": name, "active": active})
                ),
            )
        )
    return RenderResultListAction(items)


def handle(extension, query):
    """Handle the query and return the result list action."""
    if "enable" in query:
        return list_outputs(extension, query[1:], action=SUB_CMD_ENABLE)

    if "disable" in query:
        return list_outputs(extension, query[1:], action=SUB_CMD_DISABLE)

    return list_options(extension, query)


def handle_selection(_, sub_cmd, args):
    """
    Handle the selection and return the action.
    """

    name = args["name"]
    if sub_cmd == f"{HANDLER_ID}-{SUB_CMD_ENABLE}":
        sway_outputs.set_output_enabled(name, True)
    elif sub_cmd == f"{HANDLER_ID}-{SUB_CMD_DISABLE}":
        sway_outputs.set_output_enabled(name, False)
    else:
        raise ValueError(f"Unknown command: {sub_cmd}")
