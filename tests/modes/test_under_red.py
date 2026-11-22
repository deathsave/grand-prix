from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestUnderRed(DeathSaveGameTesting):

    def _under_red(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("green_flag_under_red")
        self.advance_time_and_run(1)

    # A red flag: Green Flag stops (no Backfire hurry up), and the
    # switches score like the pit
    def test_red_flag(self):
        self._under_red()
        self.assertModeRunning("under_red")
        self.assertModeNotRunning("green_flag")
        self.assertFalse(
            self.machine.timers["backfire_qualification"].running)
        self._assertIncrement("score", "s_pop1", 10)
        self._assertIncrement("score", "s_spinner", 10)

    # Topping up the resources doesn't get you out, nor does
    # Backfire
    def test_no_way_out_but_the_grand_hole(self):
        self._under_red()
        player = self.machine.game.player
        self.assertEqual(2, player.level_fuel)
        self.assertEqual(2, player.level_lube)
        for switch in ["s_pit_fuel", "s_pit_lube", "s_pit_tires"]:
            self.hit_and_release_switch(switch)
            self.advance_time_and_run(1)
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_spinner")
        self.hit_switch_and_run("s_hole_backfire", 3)
        self.assertModeNotRunning("backfire")
        self.assertModeRunning("under_red")

        # the Grand hole is
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertModeNotRunning("under_red")
        self.assertModeRunning("green_flag")

    # It doesn't carry over to the next ball (back in the pit)
    def test_drain(self):
        self._under_red()
        self._drain_one_ball()
        self.advance_time_and_run(20)
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertModeNotRunning("under_red")
        self.assertModeNotRunning("green_flag")
        self.assertModeRunning("pit")

    # Not during a multiball
    def test_not_during_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._sim_grooveline()
        self.post_event("green_flag_under_red")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("under_red")
        self.assertModeRunning("green_flag")

    # The pit inserts chase red up to the Grand hole, and GRAND 1
    # and 2 alternate
    def test_lights(self):
        self._under_red()
        seen = { name: set() for name in ["l_pit_arrow2", "l_pit_arrow1",
            "l_pit_fuel", "l_pit_lube", "l_pit_tires", "l_grand1",
            "l_grand2"] }
        both_grand = False
        for i in range(40):
            self.advance_time_and_run(0.03)
            for name in seen:
                seen[name].add(self.machine.lights[name].get_color().rgb)
            if self._on("l_grand1") and self._on("l_grand2"):
                both_grand = True
        from mpf.core.rgb_color import RGBColor
        # (config/common/named_colors.yaml)
        red = RGBColor(self.machine.config["named_colors"]["red"]).rgb
        for name in ["l_pit_arrow2", "l_pit_arrow1", "l_pit_fuel",
                "l_pit_lube", "l_pit_tires"]:
            self.assertIn(red, seen[name], name)
            self.assertIn((0, 0, 0), seen[name], name)
        for name in ["l_grand1", "l_grand2"]:
            self.assertEqual(2, len(seen[name]), name)
        self.assertFalse(both_grand)

    def _on(self, light):
        return self.machine.lights[light].get_color().rgb != (0, 0, 0)

    # A reminder of the way out every 20s while it's on
    def test_reminder_every_20s(self):
        reminders = []
        # (it also ticks as it starts, which doesn't remind)
        def tick(ticks=0, **kwargs):
            if ticks > 0:
                reminders.append(self.machine.clock.get_time())
        self.machine.events.add_handler("timer_under_red_reminder_tick", tick)
        self._under_red()
        self.advance_time_and_run(18)
        self.assertEqual([], reminders)
        self.advance_time_and_run(43)
        self.assertEqual(3, len(reminders))
        self.hit_switch_and_run("s_hole_grand", 3)
        self.advance_time_and_run(40)
        self.assertEqual(3, len(reminders))

    # Green Flag stops however it starts (like the debug key)
    def test_debug_start_stops_green_flag(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("debug_under_red")
        self.advance_time_and_run(1)
        self.assertModeRunning("under_red")
        self.assertModeNotRunning("green_flag")
