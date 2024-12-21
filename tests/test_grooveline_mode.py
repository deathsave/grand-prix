from tests.death_save_game_testing import DeathSaveGameTesting

class TestGroovelineMode(DeathSaveGameTesting):

    def test_qualification(self):
        self._start_green_flag()

        self.hit_and_release_switch("s_spinner")
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        self.machine.events.post("degrade_oil")
        self.machine.events.post("degrade_oil")
        self.advance_time_and_run(1)

        self.assertModeNotRunning("green_flag")

        # Count doesn't increase outside of green_flag mode
        self.hit_and_release_switch("s_spinner")
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        # Player tops up the oil, reactivating green_flag mode
        self.hit_and_release_switch("s_qualifier2")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        # Grooveline counter still at 1 as its value is
        # persisted for a single ball
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)
        self.assertEqual(1, self.machine.game.player.ball)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        self.assertModeRunning("base")

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine.game.player.ball)
        # Grooveline counter is reset to 0
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)

        # Players hits the grooveline 10 times (10 laps)
        for i in range(10):
            # mock the event, so we avoid the random events
            self.machine.events. \
                post("logicblock_seq_lap_complete")
            self.advance_time_and_run(1)

        # Counter resets
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)
        # And grooveline mode begins (multiball)
        self.assertModeRunning("grooveline")
