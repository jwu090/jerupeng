"""Configuration tests use no webcam, global listeners, or real input."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from config import ROOT, load_config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.defaults = json.loads((ROOT / "config.json").read_text())

    def load(self, data):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text(json.dumps(data))
            return load_config(path)

    def test_default_model_path_is_absolute(self):
        self.assertTrue(Path(self.load(self.defaults)["tracking"]["model_path"]).is_absolute())

    def test_invalid_values_fail_before_hardware(self):
        for section, key, value in [
            ("camera", "index", -1), ("camera", "width", True),
            ("camera", "mirror", "yes"), ("tracking", "num_hands", 0),
            ("tracking", "min_tracking_confidence", 1.1),
            ("tracking", "min_hand_detection_confidence", float("nan")),
            ("tracking", "model_path", ""),
        ]:
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.defaults)
                data[section][key] = value
                with self.assertRaises(ValueError):
                    self.load(data)

    def test_missing_section_is_actionable_error(self):
        with self.assertRaisesRegex(ValueError, "Invalid preview configuration"):
            self.load({})


if __name__ == "__main__":
    unittest.main()
