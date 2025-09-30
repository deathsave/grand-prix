from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestMatch(DeathSaveGameTesting):

    def test_match(self):
        self._start()

        # blow through all three balls
        for ball in range(3):
            self.assertModeNotRunning("match")
            self.assertEqual(ball + 1,
                self.machine.game.player.ball)
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            # drain (no bonus to wait out)
            self.hit_switch_and_run("s_trough1", 2)

        self.assertModeRunning("match")
