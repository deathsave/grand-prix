from tests.support.death_save_mc_testing import DeathSaveMcTesting
from unittest.mock import MagicMock

class TestBonusMode(DeathSaveMcTesting):

    def test_no_bonus_earned(self):
        self._start_and_expire_ball_save()

        # ball drains
        self.hit_switch_and_run("s_trough1", 3)

        self.assertModeNotRunning("bonus")

        # next ball begins and bonus has been skipped
        self.assertEqual(2, self.machine.game.player.ball)

    def test_bonus_main(self):
        self.machine.coils["c_chime1"].pulse = MagicMock()

        chime1_count = 0

        self._start_and_expire_ball_save()

        # Bonus is not constantly running
        self.assertModeNotRunning("bonus")

        self._start_green_flag()
        self.assertEqual(100, self.machine.game.player.score)

        # 5 for the single player game start
        # and another 3 for the first 3 signals
        # going into Green Flag Mode
        chime1_count += 8
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)

        # Spinner hit 24 times (8 per step) to bump
        # the first three bonus inserts
        for i in range(24):
            self._assertIncrement("score", "s_spinner", 50)
            self.advance_time_and_run(1)
        ball1_score = self.machine.game.player.score
        self.assertEqual(100 + (24 * 50), ball1_score)
        self.assertEqual(
            3, self.machine.game.player.luxury_counter_count)

        # 4 chimes per counter value:
        #   1st, 4th, and 7th spinner hits as well as
        #   part of a "chord" on the 8th spinner hit
        chime1_count += ( \
            self.machine.game.player.luxury_counter_count * 4)
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)

        # first 3 bonus inserts are lit
        self.assertLightColor('l_bonus01', 'white')
        self.assertLightColor('l_bonus02', 'white')
        self.assertLightColor('l_bonus03', 'white')
        self.assertLightColor('l_bonus04', 'black')

        # ball drains
        self.hit_switch_and_run("s_trough1", 3)

        # ensure multiplier is standard
        self.assertEqual(1, self.machine.game.player.multiplier)

        # bonus mode is now running
        self.assertModeRunning("bonus")
        self.advance_time_and_run(2.2)
        # at this point, chime1 fires during bonus
        # show (5 times the luxury counter value)
        # 8th step of show
        chime1_count += 5
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)
        self.assertLightColor('l_bonus01', 'white')
        self.assertLightColor('l_bonus02', 'white')
        self.assertLightColor('l_bonus03', 'black')

        self.advance_time_and_run(1)
        chime1_count += 5
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)
        self.assertLightColor('l_bonus01', 'white')
        self.assertLightColor('l_bonus02', 'black')

        self.advance_time_and_run(1)
        chime1_count += 5
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)
        self.assertLightColor('l_bonus01', 'black')

        self.advance_time_and_run(10)

        # next ball begins and bonus has been added
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertEqual(self.machine.game.player.score,
            ball1_score + 30000)

        # chime1 not fired again by the bonus: only by ball 2's Off the
        # Line countdown (Green Flag carries on into it), 3 dings. (The
        # bonus is quicker now no laps line shows with no laps)
        chime1_count += 3
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)

        # first 3 bonus inserts are restored as the
        # main bonus persists through all balls
        self.assertLightColor('l_bonus01', 'white')
        self.assertLightColor('l_bonus02', 'white')
        self.assertLightColor('l_bonus03', 'white')
        self.assertLightColor('l_bonus04', 'black')

    def test_bonus_lap(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.assertEqual(self.machine.game.player.score, 100)

        # driver makes 5 laps on ball one
        for i in range(5):
            # clear the lap to lap timer to dodge the multiplier change
            self.advance_time_and_run(17)
            self._complete_lap()

        # ball drains
        self.hit_switch_and_run("s_trough1", 3)

        # ensure multiplier is standard
        self.assertEqual(1, self.machine.game.player.multiplier)

        # - 100 for initial fuel to get into green flag
        # - 5 laps: 5,000 each, plus 500 for the Grooveline lane and
        #   50 for the spinner
        self.assertEqual(100 + 5 * (5000 + 500 + 50),
            self.machine.game.player.score)
        # bonus mode is now running
        self.assertModeRunning("bonus")

        self.advance_time_and_run(15)

        # next ball begins and bonus has been added
        self.assertEqual(2, self.machine.game.player.ball)

        # bonus of 1000 per lap made, and each lap
        # also lit a luxury insert (10,000 each)
        self.assertEqual(100 + 5 * (5000 + 500 + 50) + 5000 + 50000,
            self.machine.game.player.score)

    # Both flippers skip through the bonus (MPF's both_flippers combo
    # posts flipper_cancel, the bonus mode's hurry up)
    def test_both_flippers_skip(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        for i in range(3):
            self.advance_time_and_run(17)
            self._complete_lap()
        self.mock_event("flipper_cancel")
        self.hit_switch_and_run("s_trough1", 3)
        self.assertModeRunning("bonus")
        self.hit_switch_and_run("s_flipper1", 0.1)
        self.hit_switch_and_run("s_flipper2", 0.1)
        self.release_switch_and_run("s_flipper2", 0.1)
        self.release_switch_and_run("s_flipper1", 0.1)
        self.assertEventCalled("flipper_cancel")
        # (it takes ~15s without skipping)
        self.advance_time_and_run(4)
        self.assertModeNotRunning("bonus")
        self.assertEqual(2, self.machine.game.player.ball)

    def _var(self, name):
        return self.machine.variables.get_machine_var(name)

    def _board_texts(self):
        found = []
        def walk(widget):
            if type(widget).__name__ == "Text":
                found.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    # Multiballs played (10k each) and completed (30k each) are paid,
    # and only the lines with something in them are shown, on the
    # results board, with the total
    def test_multiball_lines(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        player = self.machine.game.player
        player.is_grooveline_played = 1
        player.is_luxury_played = 1
        player.is_grand_prix_played = 1
        self.post_event("grand_prix_super_jackpot")
        self.advance_time_and_run(1)
        self.assertEqual(1, player.is_grand_prix_super)
        score = player.score
        self.hit_switch_and_run("s_trough1", 3)
        self.assertModeRunning("bonus")
        self.assertEqual("bonus_board",
            self.mc.targets["default"].current_slide.name)
        self.advance_time_and_run(30)
        self.assertEqual(2, self.machine.game.player.ball)
        # (no Luxury inserts or laps: just the two multiball lines)
        self.assertEqual("Multiballs  x3", self._var("bonus_row1_label"))
        self.assertEqual("30,000", self._var("bonus_row1_value"))
        self.assertEqual("Super Jackpots  x1", self._var("bonus_row2_label"))
        self.assertEqual("30,000", self._var("bonus_row2_value"))
        self.assertEqual("", self._var("bonus_row3_label"))
        self.assertEqual("60,000", self._var("bonus_total_value"))
        self.assertEqual(score + 60000, player.score)

    # The board's lines slide in as the bonus pays them
    def test_board(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        for i in range(8):
            self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(1)
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(2)
        texts = self._board_texts()
        self.assertIn("End of Ball Bonus", texts)
        self.assertIn("Luxury  x1", texts)
        self.assertIn("10,000", texts)
        self.advance_time_and_run(4)
        self.assertIn("Total", self._board_texts())
