from tests.support.death_save_game_testing import DeathSaveGameTesting
from unittest.mock import MagicMock

class TestPureEvilMode(DeathSaveGameTesting):

    # Player qualifies when their "evil_number" is
    # equal to their current lap count.
    def test_qualification(self):
        self.machine.coils["c_disqualifier_up"]. \
            pulse = MagicMock()
        self.assertEqual(0, self.machine. \
            coils["c_disqualifier_up"].pulse.call_count)

        if self.machine.variables. \
            get_machine_var("is_pure_evil_available") == 0:
            print("Pure Evil mode is not available.")
            return None

        self._start_and_expire_ball_save()
        self._start_green_flag()

        assert(self.machine.game.player.evil_number is not None)
        self.assertIn( \
            self.machine.game.player.evil_number, range(1, 21))

        self.machine.game.player. \
            lap_count = self.machine.game.player.evil_number - 1

        self.assertModeNotRunning("pure_evil")
        self._complete_lap()

        self.assertModeRunning("pure_evil")

        self.advance_time_and_run(3)
        self.assertEqual(1, self.machine. \
            coils["c_disqualifier_up"].pulse.call_count)
        # value is set to ensure not called again
        # on the current ball
        self.assertEqual(True,
            self.machine.game.player.evil_number >= 999999)

        self.advance_time_and_run(1)

        # pure_evil eats your points
        score = self.machine.game.player.score
        self.advance_time_and_run(1)
        assert(self.machine.game.player.score < score)

        # and continues to...
        score = self.machine.game.player.score
        self.advance_time_and_run(1)
        assert(self.machine.game.player.score < score)

        # until player knocks down the "disqualifier" drop
        self.hit_and_release_switch("s_disqualifier")
        self.assertModeNotRunning("pure_evil")

        # score no longer decreasing
        score = self.machine.game.player.score
        self.advance_time_and_run(1)
        self.assertEqual(score, self.machine.game.player.score)
