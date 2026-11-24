from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestRacingGods(DeathSaveGameTesting):
    # Every 3 laps the Racing Gods decide: wear and tear, a wreck, bad
    # luck, or (20%) a kindness: smooth sailing or one of 4 blessings

    def _race(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        return self.machine.game.player

    def test_the_odds(self):
        events = self.machine.modes["green_flag"].config[
            "random_event_player"]
        weights = list(events.values())[0]["events"]
        self.assertEqual(100, sum(weights.values()))
        kind = ["green_flag_smooth_sailing", "racing_gods_safety_car",
            "racing_gods_sponsor", "racing_gods_slipstream",
            "racing_gods_lucky_charm"]
        self.assertEqual(20, sum(weights[event] for event in kind))

    # Safety Car: 15s of ball save
    def test_safety_car(self):
        player = self._race()
        save = self.machine.ball_saves["safety_car"]
        self.assertFalse(save.enabled)
        self.post_event("racing_gods_safety_car")
        self.advance_time_and_run(1)
        self.assertTrue(save.enabled)
        ball = player.ball
        self.hit_switch_and_run("s_trough1", 3)
        self.assertEqual(ball, self.machine.game.player.ball)
        self.assertFalse(save.enabled)
        # (and it runs out)
        self.post_event("racing_gods_safety_car")
        self.advance_time_and_run(18)
        self.assertFalse(save.enabled)

    # Sponsor Money: 25,000
    def test_sponsor(self):
        player = self._race()
        score = player.score
        self.post_event("racing_gods_sponsor")
        self.advance_time_and_run(1)
        self.assertEqual(score + 25000, player.score)

    # Slipstream: 2X, or the multiplier's 30s again if it's higher
    def test_slipstream(self):
        player = self._race()
        timer = self.machine.timers["multiplier"]
        self.post_event("racing_gods_slipstream")
        self.advance_time_and_run(1)
        self.assertEqual(2, player.multiplier)
        self.assertTrue(timer.running)
        self.advance_time_and_run(20)
        self.post_event("racing_gods_slipstream")
        self.advance_time_and_run(1)
        self.assertEqual(2, player.multiplier)
        self.assertGreater(timer.ticks, 25)

    # Lucky Charm: lights the outlane save
    def test_lucky_charm(self):
        player = self._race()
        self.assertEqual(0, player.is_outlane_save_lit)
        self.post_event("racing_gods_lucky_charm")
        self.advance_time_and_run(1)
        self.assertEqual(1, player.is_outlane_save_lit)

    # The safety car keeps the outlane save for when it's needed
    def test_safety_car_keeps_the_outlane_save(self):
        player = self._race()
        player.is_outlane_save_lit = 1
        self.post_event("racing_gods_safety_car")
        self.advance_time_and_run(1)
        self.mock_event("outlane_save_redeemed")
        self.hit_and_release_switch("s_outlane2")
        self.advance_time_and_run(0.5)
        self.assertEventNotCalled("outlane_save_redeemed")
        self.assertEqual(1, player.is_outlane_save_lit)
