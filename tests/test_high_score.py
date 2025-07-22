from tests.death_save_game_testing import DeathSaveGameTesting

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

        # score a bunch of points
        for i in range(30):
            self.hit_and_release_switch("s_pit_lube")
        self._drain_one_ball()

        # wait out bonus
        self.advance_time_and_run(18)

        self.assertModeRunning("high_score")
        current_widgets = self.get_text_widgets()
        self.assertIn("Driver 1",
            [x.text for x in current_widgets])

    def get_text_widgets(self):
        current_widgets = []
        for w in self.mc.displays['apron'].current_slide.widgets:
            if hasattr(w.widget, 'text'):
                current_widgets.append(w.widget)
        return current_widgets
