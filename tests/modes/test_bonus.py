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

        # Spinner hit 30 times to bump the first
        # three bonus inserts
        for i in range(30):
            self._assertIncrement("score", "s_spinner", 10)
            self.advance_time_and_run(1)
        ball1_score = self.machine.game.player.score
        self.assertEqual(100 + (30 * 10), ball1_score)
        self.assertEqual(
            3, self.machine.game.player.luxury_counter_count)

        # 4 chimes per counter value:
        #   1st, 4th, and 7th spinner hits as well as
        #   part of a "chord" on the 10th spinner hit
        chime1_count += ( \
            self.machine.game.player.luxury_counter_count * 4)
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)

        # first 3 bonus inserts are lit
        self.assertLightColor('l_bonus_01', 'white')
        self.assertLightColor('l_bonus_02', 'white')
        self.assertLightColor('l_bonus_03', 'white')
        self.assertLightColor('l_bonus_04', 'black')

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
        self.assertLightColor('l_bonus_01', 'white')
        self.assertLightColor('l_bonus_02', 'white')
        self.assertLightColor('l_bonus_03', 'black')

        self.advance_time_and_run(1)
        chime1_count += 5
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)
        self.assertLightColor('l_bonus_01', 'white')
        self.assertLightColor('l_bonus_02', 'black')

        self.advance_time_and_run(1)
        chime1_count += 5
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)
        self.assertLightColor('l_bonus_01', 'black')

        self.advance_time_and_run(10)

        # next ball begins and bonus has been added
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertEqual(self.machine.game.player.score,
            ball1_score + 30000)

        # chime1 not fired again until after next ball begins
        self.assertEqual(chime1_count,
            self.machine.coils["c_chime1"].pulse.call_count)

        # first 3 bonus inserts are restored as the
        # main bonus persists through all balls
        self.assertLightColor('l_bonus_01', 'white')
        self.assertLightColor('l_bonus_02', 'white')
        self.assertLightColor('l_bonus_03', 'white')
        self.assertLightColor('l_bonus_04', 'black')

    def test_bonus_lap(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.assertEqual(self.machine.game.player.score, 100)

        # driver makes 5 laps on ball one
        for i in range(5):
            self._complete_lap()

        # ball drains
        self.hit_switch_and_run("s_trough1", 3)

        # ensure multiplier is standard
        self.assertEqual(1, self.machine.game.player.multiplier)

        # - 100 for initial fuel to get into green flag
        # - 500 for the 5 laps and
        # - 10 for each spinner hit during those laps
        self.assertEqual(650, self.machine.game.player.score)
        # bonus mode is now running
        self.assertModeRunning("bonus")

        self.advance_time_and_run(15)

        # next ball begins and bonus has been added
        self.assertEqual(2, self.machine.game.player.ball)

        # bonus of 1000 per lap made
        self.assertEqual(650 + 5000,
            self.machine.game.player.score)
