import unittest
from unittest.mock import patch

import sway.outputs as sway_outputs


class TestSwayMsg(unittest.TestCase):
    @patch("sway.outputs.execute_command")
    def test_get_outputs_returns_outputs(self, mock_execute_command):
        list_of_outputs = [
            {"name": "output1", "active": True},
            {"name": "output2", "active": False},
            {"name": "output3", "active": True},
            {"name": "output4", "active": True},
        ]

        mock_execute_command.return_value = list_of_outputs

        self.assertEqual(
            len(sway_outputs.get_outputs(active=True)),
            3,
        )

        self.assertEqual(
            len(sway_outputs.get_outputs(active=False)),
            1,
        )
