from unittest import mock

def test_get_result_item_basic():
    import handlers.windows as hw

    # Prepare a fake window container and patch dependencies
    fake_con = {"id": "1", "app_id": "fake-app", "name": "Fake Window"}
    with mock.patch("handlers.windows.sway_icons.get_icon", return_value="icon-path") as mock_get_icon,\
         mock.patch("handlers.windows.windows.app_details", return_value=("1", "FakeApp", "Fake Window")) as mock_app_details,\
         mock.patch("handlers.windows.ExtensionResultItem") as mock_ext_result_item,\
         mock.patch("handlers.windows.ExtensionCustomAction") as mock_ext_custom_action:

        hw.get_result_item(fake_con)

        mock_get_icon.assert_called_once_with(fake_con)
        mock_app_details.assert_called_once_with(fake_con)
        # The item constructor should be called with the expected arguments
        mock_ext_result_item.assert_called_once()
        mock_ext_custom_action.assert_called_once_with(("sway-windows", fake_con))
