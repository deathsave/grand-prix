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

    # Numbers never follow an underscore. Groups that reach 10 are
    # zero padded (l_bonus01..10), smaller ones aren't (l_grand1..5)
    def test_numbering(self):
        names = set(load("config/common/switches.yaml")["switches"]) | \
            set(load("config/common/coils.yaml")["coils"]) | \
            set(load("config/common/lights.yaml")["lights"]) | \
            set(load("config/common/rgb_leds.yaml")["lights"])
        groups = {}
        for name in names:
            self.assertIsNone(re.search(r"_\d", name),
                f"{name}: no underscore before the number")
            match = re.fullmatch(r"(.*\D)(\d+)", name)
            if match:
                groups.setdefault(match.group(1), []).append(match.group(2))
        for prefix, numbers in groups.items():
            padded = len(numbers) >= 10
            for number in numbers:
                self.assertEqual(2 if padded else 1, len(number),
                    f"{prefix}{number}: {'pad' if padded else 'do not pad'}"
                    f" ({len(numbers)} in the group)")

    # Sounds follow the same numbering (pit_done1..7, good01..14)
    def test_sound_numbering(self):
        groups = {}
        for name in load("config/common/sounds.yaml")["sounds"]:
            match = re.fullmatch(r"(.*\D)(\d+)", name)
            if match:
                groups.setdefault(match.group(1), []).append(match.group(2))
        for prefix, numbers in groups.items():
            padded = len(numbers) >= 10
            for number in numbers:
                self.assertEqual(2 if padded else 1, len(number),
                    f"{prefix}{number} ({len(numbers)} in the group)")

    # Every sound's file exists (a missing one just never plays)
    def test_sound_files_exist(self):
        files = set()
        for root, _, names in os.walk(os.path.join(ROOT, "sounds")):
            files |= set(names)
        for name, sound in load("config/common/sounds.yaml")["sounds"] \
                .items():
            self.assertIn(sound["file"], files, name)
