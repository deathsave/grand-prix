from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestGreenFlagMode(DeathSaveGameTesting):

    def test_scoring(self):
        score = "score"

        self._start()
        self._start_green_flag()
        # 100 points for having hit the fuel switch...
        self.assertEqual(self.machine.game.player.score, 100)

        self._assertIncrement(score, "s_pop1", 50)
        self._assertIncrement(score, "s_pop2", 50)
        self._assertIncrement(score, "s_grooveline", 500)

        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)
        self._assertIncrement(score, "s_hole_backfire", 2500)
        self._assertIncrement(score, "s_hole_prix", 500)
        self._assertIncrement(score, "s_hole_grand", 500)
        self._assertIncrement(score, "s_spinner", 50)
        self._assertIncrement(score, "s_target_save", 50)
        self._assertIncrement(score, "s_target_bonus", 50)
        self._assertIncrement(score, "s_swerve1", 50)
        self._assertIncrement(score, "s_swerve2", 50)
        self._assertIncrement(score, "s_slingshot1", 50)
        self._assertIncrement(score, "s_slingshot2", 50)
        self._assertIncrement(score, "s_inlane1", 150)
        self._assertIncrement(score, "s_inlane2", 150)
        self._assertIncrement(score, "s_outlane1", 250)
        self._assertIncrement(score, "s_outlane2", 250)

        # Bubbled up from the pit mode
        self._assertIncrement(score, "s_pit_fuel", 100)
        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)

    def test_laps(self):
        self._start()
        self._start_green_flag()

        for i in range(2):
            self._complete_lap()
        self.assertEqual(2, self.machine.game.player.lap_counter_count)

        # Can also make laps via the pop bumpers
        for i in range(10):
            self.hit_and_release_switch("s_pop1")
            self.hit_and_release_switch("s_pop2")
        self.assertEqual(3, self.machine.game.player.lap_counter_count)

    def test_qualification(self):
        self._start()
        self.assertModeNotRunning("green_flag")

        self.hit_and_release_switch("s_pit_fuel")
        self.assertEqual(2, self.machine.game.player.level_fuel)
        self.assertModeRunning("green_flag")

        # player hits the disqualifier which triggers
        # the random event "green_flag_degrade_lube" reducing the
        # player's lube level from 2 to 1
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.game.player.level_lube)
        self.assertModeRunning("green_flag")

        # player's poor luck continues as they hit the
        # disqualifier again, triggering the same event,
        # reducing their lube level from 1 to 0
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(0, self.machine.game.player.level_lube)
        self.assertModeNotRunning("green_flag")

    def test_auto_qualification(self):
        self._start_and_expire_ball_save()
        self.assertModeNotRunning("green_flag")

        # ball drains
        self.hit_switch_and_run("s_trough1", 3)

        # next ball begins and bonus has been skipped
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertModeRunning("green_flag")

        # Loop gate is still open for ball launch
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].enabled)
        self.hit_and_release_switch("s_shooter_lane")
        # (it's a plunge once the switch has stayed open 80ms)
        self.advance_time_and_run(0.1)
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)


    def test_loop_gate(self):
        self._start()
        # shut after the plunge, and the spinner doesn't open it in the
        # pit (only under green)
        self.advance_time_and_run(6)
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)
        self.hit_and_release_switch("s_spinner")
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

        self._start_green_flag()
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].enabled)
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

        # hitting the spinner activates the loop gate
        self.hit_and_release_switch("s_spinner")
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.advance_time_and_run(4)
        # still active after 4 seconds
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.advance_time_and_run(2)
        # no longer active after 2 more (it holds 5s)
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

        # reactivate and disable with the grooveline switch
        self.hit_and_release_switch("s_spinner")
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

    def test_random_green_flag_degrade_fuel_event(self):
        self._start()
        self._start_green_flag()
        self.machine.events.post("green_flag_degrade_fuel")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.level_fuel)
        self.assertModeRunning("green_flag")
        self.machine.events.post("green_flag_degrade_fuel")
        self.advance_time_and_run(1)
        self.assertEqual(
            0, self.machine.game.player.level_fuel)
        self.assertEqual(
            2, self.machine.game.player.level_lube)
        self.assertEqual(
            2, self.machine.game.player.level_tires)
        self.assertModeNotRunning("green_flag")

    def test_random_green_flag_degrade_lube_event(self):
        self._start()
        self._start_green_flag()
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.level_lube)
        self.assertModeRunning("green_flag")
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(
            0, self.machine.game.player.level_lube)
        self.assertEqual(
            2, self.machine.game.player.level_tires)
        self.assertEqual(
            2, self.machine.game.player.level_fuel)
        self.assertModeNotRunning("green_flag")
        # self.machine.events.post("green_flag_bad_luck")
        # self.machine.events.post("green_flag_smooth_sailing")

    def test_random_green_flag_degrade_tires_event(self):
        self._start()
        self._start_green_flag()
        self.machine.events.post("green_flag_degrade_tires")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.level_tires)
        self.assertModeRunning("green_flag")
        self.machine.events.post("green_flag_degrade_tires")
        self.advance_time_and_run(1)
        self.assertEqual(
            0, self.machine.game.player.level_tires)
        self.assertEqual(
            2, self.machine.game.player.level_lube)
        self.assertEqual(
            2, self.machine.game.player.level_fuel)
        self.assertModeNotRunning("green_flag")

    def test_random_green_flag_degrade_all_event(self):
        self._start()
        self._start_green_flag()
        self.machine.events.post("green_flag_degrade_all")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.level_tires)
        self.assertEqual(
            1, self.machine.game.player.level_lube)
        self.assertEqual(
            1, self.machine.game.player.level_fuel)
        self.assertModeRunning("green_flag")
        self.machine.events.post("green_flag_degrade_all")
        self.advance_time_and_run(1)
        self.assertEqual(
            0, self.machine.game.player.level_tires)
        self.assertEqual(
            0, self.machine.game.player.level_lube)
        self.assertEqual(
            0, self.machine.game.player.level_fuel)
        self.assertModeNotRunning("green_flag")

    # All bad luck events disable the flippers
    def test_random_bad_luck_event(self):
        self._start()
        self._start_green_flag()
        self.assertTrue(
            self.machine.flippers["left_flipper"]._enabled
        )
        self.assertTrue(
            self.machine.flippers["right_flipper"]._enabled
        )

        self.machine.events.post("green_flag_bad_luck")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("green_flag")
        self.assertFalse(
            self.machine.flippers["left_flipper"]._enabled
        )
        self.assertFalse(
            self.machine.flippers["right_flipper"]._enabled
        )

    # Bad luck lights every RGB insert solid red (like Pure Evil,
    # without the flashing) until the ball drains
    def test_bad_luck_lights(self):
        from mpf.core.rgb_color import RGBColor
        red = RGBColor("red").rgb
        rgb = ["l_loop01", "l_grooveline05", "l_pit_fuel", "l_hole_grand"]
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.machine.events.post("green_flag_bad_luck")
        for i in range(5):  # steady, not flashing
            self.advance_time_and_run(0.3)
            for light in rgb:
                self.assertEqual(red,
                    self.machine.lights[light].get_color().rgb, light)
        # the ball drains: back to normal for the next ball
        self.hit_switch_and_run("s_trough1", 6)
        self.assertEqual(2, self.machine.game.player.ball)
        for light in rgb:
            self.assertNotEqual(red,
                self.machine.lights[light].get_color().rgb, light)
