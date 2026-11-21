from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestFlippers(DeathSaveGameTesting):

    def _assertFlippers(self, enabled):
        for name in ["left_flipper", "right_flipper"]:
            self.assertEqual(enabled,
                self.machine.flippers[name]._enabled, name)

    # Flippers only work during a ball, never in attract
    def test_disabled_in_attract_after_game(self):
        self.advance_time_and_run(1)
        self.assertModeRunning("attract")
        self._assertFlippers(False)

        self._start()
        self._assertFlippers(True)

        # play through all the balls
        for i in range(3):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_activate_playfield")
            self._expire_ball_save()
            self.hit_switch_and_run("s_trough1", 2)
            # and back on for the next ball
            if i < 2:
                self._assertFlippers(True)

        # through match and back to attract
        self.advance_time_and_run(6)
        self.assertModeRunning("attract")
        self._assertFlippers(False)
