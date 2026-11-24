from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestMultiballQualifying(DeathSaveGameTesting):
    # A qualified Grooveline or Luxury stays qualified: going back to
    # the pit, or losing the ball, before the multiball target doesn't
    # lose it

    def _qualify_grooveline(self):
        for i in range(10):
            self._make_lap()
            # (past the quick-lap 2X, so each lap is one)
            self.advance_time_and_run(16)
        self.assertEqual(10, self.machine.game.player.grooveline_counter_count)

    def _qualify_luxury(self):
        for i in range(80):
            self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(1)
        self.assertEqual(10, self.machine.game.player.luxury_counter_count)

    def _pit_and_back(self):
        self.post_event("pit_required_lube")
        self.advance_time_and_run(2)
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_pit_lube")
        self.advance_time_and_run(8)
        self.assertModeRunning("green_flag")

    def _drain_and_back(self):
        ball = self.machine.game.player.ball
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(20)
        self.assertEqual(ball + 1, self.machine.game.player.ball)
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self._expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        self.assertModeRunning("green_flag")

    def _multiball_lamp_blinks(self):
        seen = set()
        for i in range(10):
            self.advance_time_and_run(0.1)
            seen.add(self.machine.lights["l_multiball"].get_color().rgb)
        return len(seen) > 1

    def _qualify_and(self, qualify, back):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        qualify()
        back()
        self.assertTrue(self._multiball_lamp_blinks())

    def test_grooveline_after_the_pit(self):
        self._qualify_and(self._qualify_grooveline, self._pit_and_back)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("grooveline")

    def test_grooveline_after_a_drain(self):
        self._qualify_and(self._qualify_grooveline, self._drain_and_back)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("grooveline")

    def test_luxury_after_the_pit(self):
        self._qualify_and(self._qualify_luxury, self._pit_and_back)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("luxury")

    def test_luxury_after_a_drain(self):
        self._qualify_and(self._qualify_luxury, self._drain_and_back)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("luxury")

    # Both qualified: Grooveline first, then Luxury after it
    def test_grooveline_first(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._qualify_luxury()
        self._qualify_grooveline()
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("grooveline")
        self.assertModeNotRunning("luxury")
        # (another hit during it isn't another multiball)
        self.machine.modes["grooveline"].stop()
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeRunning("luxury")

    # Luxury's played once a game (its chain stays maxed)
    def test_luxury_once(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._qualify_luxury()
        self.machine.game.player.is_luxury_played = 1
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("luxury")

    # Not qualified, the target's just a target
    def test_unqualified(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("grooveline")
        self.assertModeNotRunning("luxury")
