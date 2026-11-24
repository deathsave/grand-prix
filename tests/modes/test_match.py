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
        from modes.match.code.match import GrandPrixMatch
        # (the player's number always matches)
        patcher = patch.object(GrandPrixMatch, "_get_winner_number",
            lambda match, numbers, percentage: numbers[0])
        patcher.start()
        self.addCleanup(patcher.stop)
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        # (start is blocked for 5s after a toggle)
        self.advance_time_and_run(5.5)
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
        from modes.match.code.match import GrandPrixMatch
        patcher = patch.object(GrandPrixMatch, "_get_winner_number",
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

    # MPF's chance was match_percentage to the power of how many
    # different numbers the players had (a 2 or 3 player game nearly
    # always matched). Each different number gets its own 10% now
    def test_match_odds(self):
        import random
        from modes.match.code.match import GrandPrixMatch
        from modes.match.code.match import GrandPrixMatch
        mode = self.machine.modes["match"]
        self.assertIsInstance(mode, GrandPrixMatch)
        random.seed(86)
        for numbers, expected in [([30], 0.10), ([30, 50], 0.19),
                ([30, 50, 70], 0.271)]:
            wins = sum(mode._get_winner_number(numbers, 10) in numbers
                for i in range(20000))
            self.assertAlmostEqual(expected, wins / 20000, delta=0.01,
                msg=numbers)
        # and a miss is never anyone's number
        for i in range(500):
            winner = mode._get_winner_number([30, 50, 70], 0)
            self.assertNotIn(winner, [30, 50, 70])
            self.assertEqual(0, winner % 10)

    # The segment displays spin with the match: two players, player 2
    # matching (player 1's number is 10 higher), every digit the same
    # number, settling on the match number, then the scores again with
    # the winner's blinking
    def _play_two_to_match(self, player2_matches):
        from unittest.mock import patch
        from modes.match.code.match import GrandPrixMatch
        patcher = patch.object(GrandPrixMatch, "_get_winner_number",
            lambda match, numbers, percentage:
                numbers[1] if player2_matches else 90 if 90 not in numbers
                else 80)
        patcher.start()
        self.addCleanup(patcher.stop)
        self._start()
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        players = self.machine.game.player_list
        players[0].score = 12340
        players[1].score = 5670
        for ball in range(6):
            self.hit_and_release_switch("s_shooter_lane")
            self._expire_ball_save()
            # (keep the scores' last digits)
            players[0].score, players[1].score = 12340, 5670
            self.hit_switch_and_run("s_trough1", 0.05)
            # (from the moment the match starts)
            for i in range(60):
                if self.machine.modes["match"].active:
                    return
                self.advance_time_and_run(0.05)
            self.advance_time_and_run(20)
        self.fail("no match")

    def _text(self, number):
        display = self.machine.segment_displays[f"segment{number}"]
        return str(display.text).strip(), display.flashing

    def test_displays_spin(self):
        from mpf.platforms.interfaces.segment_display_platform_interface \
            import FlashingType
        self._play_two_to_match(True)
        seen = set()
        for i in range(28):
            self.advance_time_and_run(0.1)
            one, two = self._text(1)[0], self._text(2)[0]
            # every digit the same, on both displays
            self.assertEqual(1, len(set(one)), one)
            self.assertEqual(one, two)
            seen.add(one[0])
        self.assertEqual(set("0123456789"), seen)
        # it settles on the match number (70) by 5s
        self.advance_time_and_run(2.2)
        self.assertEqual(("7777777", FlashingType.NO_FLASH), self._text(1))
        # the result at 6s: player 2's score blinks, player 1's doesn't
        self.advance_time_and_run(1)
        self.assertModeRunning("match")
        self.assertEqual(("12340", FlashingType.NO_FLASH), self._text(1))
        self.assertEqual(("5670", FlashingType.FLASH_ALL), self._text(2))
        # for 2s, then the game's over
        self.advance_time_and_run(2.5)
        self.assertModeNotRunning("match")
        self.assertIsNone(self.machine.game)

    # With no match, the game's winner (player 1) blinks instead, for 2s
    def test_no_match_blinks_the_winner(self):
        from mpf.platforms.interfaces.segment_display_platform_interface \
            import FlashingType
        self._play_two_to_match(False)
        self.advance_time_and_run(5.5)
        self.assertEqual("9999999", self._text(1)[0])
        self.advance_time_and_run(1)
        self.assertEqual(("12340", FlashingType.FLASH_ALL), self._text(1))
        self.assertEqual(("5670", FlashingType.NO_FLASH), self._text(2))
        self.advance_time_and_run(1)
        self.assertModeRunning("match")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("match")
