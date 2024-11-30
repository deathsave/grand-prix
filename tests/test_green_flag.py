"""Tests Green Flag Mode"""
import os

from mpf.tests.MpfGameTestCase import MpfGameTestCase

class TestGreenFlag(MpfGameTestCase):

    def get_config_file(self):
        return 'development.yaml'

    def get_machine_path(self):
        return os.path.abspath(os.path.join(
            os.path.realpath(__file__),
            os.pardir,os.pardir
        ))

    def test_qualification(self):
        self.start_game()
        self.assertEqual(
            0, self.machine.game.player.level_green_flag
        )
        self.assertModeNotRunning("green_flag")

        self.hit_and_release_switch("s_qualifier1")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        self.assertEqual(
            1, self.machine.game.player.level_green_flag
        )

        self.hit_and_release_switch("s_disqualifier")
        self.assertModeNotRunning("green_flag")

        # Second time around, it requires hitting two
        # qualifiers to start the mode
        self.hit_and_release_switch("s_qualifier1")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier2")
        self.assertModeRunning("green_flag")
        self.hit_and_release_switch("s_disqualifier")

        # Third time around, it requires hitting
        # all three qualifiers
        self.hit_and_release_switch("s_qualifier1")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier2")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier3")
        self.assertModeRunning("green_flag")
        self.hit_and_release_switch("s_disqualifier")

        # Further attempts function the same way,
        # requiring all 3 qualifiers to be hit
        self.hit_and_release_switch("s_qualifier1")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier2")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier3")
        self.assertModeRunning("green_flag")
        self.hit_and_release_switch("s_disqualifier")
