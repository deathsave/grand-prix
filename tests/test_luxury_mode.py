from tests.death_save_game_testing import DeathSaveGameTesting

class TestLuxuryMode(DeathSaveGameTesting):

    # Player qualifies by making 50 laps
    # accumulating across all 3 balls
    def test_qualification(self):
        self._start()
        self._start_green_flag()

        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        # Count doesn't reset between balls
        # in contrast with grooveline mode
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)

        # Mult-ball light indicators off
        self.assertLightColor('l_north_advance1', 'black')
        self.assertLightColor('l_north_advance2', 'black')

        # Players makes 50 laps
        self._start_luxury()

        # Mult-ball light indicators on
        self.assertLightColor('l_north_advance1', 'white')
        self.assertLightColor('l_north_advance2', 'white')


    def test_multiball(self):
        pass

    def test_stacking_on_grooveline(self):
        pass
