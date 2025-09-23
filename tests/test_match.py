from tests.death_save_game_testing import DeathSaveGameTesting

class TestMatch(DeathSaveGameTesting):

    def test_match(self):
        self._start()

        # blow through all three balls
        for ball in range(1, 4):
            self.assertModeNotRunning("match")
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            self.assertEqual(ball, self.machine.game.player.ball)

            # ball drains and next ball begins
            self._drain_one_ball()
            self.advance_time_and_run(2)

        self.assertEqual(self.machine.game.player.score, 3)
        self.assertModeRunning("match")
