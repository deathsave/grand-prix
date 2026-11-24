from mpf.platforms.interfaces.segment_display_platform_interface import \
    FlashingType
from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestSegmentEffects(DeathSaveGameTesting):

    def _text(self, number):
        return str(self.machine.segment_displays[f"segment{number}"]
            .text).strip()

    def _flashing(self, number):
        return self.machine.segment_displays[f"segment{number}"].flashing

    def _module(self):
        from code.segment_displays import SegmentDisplays
        return [code for code in self.machine.custom_code
            if isinstance(code, SegmentDisplays)][0]

    # Off the Line's start tree: all four count down 3-2-1 together, and
    # the scores come back on green
    def test_start_tree(self):
        self._start()
        for digit in [3, 2, 1]:
            self.post_event(f"off_the_line_countdown{digit}")
            self.advance_time_and_run(0.5)
            for n in range(1, 5):
                self.assertEqual(str(digit) * 7, self._text(n))
        self.post_event("green_flag_dropped")
        self.advance_time_and_run(0.1)
        self.assertEqual(str(self.machine.game.player.score), self._text(1))
        self.assertEqual("", self._text(2))

    # (and it really runs with Green Flag's countdown)
    def test_start_tree_with_green_flag(self):
        self._start_and_expire_ball_save()
        seen = set()
        self.hit_and_release_switch("s_pit_fuel")
        for i in range(80):
            self.advance_time_and_run(0.1)
            seen.add(self._text(3))
        self.assertTrue({"3333333", "2222222", "1111111"} <= seen, seen)
        self.assertEqual("", self._text(3))

    # A big award rolls the score up to its new total
    def test_count_up(self):
        self._start()
        player = self.machine.game.player
        player.score = 10000
        self.advance_time_and_run(1)
        player.score += 75000
        self.advance_time_and_run(0.2)
        partway = int(self._text(1))
        self.assertLess(10000, partway)
        self.assertLess(partway, 85000)
        self.advance_time_and_run(0.6)
        self.assertEqual("85000", self._text(1))

    # a small one just jumps
    def test_small_scores_jump(self):
        self._start()
        player = self.machine.game.player
        player.score = 10000
        self.advance_time_and_run(1)
        player.score += 5000
        self.advance_time_and_run(0.05)
        self.assertEqual("15000", self._text(1))

    # a small one during a count-up: it counts to the new total
    def test_small_score_during_count_up(self):
        self._start()
        player = self.machine.game.player
        player.score += 100000
        self.advance_time_and_run(0.1)
        player.score += 50
        self.advance_time_and_run(1)
        self.assertEqual("100050", self._text(1))

    # Pure Evil: the other displays alternate the 666s, the current
    # player's keeps their score
    def test_pure_evil(self):
        self._start()
        self.machine.game.player.score = 4560
        self.post_event("mode_pure_evil_started")
        seen = set()
        for i in range(6):
            self.advance_time_and_run(0.2)
            self.assertEqual("4560", self._text(1))
            for n in [2, 3, 4]:
                seen.add(str(self.machine.segment_displays[f"segment{n}"]
                    .text))
        self.assertEqual({"    666", "666 666", "666    "}, seen)
        self.post_event("mode_pure_evil_stopped")
        self.advance_time_and_run(0.5)
        for n in [2, 3, 4]:
            self.assertEqual("", self._text(n))

    # The winning score blinks as a multiplayer game ends (ties both
    # blink), not in a 1 player game, and it's gone after the game
    def test_winner_blinks(self):
        self._start()
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        players = self.machine.game.player_list
        players[0].score, players[1].score = 50000, 80000
        self.advance_time_and_run(1)
        module = self._module()
        module.blink_winner()
        self.advance_time_and_run(0.1)
        self.assertEqual(("80000", FlashingType.FLASH_ALL),
            (self._text(2), self._flashing(2)))
        self.assertEqual(FlashingType.NO_FLASH, self._flashing(1))
        players[0].score = 80000
        module.blink_winner()
        self.advance_time_and_run(0.1)
        self.assertEqual(FlashingType.FLASH_ALL, self._flashing(1))
        module.clear()
        self.advance_time_and_run(0.1)
        self.assertEqual(FlashingType.NO_FLASH, self._flashing(1))
        self.assertEqual(FlashingType.NO_FLASH, self._flashing(2))

    def test_no_winner_in_one_player_games(self):
        from code.segment_displays import SegmentDisplays
        self._start()
        self.assertEqual([], SegmentDisplays.winners(self.machine.game))
