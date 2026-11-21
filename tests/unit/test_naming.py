import os
import re
import unittest
from ruamel.yaml import YAML

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def load(path):
    with open(os.path.join(ROOT, path)) as f:
        return YAML(typ="safe").load(f)


class TestNaming(unittest.TestCase):

    # Pairs are numbered left to right from the player's view:
    # anything ending in 1 is left of its 2 (per the monitor)
    def test_pairs_are_left_then_right(self):
        monitor = load("monitor/monitor.yaml")
        for kind in ["switch", "light"]:
            spots = monitor[kind]
            for name, spot in spots.items():
                match = re.fullmatch(r"(.*[a-z])1", name)
                pair = match and f"{match.group(1)}2"
                if pair and pair in spots and f"{match.group(1)}3" \
                        not in spots:
                    self.assertLess(spot["x"], spots[pair]["x"],
                        f"{name} should be left of {pair}")

    # s_flipper1 is the left flipper, its tag included
    def test_flippers(self):
        flippers = load("config/common/flippers.yaml")["flippers"]
        switches = load("config/common/switches.yaml")["switches"]
        for side, number in [("left", 1), ("right", 2)]:
            flipper = flippers[f"{side}_flipper"]
            self.assertEqual(f"s_flipper{number}",
                flipper["activation_switch"])
            self.assertEqual(f"c_flipper{number}", flipper["main_coil"])
            self.assertIn(f"{side}_flipper",
                switches[f"s_flipper{number}"]["tags"])

    # The left flipper moves the high score letter left
    def test_high_score_shifting(self):
        entry = [w for w in load(
            "modes/high_score/config/high_score.yaml")["slides"]
            ["high_score_enter_initials"] if w.get("type") ==
            "text_input"][0]
        self.assertEqual("sw_left_flipper", entry["shift_left_event"])
        self.assertEqual("sw_right_flipper", entry["shift_right_event"])
