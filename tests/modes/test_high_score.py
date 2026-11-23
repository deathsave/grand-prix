from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestHighScore(DeathSaveGameTesting):

    def test_score_entry(self):
        self._start()

        # blow through the first two balls
        for ball in range(1, 3):
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_activate_playfield")
            self._expire_ball_save()
            self.assertEqual(ball, self.machine.game.player.ball)

            # ball drains and next ball begins
            self._drain_one_ball()

            # wait out bonus
            self.advance_time_and_run(18)

        # now we're on ball 3
        self.assertEqual(3, self.machine.game.player.ball)
        self.hit_and_release_switch("s_shooter_lane")
        self._expire_ball_save()
        self.advance_time_and_run(10)
        self.assertEqual(2,
            self.machine.ball_devices["bd_trough"].balls)

        # score a bunch of points (past the lowest default, 150k, but
        # under the 500k replay, which would be an extra ball)
        for i in range(30):
            self.hit_and_release_switch("s_pit_lube")
        self.machine.game.player.score += 200000
        self._drain_one_ball()

        self.advance_time_and_run(1)

        self.assertModeRunning("high_score")

    # The initials move the way of the button pressed: the flipper tags
    # are swapped relative to the buttons (left_flipper is the
    # physically right one), so left is the right_flipper tag
    def test_initials_follow_the_buttons(self):
        from ruamel.yaml import YAML
        config = YAML(typ="safe").load(
            open("modes/high_score/config/high_score.yaml"))
        entry = [ w for w in config["slides"]["high_score_enter_initials"]
            if w.get("type") == "text_input" ][0]
        self.assertEqual("sw_right_flipper", entry["shift_left_event"])
        self.assertEqual("sw_left_flipper", entry["shift_right_event"])
        switches = YAML(typ="safe").load(
            open("config/common/switches.yaml"))["switches"]
        self.assertIn("left_flipper", switches["s_flipper1"]["tags"])
