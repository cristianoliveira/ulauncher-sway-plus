from unittest import TestCase, mock


class TestOutputs(TestCase):
    def test_get_outputs_returns_outputs(self):
        import sway.outputs as outputs

        fake_json = (
            '[{"name": "HDMI-A-1", "active": true, "make": "Dell", "model": "U2412M"}]'
        )
        with mock.patch("subprocess.check_output", return_value=fake_json.encode()):
            result = outputs.get_outputs()
            assert isinstance(result, list)
            assert result[0]["name"] == "HDMI-A-1"
            assert result[0]["active"] is True

    def test_set_output_enabled_on_and_off(self):
        import sway.outputs as outputs

        with mock.patch("sway.outputs.execute_command") as m:
            outputs.set_output_enabled("HDMI-A-1", True)
            m.assert_called_with(["swaymsg", "output", "HDMI-A-1", "enable"])
            outputs.set_output_enabled("HDMI-A-1", False)
            m.assert_called_with(["swaymsg", "output", "HDMI-A-1", "disable"])

    def test_list_outputs_action(self):
        import handlers.outputs as houtputs

        with mock.patch(
            "sway.outputs.get_outputs",
            return_value=[
                {"name": "HDMI-A-1", "active": True, "make": "Dell", "model": "U2412M"},
                {"name": "DP-1", "active": False, "make": "LG", "model": "27GL850"},
            ],
        ):
            fake_ext = mock.Mock()
            result = houtputs.list_outputs(fake_ext)
            assert hasattr(
                result, "result_list"
            ), "Result should have a result_list (RenderResultListAction)"
            names = [item.get_name() for item in result.result_list]
            assert names == ["HDMI-A-1", "DP-1"]
