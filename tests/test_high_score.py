from tests.death_save_game_testing import DeathSaveGameTesting

class TestHighScore(DeathSaveGameTesting):

    def test_score_entry(self):
        pass
        # TODO: This is bugged
        # self._start()
        # for ball in range(1, 4):
        #     self._expire_ball_save()
        #     self.assertEqual(ball, self.machine.game.player.ball)

        #     # ball drains and next ball begins
        #     self._drain_one_ball()
        #     self.advance_time_and_run(4)
        #     self.hit_and_release_switch("s_activate_playfield")

        # self._expire_ball_save()
        # # skip to ball 3
        # self.assertEqual(3, self.machine.game.player.ball)
        # for i in range(30):
        #     self.hit_and_release_switch("s_pit_lube")

        # self.assertModeRunning("high_score")
        # current_widgets = self.get_text_widgets()
        # self.assertIn("Driver 1",
        #     [x.text for x in current_widgets])

    def get_text_widgets(self):
        current_widgets = []
        for w in self.mc.displays['apron'].current_slide.widgets:
            if hasattr(w.widget, 'text'):
                current_widgets.append(w.widget)
        return current_widgets
