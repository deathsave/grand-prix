from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestRedLineShots(DeathSaveGameTesting):

    def setUp(self):
        super().setUp()
        self._events = {}
        for event in ["red_line_rev", "red_line_bell", "red_line_redline",
                "red_line_shift", "red_line_final_run",
                "red_line_checkered_flag"]:
            self.machine.events.add_handler(event, self._count,
                event_name=event)

    def _count(self, event_name, **kwargs):
        self._events.setdefault(event_name, []).append(kwargs)

    def _n(self, event):
        return len(self._events.get(event, []))

    def _start_red_line(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        player = self.machine.game.player
        player.is_grooveline_completed = 1
        player.is_luxury_completed = 1
        player.is_grand_prix_completed = 1
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertModeRunning("red_line")
        self.mode = self.machine.modes["red_line"].code if hasattr(
            self.machine.modes["red_line"], "code") else \
            self.machine.modes["red_line"]

    def _tach_lit(self):
        return sum(self._lit(f"l_backbox_match{n}0") for n in range(1, 10)) \
            + self._lit("l_backbox_match00")

    def _lit(self, light):
        return self.machine.lights[light].get_color().rgb != (0, 0, 0)

    def _hit(self, switch, times=1):
        for _ in range(times):
            self.hit_and_release_switch(switch)
            self.advance_time_and_run(0.1)

    def _rev_to_redline(self):
        self._hit("s_spinner", 10)

    # A full minute of ball save, with all 3 balls
    def test_three_balls_and_a_minute_of_ball_save(self):
        self._start_red_line()
        multiball = self.machine.multiballs["red_line"]
        self.assertEqual(3, multiball.config["ball_count"].evaluate({}))
        self.assertEqual(60000,
            multiball.config["shoot_again"].evaluate({}))

    # Every switch revs the tach, which drains one every 10s
    def test_rev_up_and_drain(self):
        self._start_red_line()
        self.assertEqual(0, self._tach_lit())
        self._hit("s_spinner")
        self._hit("s_target_save")
        self._hit("s_pop1")
        self.assertEqual(3, self._n("red_line_rev"))
        self.assertEqual(3, self._tach_lit())
        self.advance_time_and_run(10)
        self.assertEqual(2, self._tach_lit())

    # Full: stays full (no drain), switches just score 10 with the
    # bell, until the Backfire hole shifts for a jackpot
    def test_redline_and_shift(self):
        self._start_red_line()
        self._rev_to_redline()
        self.assertEqual(1, self._n("red_line_redline"))
        self.assertEqual(1, self.machine.game.player.red_line_at_redline)
        self.advance_time_and_run(30)
        self.assertEqual(1, self.machine.game.player.red_line_at_redline)

        score = self.machine.game.player.score
        self._hit("s_target_save")
        self._hit("s_slingshot1")
        self.assertEqual(score + 20, self.machine.game.player.score)
        self.assertEqual(2, self._n("red_line_bell"))
        self.assertEqual(10, self._n("red_line_rev"))

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_hole_backfire", 3)
        self.assertEqual(1, self._n("red_line_shift"))
        self.assertEqual(250000, self._events["red_line_shift"][0]["value"])
        self.assertGreaterEqual(self.machine.game.player.score - score,
            250000)
        self.assertEqual(0, self.machine.game.player.red_line_at_redline)
        self.assertEqual(0, self._tach_lit())
        # 2nd gear
        self.assertTrue(self._lit("l_signal1"))
        self.assertFalse(self._lit("l_signal2"))

    # The Backfire hole revs too, before the red line
    def test_backfire_revs_before_redline(self):
        self._start_red_line()
        self.hit_switch_and_run("s_hole_backfire", 3)
        self.assertEqual(0, self._n("red_line_shift"))
        self.assertEqual(1, self._tach_lit())

    # 4 shifts to 5th gear, then all three of Grooveline, Grand and
    # Prix for the checkered flag, back to 1st
    def test_final_run(self):
        self._start_red_line()
        for gear in range(1, 5):
            self._rev_to_redline()
            self.hit_switch_and_run("s_hole_backfire", 3)
            self.assertEqual(250000 * gear,
                self._events["red_line_shift"][-1]["value"])
        self.assertEqual(1, self._n("red_line_final_run"))
        self.assertEqual(10, self._tach_lit())
        for light in ["l_signal1", "l_signal2", "l_signal3", "l_signal4"]:
            self.assertTrue(self._lit(light), light)

        score = self.machine.game.player.score
        self._hit("s_grooveline")
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertEqual(0, self._n("red_line_checkered_flag"))
        self.hit_switch_and_run("s_hole_prix", 3)
        self.assertEqual(1, self._n("red_line_checkered_flag"))
        self.assertGreaterEqual(self.machine.game.player.score - score,
            2000000)
        # back to 1st
        self.assertEqual(0, self._tach_lit())
        self.assertFalse(self._lit("l_signal1"))

    # Each shift counts toward the Shift Champ high score
    def test_shifts_counted(self):
        self._start_red_line()
        self.assertEqual(0, self.machine.game.player.shift_count)
        for gear in range(2):
            self._rev_to_redline()
            self._hit("s_hole_backfire")
            self.advance_time_and_run(3)
        self.assertEqual(2, self._n("red_line_shift"))
        self.assertEqual(2, self.machine.game.player.shift_count)
