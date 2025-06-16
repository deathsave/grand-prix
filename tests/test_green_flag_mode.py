from tests.death_save_game_testing import DeathSaveGameTesting

class TestGreenFlagMode(DeathSaveGameTesting):

    def test_scoring(self):
        score = "score"

        # Workaround to use the incandescent
        # driver for the mini coils
        # self.assertLightColor('x_loop_gate', 'black')

        self._start()
        self._start_green_flag()
        # 100 points for having hit the fuel switch...
        self.assertEqual(self.machine.game.player.score, 100)

        self._assertIncrement(score, "s_pop1", 10)
        self._assertIncrement(score, "s_pop2", 10)
        self._assertIncrement(score, "s_grooveline", 100)

        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)
        self._assertIncrement(score, "s_backfire_hole", 500)
        self._assertIncrement(score, "s_prix_hole", 100)
        self._assertIncrement(score, "s_grand_hole", 100)
        self._assertIncrement(score, "s_spinner", 10)
        self._assertIncrement(score, "s_save_target", 10)
        self._assertIncrement(score, "s_bonus_target", 10)
        self._assertIncrement(score, "s_swerve1", 10)
        self._assertIncrement(score, "s_swerve2", 10)
        self._assertIncrement(score, "s_slingshot1", 10)
        self._assertIncrement(score, "s_slingshot2", 10)
        self._assertIncrement(score, "s_inlane1", 25)
        self._assertIncrement(score, "s_inlane2", 25)
        self._assertIncrement(score, "s_outlane1", 50)
        self._assertIncrement(score, "s_outlane2", 50)

        # Bubbled up from the pit mode
        self._assertIncrement(score, "s_pit_fuel", 100)
        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)

    def test_laps(self):
        random_events = [
            "green_flag_smooth_sailing",
            "green_flag_degrade_fuel",
            "green_flag_degrade_lube",
            "green_flag_degrade_tires",
            "green_flag_degrade_all",
            "green_flag_under_red",
            "green_flag_bad_luck",
        ]
        # No random event should have occurred, yet
        for event in random_events:
            self.mock_event(event)
            self.assertEqual(0, self._events.get(event, 0))

        self._start()
        self._start_green_flag()

        for i in range(3):
            self._complete_lap()
        self.assertEqual(
            3, self.machine.game.player.lap_counter_count)

        # Recording 3 laps triggers a single random event
        random_events_fired = []
        for e in random_events:
            random_events_fired.append(self._events.get(e, 0))
        self.assertEqual(1, sum(random_events_fired))
        # NOTE: we're testing the event here, not the mode
        #       since the mode could end up stopped

    def test_qualification(self):
        self._start()
        self.assertModeNotRunning("green_flag")

        self.hit_and_release_switch("s_pit_fuel")
        self.assertEqual(
            2, self.machine.game.player.level_fuel)
        self.assertModeRunning("green_flag")

        # player hits the disqualifier which triggers
        # the random event "green_flag_degrade_lube" reducing the
        # player's lube level from 2 to 1
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.level_lube)
        self.assertModeRunning("green_flag")

        # player's poor luck continues as they hit the
        # disqualifier again, triggering the same event,
        # reducing their lube level from 1 to 0
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)
        self.assertEqual(
            0, self.machine.game.player.level_lube)
        self.assertModeNotRunning("green_flag")

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
