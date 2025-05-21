from tests.death_save_game_testing import DeathSaveGameTesting

class TestMultiplier(DeathSaveGameTesting):

    def test_qualification(self):
        self._start()
        self.assertEqual(0, self.machine.game.player.multiplier)
        self._start_green_flag()
        self._start_luxury()

        # once in multiball, the swerve targets
        # can activate the multiplier
        self.assertEqual(1, self.machine.game.player.multiplier)
        for i in range(4):
            self.hit_and_release_switch("s_swerve1")
        self.assertEqual(1, self.machine.game.player.multiplier)

        # after swerving 5 times, the
        # multiplier is increated by 1
        self.hit_and_release_switch("s_swerve1")
        self.assertEqual(2, self.machine.game.player.multiplier)
