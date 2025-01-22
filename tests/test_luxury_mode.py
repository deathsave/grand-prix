from tests.death_save_game_testing import DeathSaveGameTesting

class TestLuxuryMode(DeathSaveGameTesting):

    # Player qualifies by making 10 laps during
    # green_flag mode on a single ball.
    def test_qualification(self):
        self._start()
        self._start_green_flag()

        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

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
