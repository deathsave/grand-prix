from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestModeStacking(DeathSaveGameTesting):

    # Grooveline and Luxury don't stack: Luxury qualified during
    # Grooveline waits, and starts as soon as Grooveline ends (see
    # modes/green_flag/config/event_player.yaml)
    def test_grooveline_then_luxury(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()

        self._start_grooveline()
        self.advance_time_and_run(5)
        self.assertEqual(2, self.machine.playfield.balls)

        # Luxury's chain fills, but the target doesn't stack it
        for i in range(80):
            self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(1)
        self.assertEqual(10, self.machine.game.player.luxury_counter_count)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(4)
        self.assertModeRunning("grooveline")
        self.assertModeNotRunning("luxury")

        # expire any ball saves
        self.advance_time_and_run(30)

        # Grooveline's lost: Luxury starts, with its 2 balls
        self._drain_one_ball()
        self.advance_time_and_run(2)
        self.assertModeRunning("green_flag")
        self.assertModeNotRunning("grooveline")
        self.assertModeRunning("luxury")
        self.advance_time_and_run(8)
        self.assertEqual(2, self.machine.playfield.balls)
