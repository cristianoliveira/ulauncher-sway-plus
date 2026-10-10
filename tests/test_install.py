import os
import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
EXTENSION_ID = "com.github.cristianoliveira.ulauncher-sway-plus"


class TestInstall(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        self.home.mkdir()
        self.data = self.home / ".local/share"

    def install(self, *args, data_home=None):
        env = {**os.environ, "HOME": str(self.home)}
        env.pop("XDG_DATA_HOME", None)
        if data_home is not None:
            env["XDG_DATA_HOME"] = str(data_home)
        return subprocess.run(
            ["bash", str(ROOT / "install.sh"), *args],
            cwd=self.home,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_installs_runtime_files_in_default_data_directory(self):
        result = self.install()

        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.data / "ulauncher/extensions" / EXTENSION_ID
        for name in ("main.py", "manifest.json", "sway/icons.py", "images/icon.png"):
            self.assertEqual((target / name).read_bytes(), (ROOT / name).read_bytes())
        self.assertFalse((target / "tests").exists())
        self.assertFalse(list(target.rglob("*.pyc")))

    def test_respects_data_directory_with_spaces(self):
        data = self.home / "custom data"

        result = self.install(data_home=data)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            (data / "ulauncher/extensions" / EXTENSION_ID / "main.py").is_file()
        )
        self.assertFalse(self.data.exists())

    def test_refuses_existing_install_without_changing_it(self):
        target = self.data / "ulauncher/extensions" / EXTENSION_ID
        target.mkdir(parents=True)
        (target / "main.py").write_text("existing installation")

        result = self.install()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "main.py").read_text(), "existing installation")
        self.assertEqual(list(target.iterdir()), [target / "main.py"])

    def test_refuses_dangling_symlink(self):
        target = self.data / "ulauncher/extensions" / EXTENSION_ID
        target.parent.mkdir(parents=True)
        target.symlink_to(self.home / "missing")

        result = self.install()

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(target.is_symlink())
        self.assertFalse((self.home / "missing").exists())

    def test_help_does_not_install(self):
        result = self.install("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.data.exists())

    def test_rejects_unknown_options_and_relative_data_directory(self):
        for args, data in ((("--force",), None), ((), "relative")):
            with self.subTest(args=args, data=data):
                result = self.install(*args, data_home=data)

                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.data.exists())
                self.assertFalse((self.home / "relative").exists())
