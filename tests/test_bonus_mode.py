from tests.death_save_game_testing import DeathSaveGameTesting

class TestBonusMode(DeathSaveGameTesting):

    def test_bonus_main(self):
        self._start()
        self._start_green_flag()
        self.assertEqual(100, self.machine.game.player.score)

        # Spinner hit 20 times to bump the first bonus insert
        for i in range(20):
            self._assertIncrement("score", "s_spinner", 10)
            self.advance_time_and_run(1)
        ball1_score = self.machine.game.player.score
        self.assertEqual(100 + 200, ball1_score)
        self.assertEqual(1, self.machine.game.player.bonus_main)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        self.advance_time_and_run(3)
        self.assertModeRunning("bonus")


        self.assertEqual(2, self.machine.game.player.ball)
        self.assertEqual(self.machine.game.player.score,
            ball1_score + 10000)
