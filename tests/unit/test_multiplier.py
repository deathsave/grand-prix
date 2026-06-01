from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestMultiplier(DeathSaveGameTesting):

    def test_swerve_qualification(self):
        self._start()
        self.assertEqual(1, self.machine.game.player.multiplier)
        self._start_green_flag()
        self._start_luxury()
        self.advance_time_and_run(5)

        # Start with multiplier of 1
        self.assertEqual(1, self.machine.game.player.multiplier)

        # once in multiball, the swerve targets
        # can activate the multiplier
        for i in range(4):
            self.hit_and_release_switch("s_swerve1")
        self.assertEqual(1, self.machine.game.player.multiplier)

        # after swerving 5 times, the
        # multiplier is increased by 1
        self.hit_and_release_switch("s_swerve1")
        self.assertEqual(2, self.machine.game.player.multiplier)

        # Swerving more doesn't bring the multiplier beyond 2
        for i in range(5):
            self.hit_and_release_switch("s_swerve1")
        self.assertEqual(2, self.machine.game.player.multiplier)

        # Eventually it expires
        self.advance_time_and_run(25)
        self.assertEqual(2, self.machine.game.player.multiplier)
        self.advance_time_and_run(5)
        self.assertEqual(1, self.machine.game.player.multiplier)

    def test_subsequent_lap_qualification(self):
        self._start()
        self.assertEqual(1, self.machine.game.player.multiplier)
        self._start_green_flag()

        # Making a lap after 15 seconds does not trigger the multiplier
        self._complete_lap()
        self.assertEqual(True, self.machine.timers["lap_to_lap"].running)
        self.advance_time_and_run(17)
        self.assertEqual(False, self.machine.timers["lap_to_lap"].running)
        self._complete_lap()
        self.assertEqual(1, self.machine.game.player.multiplier)

        # But under 15 seconds does
        self.assertEqual(True, self.machine.timers["lap_to_lap"].running)
        self.advance_time_and_run(13)
        self._complete_lap()
        self.advance_time_and_run(1)
        self.assertEqual(2, self.machine.game.player.multiplier)

        # Player CANNOT increase it again - too easy otherwise
        self._complete_lap()
        self.advance_time_and_run(1)
        self.assertEqual(2, self.machine.game.player.multiplier)

        # But eventually it will expire
        self.advance_time_and_run(25)
        self.assertEqual(2, self.machine.game.player.multiplier)
        self.advance_time_and_run(5)
        self.assertEqual(1, self.machine.game.player.multiplier)

    def test_grooveline_override(self):
        self._start()
        self._start_green_flag()
        self._complete_lap()
        self._complete_lap()

        self.assertEqual(2, self.machine.game.player.lap_count)
        self.assertEqual(
            2, self.machine.game.player.grooveline_counter_count)
        # Multiplier increases
        self.assertEqual(2, self.machine.game.player.multiplier)

        # Next lap is under multiplier and doubles the reward
        # affecting BOTH the lap_count and grooveline
        self._complete_lap()
        self.assertEqual(4, self.machine.game.player.lap_count)
        self.assertEqual(
            4, self.machine.game.player.grooveline_counter_count)

    # These need more thought to not get out of sync with
    # the counters.
    #
    # def test_luxury_override(self):
    #     self._start()
    #     self._start_green_flag()
    #     self._complete_lap()
    #     self._complete_lap()
    #     self.assertEqual(2, self.machine.game.player.multiplier)

    #     for i in range(10):
    #         self.hit_and_release_switch("s_spinner")
    #     self.assertEqual(2,
    #         self.machine.game.player.luxury_counter_count)

    # def test_grand_prix_override(self):
    #     self._start()
    #     self._start_green_flag()
    #     self._complete_lap()
    #     self._complete_lap()
    #     self.assertEqual(2, self.machine.game.player.multiplier)

    #     self.hit_and_release_switch("s_save_target")
    #     self.assertEqual(2, self.machine.game.player.grand_counter_count)

    #     self.hit_and_release_switch("s_bonus_target")
    #     self.assertEqual(2, self.machine.game.player.prix_counter_count)
