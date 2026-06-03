from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestModeStacking(DeathSaveGameTesting):

    def test_stacking(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()

        self._start_grooveline()
        self.advance_time_and_run(5)
        self.assertEqual(2, self.machine.playfield.balls)

        # TODO: continue building this out
