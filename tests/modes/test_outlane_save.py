from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestOutlaneSave(DeathSaveGameTesting):

    def _lit(self):
        return self.machine.lights["l_outlane_bottom1"].get_color().rgb \
            != (0, 0, 0)

    def _complete_grand(self):
        for i in range(5):
            self.hit_and_release_switch("s_target_save")
            self.advance_time_and_run(0.2)
        self.assertEqual(5, self.machine.game.player.grand_counter_count)

    # Completing the Grand counter lights the save (the heart)
    def test_grand_counter_lights_it(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.advance_time_and_run(1)
        self.assertFalse(self._lit())
        self._complete_grand()
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.game.player.is_outlane_save_lit)
        self.assertTrue(self._lit())

    def _redeem(self, outlane):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        player = self.machine.game.player
        player.is_outlane_save_lit = 1
        self.advance_time_and_run(1)
        self.mock_event("outlane_save_redeemed")
        balls = self.machine.playfield.available_balls
        self.hit_and_release_switch(outlane)
        self.advance_time_and_run(0.1)
        self.assertEventCalled("outlane_save_redeemed")
        self.assertEqual(0, player.is_outlane_save_lit)
        # another ball's on its way
        self.assertEqual(balls + 1, self.machine.playfield.available_balls)
        self.advance_time_and_run(1)
        self.assertFalse(self._lit())
        # the outlaned ball drains, and it's still the same ball
        ball = player.ball
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(5)
        self.assertEqual(ball, self.machine.game.player.ball)
        self.assertEqual(1, self.machine.game.player.number)
        self.assertModeRunning("pit")

    # Either outlane uses it, kicking out another ball, and the
    # outlaned ball's drain doesn't end the ball
    def test_left_outlane_uses_it(self):
        self._redeem("s_outlane1")

    def test_right_outlane_uses_it(self):
        self._redeem("s_outlane2")

    # A center drain doesn't use it (it ends the ball, and it stays lit
    # for the next)
    def test_center_drain_keeps_it(self):
        self._start_and_expire_ball_save()
        player = self.machine.game.player
        player.is_outlane_save_lit = 1
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(20)
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertEqual(1, self.machine.game.player.is_outlane_save_lit)

    # Not while the ball start's save would return the ball anyway
    def test_not_during_the_ball_save(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        self.assertTrue(self.machine.ball_saves["ball_start"].enabled)
        self.machine.game.player.is_outlane_save_lit = 1
        self.mock_event("outlane_save_redeemed")
        self.hit_and_release_switch("s_outlane2")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("outlane_save_redeemed")
        self.assertEqual(1, self.machine.game.player.is_outlane_save_lit)

    # Not lit, an outlane is just an outlane
    def test_unlit(self):
        self._start_and_expire_ball_save()
        self.mock_event("outlane_save_redeemed")
        self.hit_and_release_switch("s_outlane1")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("outlane_save_redeemed")

    # Tune Up: the left inlane fills a random low resource, with its
    # callout
    def test_tune_up(self):
        self._start_and_expire_ball_save()
        player = self.machine.game.player
        player.level_fuel, player.level_lube, player.level_tires = 1, 1, 2
        self.mock_event("tune_up")
        self.hit_and_release_switch("s_inlane1")
        self.advance_time_and_run(0.5)
        self.assertEventCalled("tune_up")
        self.assertEqual(1, [player.level_fuel, player.level_lube]
            .count(2))
        self.assertModeNotRunning("green_flag")
        # the last one: racing
        self.hit_and_release_switch("s_inlane1")
        self.advance_time_and_run(1)
        self.assertEqual([2, 2, 2], [player.level_fuel, player.level_lube,
            player.level_tires])
        self.assertModeRunning("green_flag")
        # (nothing to do in Green Flag)
        self.mock_event("tune_up")
        self.hit_and_release_switch("s_inlane1")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("tune_up")

    # not out of Under Red (only the Grand hole gets you out)
    def test_tune_up_under_red(self):
        self._start_and_expire_ball_save()
        player = self.machine.game.player
        player.level_fuel, player.level_lube, player.level_tires = 1, 2, 2
        self.machine.modes["under_red"].start()
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_inlane1")
        self.advance_time_and_run(1)
        self.assertEqual(2, player.level_fuel)
        self.assertModeNotRunning("green_flag")

    # While the left lanes' switches fire on their own (the machine sets
    # is_left_lanes_working to 0), they do nothing: no outlane save from
    # the left, no Tune Up. The right outlane still works
    def test_left_lanes_not_working(self):
        self._start_and_expire_ball_save()
        self.machine.variables.set_machine_var("is_left_lanes_working", 0)
        player = self.machine.game.player
        player.level_fuel = 1
        self.mock_event("tune_up")
        self.hit_and_release_switch("s_inlane1")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("tune_up")
        self.assertEqual(1, player.level_fuel)
        self._start_green_flag()
        player.is_outlane_save_lit = 1
        self.mock_event("outlane_save_redeemed")
        self.mock_event("outlane_drain")
        self.mock_event("outlane_saved")
        self.hit_and_release_switch("s_outlane1")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("outlane_save_redeemed")
        self.assertEventNotCalled("outlane_drain")
        self.assertEventNotCalled("outlane_saved")
        self.hit_and_release_switch("s_outlane2")
        self.advance_time_and_run(0.5)
        self.assertEventCalled("outlane_save_redeemed")
