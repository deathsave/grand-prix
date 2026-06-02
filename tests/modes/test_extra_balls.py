from tests.support.death_save_game_testing import DeathSaveGameTesting
from unittest.mock import MagicMock

class TestExtraBalls(DeathSaveGameTesting):

    def test_qualification(self):
        self._start()
        player = self.machine.game.player

        self._start_green_flag()
        self.assertEqual(1, self.machine.playfield.balls)
        # Extra ball enabled at start
        self.assertEqual(True,
            self.machine.extra_balls["awareness"].enabled)
        # But counter for it isn't, yet
        self.assertEqual(False,
            self.machine.counters["awareness_counter"].enabled)

        # To enable it, player needs to complete the
        # prix counter which uses the same switch
        self.assertEqual(0, player.prix_counter_count)

        for i in range(4):
            self.hit_and_release_switch("s_bonus_target")

        # after a the next "sync", all the
        # prix inserts should be lit
        self.advance_time_and_run(3)
        for i in range(4):
            self.assertLightColor("l_prix_0{}". \
                format(i + 1), 'white')
        self.assertEqual(4, player.prix_counter_count)

        # Now counter is enabled
        self.assertEqual(True,
            self.machine.counters["awareness_counter"].enabled)
        self.assertEqual(0, player.awareness_counter_count)

        # Player gets 3/4 hits
        for i in range(3):
            self.hit_and_release_switch("s_bonus_target")
            self.advance_time_and_run(1)
        self.assertEqual(3, player.awareness_counter_count)

        # hit shots are unlit
        self.advance_time_and_run(3)
        for i in range(3):
            self.assertLightColor("l_prix_0{}". \
                format(i + 1), 'black')
        self.assertEqual(3, player.awareness_counter_count)

        # No extra ball yet
        self.hit_and_release_switch("s_inlane2")
        self.assertEqual(0, player.extra_balls)

        # Another hit resets the disables and resets
        # the counter, but lights the extra ball
        self.hit_and_release_switch("s_bonus_target")
        self.assertEqual(0, player.awareness_counter_count)

        # This time it's collected
        self.hit_and_release_switch("s_inlane2")
        self.assertEqual(1, player.extra_balls)

    def test_disqualification(self):
        self._start()
        player = self.machine.game.player

        self._start_green_flag()

        for i in range(4):
            self.hit_and_release_switch("s_bonus_target")
        self.assertEqual(True,
            self.machine.counters["awareness_counter"].enabled)
        self.assertEqual(0, player.awareness_counter_count)

        # Player gets 3/4 hits
        for i in range(3):
            self.hit_and_release_switch("s_bonus_target")
            self.advance_time_and_run(1)
        self.assertEqual(3, player.awareness_counter_count)

        # Then gets in the hole, disqualifying the progress
        self.hit_switch_and_run("s_prix_hole", 2)
        self.assertEqual(0, player.awareness_counter_count)
        self.hit_and_release_switch("s_inlane2")
        self.assertEqual(0, player.extra_balls)

        # Player tries again with better awareness
        for i in range(4):
            self.assertEqual(i, player.awareness_counter_count)
            self.hit_and_release_switch("s_bonus_target")
            self.advance_time_and_run(1)
        self.assertEqual(0, player.awareness_counter_count)
        self.hit_and_release_switch("s_inlane2")
        self.assertEqual(1, player.extra_balls)
