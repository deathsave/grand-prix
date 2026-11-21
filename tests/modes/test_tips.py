from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestTipsMode(DeathSaveGameTesting):

    def _var(self, name):
        return self.machine.variables.get_machine_var(name)

    # Tips run alongside attract mode (outside of a game)
    def test_runs_during_attract(self):
        self.assertModeRunning("attract")
        self.assertModeRunning("tips")

    # When the tip slide comes up, the tip is typed out one
    # character at a time with a cursor on the current line
    def test_types_tip(self):
        self.post_event("attract_tip")
        self.advance_time_and_run(0.2)
        title = self._var("tip_title")
        self.assertTrue(title.startswith("Ge"))
        self.assertTrue(title.endswith("_"))
        self.assertEqual("", self._var("tip_line1"))

        # typing takes ~8.5s (and the attract show
        # returns to the splash at 12s, clearing it)
        self.advance_time_and_run(10)
        self.assertEqual("Get Under Green", self._var("tip_title"))
        self.assertEqual(
            "1. Skill shot: plunge into the Backfire Hole",
            self._var("tip_line1"))
        self.assertEqual(
            "    Backfire Hole, then 10 pop bumpers",
            self._var("tip_line4"))

    # Switching back to the splash clears the tip
    def test_clears_tip(self):
        self.post_event("attract_tip")
        self.advance_time_and_run(10)
        self.assertEqual("Get Under Green", self._var("tip_title"))
        self.post_event("attract_tip_clear")
        self.advance_time_and_run(0.1)
        self.assertEqual("", self._var("tip_title"))
        self.assertEqual("", self._var("tip_line4"))

    # The attract show rotates splash -> tip after the intro
    def test_attract_rotation(self):
        # intro (12s) + splash (15s) puts us on the tip slide
        self.advance_time_and_run(28)
        self.assertTrue(self._var("tip_title"))
        # and back to the splash 15s later
        self.advance_time_and_run(15)
        self.assertEqual("", self._var("tip_title"))

    # Starting a game stops the tips and clears the text
    def test_stops_on_game_start(self):
        self.post_event("attract_tip")
        self.advance_time_and_run(1)
        self._start()
        self.assertModeNotRunning("tips")
        self.assertEqual("", self._var("tip_title"))

    # Either flipper skips to the next tip right away
    def test_flipper_skips_to_next_tip(self):
        # still on the Death Save intro
        self.advance_time_and_run(2)
        self.assertEqual("", self._var("tip_title"))

        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(10)
        self.assertEqual("Get Under Green", self._var("tip_title"))

        # the end of the intro does not interrupt the tip
        # (12s mark has passed), it stays up for its full 15s
        self.assertEqual("Get Under Green", self._var("tip_title"))
        self.advance_time_and_run(5)
        self.assertEqual("", self._var("tip_title"))

        # the other flipper skips too, restarting the typing
        self.hit_and_release_switch("s_flipper2")
        self.advance_time_and_run(0.2)
        self.assertTrue(self._var("tip_title").endswith("_"))

    # Each tip comes up in order, wrapping back to the first
    def test_cycles_through_tips(self):
        titles = []
        # (stay under the 12s intro, which clears the tip)
        for i in range(8):
            self.post_event("attract_tip")
            self.advance_time_and_run(1.2)
            titles.append(self._var("tip_title").rstrip("_"))
        self.assertTrue(titles[0].startswith("Get Under"))
        self.assertTrue(titles[1].startswith("Backfire"))
        self.assertTrue(titles[2].startswith("Grooveline"))
        self.assertTrue(titles[3].startswith("Lap of"))
        self.assertTrue(titles[4].startswith("Grand Prix"))
        self.assertTrue(titles[5].startswith("Red Line"))
        self.assertTrue(titles[6].startswith("Pure Evil"))
        # back to the start
        self.assertTrue(titles[7].startswith("Get Under"))

    # Every tip line fits the 4 line slide
    def test_tips_fit_the_slide(self):
        tips = self.machine.modes["tips"].tips
        self.assertEqual(7, len(tips))
        for tip in tips:
            self.assertTrue(tip["title"])
            self.assertLessEqual(len(tip["lines"]), 4)
            for line in tip["lines"]:
                self.assertLessEqual(len(line), 48, line)

    # Pressing a flipper while a tip is up goes to the next one
    def test_flipper_skips_during_tip(self):
        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(1.2)
        self.assertTrue(self._var("tip_title").startswith("Get Under"))
        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(1.2)
        self.assertTrue(self._var("tip_title").startswith("Backfire"))
