from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestTipsMode(DeathSaveGameTesting):

    def _var(self, name):
        return self.machine.variables.get_machine_var(name)

    # the tip title without the typing cursor
    def _title(self):
        return self._var("tip_title").rstrip("_")

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

        # typing takes under 7s (and the intro ending
        # at 12s starts the splash, clearing it)
        self.advance_time_and_run(8)
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

    # After the intro (12s): the splash for 15s, then
    # each tip for 10s, then back to the splash
    def test_attract_rotation(self):
        self.advance_time_and_run(13)
        self.assertEqual("", self._var("tip_title"))
        self.advance_time_and_run(15)
        self.assertEqual("Get Under Green", self._title())
        self.advance_time_and_run(10)
        self.assertEqual("Back... Fire", self._title()[:12])
        # 6 more tips (8 total) puts us on the last one
        self.advance_time_and_run(60)
        self.assertEqual("Pure Evil", self._title())
        # then the splash again
        self.advance_time_and_run(10)
        self.assertEqual("", self._var("tip_title"))
        self.advance_time_and_run(15)
        self.assertEqual("Get Under Green", self._title())

    # The show has one 10s step per tip after the 15s splash
    def test_show_has_a_step_per_tip(self):
        steps = self.machine.shows["attract_rotation"].get_show_steps()
        tips = self.machine.modes["tips"].tips
        self.assertEqual(len(tips) + 1, len(steps))
        self.assertEqual(15, steps[0]["duration"])
        for step in steps[1:]:
            self.assertEqual(10, step["duration"])

    # Every slide change whooshes (timed or from a flipper)
    def test_every_step_whooshes(self):
        steps = self.machine.shows["attract_rotation"].get_show_steps()
        for step in steps:
            self.assertIn("whoosh", step.get("sounds", {}))

    # Starting a game stops the tips and clears the text
    def test_stops_on_game_start(self):
        self.post_event("attract_tip")
        self.advance_time_and_run(1)
        self._start()
        self.assertModeNotRunning("tips")
        self.assertEqual("", self._var("tip_title"))

    # From the intro, the right flipper starts at the first
    # tip and the left flipper at the last
    def test_right_flipper_from_intro(self):
        self.advance_time_and_run(2)
        self.assertEqual("", self._var("tip_title"))
        self.hit_and_release_switch("s_flipper2") # right
        self.advance_time_and_run(8)
        self.assertEqual("Get Under Green", self._title())
        # the end of the intro does not interrupt the tip,
        # it stays up for its full 10s
        self.advance_time_and_run(1.5)
        self.assertEqual("Get Under Green", self._title())

    def test_left_flipper_from_intro(self):
        self.advance_time_and_run(2)
        self.hit_and_release_switch("s_flipper1") # left
        self.advance_time_and_run(8)
        self.assertEqual("Pure Evil", self._title())
        # and the splash comes next
        self.advance_time_and_run(2.5)
        self.assertEqual("", self._var("tip_title"))

    # The right flipper advances through every step
    # (splash included) and wraps around
    def test_right_flipper_advances(self):
        self.advance_time_and_run(13)
        titles = []
        for i in range(10):
            self.hit_and_release_switch("s_flipper2")
            self.advance_time_and_run(8)
            titles.append(self._title())
        self.assertEqual([
            "Get Under Green",
            "Back... Fire... Pops! Alright?",
            "Grooveline Multiball",
            "Lap of Luxury",
            "Grand Prix Multiball",
            "Extra Ball & 2X",
            "Red Line",
            "Pure Evil",
            "", # splash
            "Get Under Green",
        ], titles)

    # The left flipper steps back, wrapping from the
    # splash to the last tip
    def test_left_flipper_rewinds(self):
        self.advance_time_and_run(13 + 15 + 10)
        self.assertEqual("Back... Fire", self._title()[:12])
        titles = []
        for i in range(3):
            self.hit_and_release_switch("s_flipper1")
            self.advance_time_and_run(8)
            titles.append(self._title())
        self.assertEqual(
            ["Get Under Green", "", "Pure Evil"], titles)

    # A step's full time restarts after a flipper press
    def test_flipper_restarts_step_time(self):
        self.advance_time_and_run(13 + 15 + 9)
        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(9.5)
        self.assertEqual("Get Under Green", self._title())

    # Every tip line fits the 4 line slide
    def test_tips_fit_the_slide(self):
        tips = self.machine.modes["tips"].tips
        self.assertEqual(8, len(tips))
        for tip in tips:
            self.assertTrue(tip["title"])
            self.assertLessEqual(len(tip["lines"]), 4)
            for line in tip["lines"]:
                self.assertLessEqual(len(line), 48, line)
