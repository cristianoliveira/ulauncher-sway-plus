from unittest import TestCase, mock

from sway.icons import get_icon


class TestGetIcon(TestCase):
    def setUp(self):
        self.container = {
            "id": 1,
            "app_id": "example",
            "pid": 123,
            "name": "Example Window",
        }

    def test_app_icon_does_not_need_process_access(self):
        with (
            mock.patch("sway.icons.getIconPath", return_value="app.svg"),
            mock.patch("sway.icons.os.readlink") as readlink,
        ):
            icon = get_icon(self.container)

        self.assertEqual(icon, "app.svg")
        readlink.assert_not_called()

    def test_x11_icon_does_not_need_process_access(self):
        self.container["app_id"] = None
        self.container["window_properties"] = {"class": "Example"}
        with (
            mock.patch("sway.icons.getIconPath", return_value="x11.svg"),
            mock.patch("sway.icons.os.readlink") as readlink,
        ):
            icon = get_icon(self.container)

        self.assertEqual(icon, "x11.svg")
        readlink.assert_not_called()

    def test_executable_icon_is_used_when_app_icon_is_missing(self):
        with (
            mock.patch("sway.icons.getIconPath", side_effect=[None, "exe.svg"]),
            mock.patch("sway.icons.os.readlink", return_value="/usr/bin/example"),
        ):
            icon = get_icon(self.container)

        self.assertEqual(icon, "exe.svg")

    def test_default_icon_is_used_when_process_is_inaccessible_or_gone(self):
        for error in (PermissionError(), FileNotFoundError()):
            with (
                self.subTest(error=type(error).__name__),
                mock.patch("sway.icons.getIconPath", return_value=None),
                mock.patch("sway.icons.os.readlink", side_effect=error),
            ):
                icon = get_icon(self.container)

                self.assertEqual(icon, "images/default.svg")

    def test_default_icon_is_used_when_no_icon_matches(self):
        with (
            mock.patch("sway.icons.getIconPath", return_value=None),
            mock.patch("sway.icons.os.readlink", return_value="/usr/bin/example"),
        ):
            icon = get_icon(self.container)

        self.assertEqual(icon, "images/default.svg")
