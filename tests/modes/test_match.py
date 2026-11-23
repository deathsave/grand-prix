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

    # In credit play, a match gives back a free credit
    def test_match_awards_a_credit(self):
        from unittest.mock import patch
        from mpf.modes.match.code.match import Match
        # (the player's number always matches)
        patcher = patch.object(Match, "_get_winner_number",
            lambda match, numbers, percentage: numbers[0])
        patcher.start()
        self.addCleanup(patcher.stop)
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(1)
        for i in range(2):
            self.hit_and_release_switch("s_credit")
            self.advance_time_and_run(0.2)
        self.assertEqual(1, self.machine.variables.get_machine_var(
            "credits_whole_num"))
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNotNone(self.machine.game)
        self.assertEqual(0, self.machine.variables.get_machine_var(
            "credits_whole_num"))
        self.mock_event("match_has_match")
        for ball in range(3):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            self.hit_switch_and_run("s_trough1", 2)
        self.advance_time_and_run(15)
        self.assertEventCalled("match_has_match")
        self.assertEqual(1, self.machine.variables.get_machine_var(
            "credits_whole_num"))

    def _play_to_match(self, matched):
        from unittest.mock import patch, MagicMock
        from mpf.modes.match.code.match import Match
        patcher = patch.object(Match, "_get_winner_number",
            lambda match, numbers, percentage:
                numbers[0] if matched else (numbers[0] + 10) % 100)
        patcher.start()
        self.addCleanup(patcher.stop)
        self._start()
        for ball in range(3):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_swerve1")
            self._expire_ball_save()
            self.hit_switch_and_run("s_trough1", 2)
        self.assertModeRunning("match")
        pulses = []
        for coil in ["c_chime1", "c_chime3"]:
            self.machine.coils[coil].pulse = MagicMock(
                side_effect=lambda *a, coil=coil, **k: pulses.append(coil))
        self.advance_time_and_run(10)
        return pulses

    # A match chimes 1 then 3 (as the winning number lands)
    def test_match_chimes(self):
        self.assertEqual(["c_chime1", "c_chime3"], self._play_to_match(True))

    # No match, no chimes
    def test_no_match_no_chimes(self):
        self.assertEqual([], self._play_to_match(False))

    # A pair for each player who matched
    def test_two_winners_two_pairs(self):
        from unittest.mock import MagicMock
        self.advance_time_and_run(10)
        pulses = []
        for coil in ["c_chime1", "c_chime3"]:
            self.machine.coils[coil].pulse = MagicMock(
                side_effect=lambda *a, coil=coil, **k: pulses.append(coil))
        self.post_event_with_params("match_has_match", winners=2,
            winner_number=30)
        self.advance_time_and_run(3)
        self.assertEqual(["c_chime1", "c_chime3", "c_chime1", "c_chime3"],
            pulses)
