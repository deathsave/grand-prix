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

    # Starts at 500k
    def test_starts_at_half_a_million(self):
        self.advance_time_and_run(10)
        self.assertEqual(500000, self._replay_score())

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

    def _final_score(self):
        final = []
        def ending(**kwargs):
            final.append(self.machine.game.player.score)
        self.machine.events.add_handler("game_ending", ending, priority=100)
        return final

    # After a game with a replay, it's 1.5x their final score (to 10k)
    def test_raised_to_one_and_a_half_times_their_score(self):
        final = self._final_score()
        self._start()
        self.machine.game.player.score += 1600000
        self.advance_time_and_run(1)
        # (the replay's extra ball)
        self._play_out()
        self._play_out()
        self.assertIsNone(self.machine.game)
        self.assertEqual(round(final[0] * 1.5 / 10000) * 10000,
            self._replay_score())

    # The best of the players who got a replay
    def test_best_of_the_replays(self):
        final = []
        def ending(**kwargs):
            final.extend(p.score for p in self.machine.game.player_list)
        self.machine.events.add_handler("game_ending", ending, priority=100)
        self._start()
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        players = self.machine.game.player_list
        self.assertEqual(2, len(players))
        players[0].score += 2600000
        self.advance_time_and_run(1)
        # (6 balls, and player 1's extra ball)
        for i in range(15):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            self.hit_switch_and_run("s_trough1", 2)
            self.advance_time_and_run(20)
            if not self.machine.game:
                break
        self.assertIsNone(self.machine.game)
        # (player 2 never got one, so only player 1's counts)
        self.assertEqual(round(final[0] * 1.5 / 10000) * 10000,
            self._replay_score())

    # Halved after 50 games in a row without one
    def test_halved_after_fifty_games_without(self):
        self.advance_time_and_run(1)
        self.machine.variables.set_machine_var("replay_games_without", 48)
        for game in range(2):
            self.assertEqual(500000, self._replay_score())
            self._start()
            self._play_out()
            self.assertIsNone(self.machine.game)
        self.assertEqual(250000, self._replay_score())
        self.assertEqual(0, self.machine.variables.get_machine_var(
            "replay_games_without"))

    # but never below 150k
    def test_never_below_the_floor(self):
        self.advance_time_and_run(1)
        self.machine.variables.set_machine_var("replay_score", 200000)
        self.machine.variables.set_machine_var("replay_games_without", 49)
        self._start()
        self._play_out()
        self.assertEqual(150000, self._replay_score())

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
