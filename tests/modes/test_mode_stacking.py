from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestModeStacking(DeathSaveGameTesting):

    def test_stacking_grooveline_and_luxury(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()

        self._start_grooveline()
        self.advance_time_and_run(5)
        self.assertEqual(2, self.machine.playfield.balls)

        self._start_luxury()

        self.assertModeRunning("green_flag")
        self.assertModeRunning("grooveline")
        self.assertModeRunning("luxury")

        # expire any ball saves
        self.advance_time_and_run(30)

        self._drain_one_ball()
        self.advance_time_and_run(2)

        # Both 2 ball multiballs end together
        self.assertModeRunning("green_flag")
        self.assertModeNotRunning("grooveline")
        self.assertModeNotRunning("luxury")
        # self.assertEqual(1, self.machine.playfield.balls)

        # TODO: continue building this out
