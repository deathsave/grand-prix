from tests.death_save_game_testing import DeathSaveGameTesting

class TestHighScore(DeathSaveGameTesting):

    def test_score_entry(self):
        self._start()
        self._start_green_flag()
        for i in range(10):
            self.hit_and_release_switch("s_grooveline")
            self.advance_time_and_run(1)

        for ball in range(1, 4):
            self.assertEqual(ball, self.machine.game.player.ball)
            self.hit_and_release_switch("s_pop1")

            # ball drains and ball 2 begins
            for i in range(2):
                self.hit_switch_and_run("s_trough1", 4)
                self.hit_and_release_switch("s_shooter_lane")

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
