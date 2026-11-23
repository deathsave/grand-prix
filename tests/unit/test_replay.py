from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestReplay(DeathSaveGameTesting):

    def _replay_score(self):
        return self.machine.variables.get_machine_var("replay_score")

    def _credits(self):
        return self.machine.variables.get_machine_var("credits_whole_num")

    def _play_out(self):
        for ball in range(3):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            self.hit_switch_and_run("s_trough1", 2)
            self.advance_time_and_run(20)

    # Starts at 1.5M
    def test_starts_at_one_and_a_half_million(self):
        self.advance_time_and_run(10)
        self.assertEqual(1500000, self._replay_score())

    # Free play: passing it is an extra ball (once a game)
    def test_free_play_extra_ball(self):
        self.mock_event("replay_awarded")
        self.mock_event("replay_credit")
        self._start()
        player = self.machine.game.player
        player.score += 1600000
        self.advance_time_and_run(1)
        self.assertEventCalled("replay_awarded")
        self.assertEventNotCalled("replay_credit")
        self.assertEqual(1, player.extra_balls)
        player.score += 1000000
        self.advance_time_and_run(1)
        self.assertEventCalled("replay_awarded", times=1)
        self.assertEqual(1, player.extra_balls)

    # Credit play: passing it is a free credit
    def test_credit_play_free_credit(self):
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(1)
        for i in range(2):
            self.hit_and_release_switch("s_credit")
            self.advance_time_and_run(0.2)
        self._start()
        self.assertEqual(0, self._credits())
        player = self.machine.game.player
        player.score += 1600000
        self.advance_time_and_run(1)
        self.assertEqual(1, self._credits())
        self.assertEqual(0, player.extra_balls)

    # Up 250k after a game with a replay
    def test_goes_up_after_a_replay(self):
        self._start()
        self.machine.game.player.score += 1600000
        self.advance_time_and_run(1)
        # (the replay's extra ball)
        self._play_out()
        self._play_out()
        self.assertIsNone(self.machine.game)
        self.assertEqual(1750000, self._replay_score())

    # Down 100k after 3 games in a row without one
    def test_comes_down_after_three_games_without(self):
        for game in range(3):
            self.assertEqual(1500000, self._replay_score())
            self._start()
            self._play_out()
            self.assertIsNone(self.machine.game)
        self.assertEqual(1400000, self._replay_score())

    # The chimes knock (rolling down twice)
    def test_chimes(self):
        from unittest.mock import MagicMock
        self._start()
        pulses = []
        for coil in ["c_chime1", "c_chime2", "c_chime3"]:
            self.machine.coils[coil].pulse = MagicMock(
                side_effect=lambda *a, coil=coil, **k: pulses.append(coil))
        self.machine.game.player.score += 1600000
        self.advance_time_and_run(2)
        self.assertEqual(["c_chime3", "c_chime2", "c_chime1"] * 2, pulses)
