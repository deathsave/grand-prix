from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestBallSaves(DeathSaveGameTesting):

    def test_start_save_consumed(self):
        self._start()
        # 4 seconds elapse here

        # player hits a switch activating the save timer
        self.hit_and_release_switch("s_activate_playfield")
        self.assertLightColor('l_shoot_again', 'white')
        self.assertLightColor('l_backbox_shoot_again', 'white')

        # save still active after another 7 seconds
        self.advance_time_and_run(7)
        self.assertLightColor('l_shoot_again', 'white')
        self.assertLightColor('l_backbox_shoot_again', 'white')

        # ball drains, save is consumed
        self._drain_one_ball()
        self.assertEqual(1, self.machine.game.player.ball)
        self.advance_time_and_run(1)
        self.assertLightColor('l_shoot_again', 'black')
        self.assertLightColor('l_backbox_shoot_again', 'black')

    def test_start_save_expires(self):
        self._start()
        # 4 seconds elapse here

        # player hits a switch activating the save timer
        self.hit_and_release_switch("s_activate_playfield")

        # save expires after another 12 seconds or so
        self.advance_time_and_run(12)
        self.assertLightColor('l_shoot_again', 'black')
        self.assertLightColor('l_backbox_shoot_again', 'black')

        # ball drains and is NOT saved
        self._drain_one_ball()
        self.advance_time_and_run(1)
        self.assertEqual(2, self.machine.game.player.ball)
