from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestBackfireMode(DeathSaveGameTesting):

    # To qualify:
    #
    # - Top hole is lit for 15 seconds when
    #   leaving green flag mode (pit stop)
    # - During that time, first hit the spinner
    # - Then enter the top hole to start the mode
    #
    def test_qualification(self):
        self._start()
        self._start_green_flag()
        self.assertModeRunning("green_flag")

        # qualification window not ready yet
        self.assertEqual(False,
            self.machine.timers["backfire_qualification"].running)
        self.assertEqual(False, self.machine. \
            sequences["seq_backfire_qualifier"].enabled)

        # player returns to the pit
        self.machine.events.post("pit_required_lube")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("green_flag")
        self.assertModeNotRunning("backfire")

        # qualification timer should be running now
        self.assertEqual(True,
            self.machine.timers["backfire_qualification"].running)
        # sequence should be enabled
        self.assertEqual(True, self.machine. \
            sequences["seq_backfire_qualifier"].enabled)

        # player hits the spinner
        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(1)
        # then enters the top hole
        self.hit_switch_and_run("s_backfire_hole", 1)

        self.assertEqual(1,
            self.machine.ball_devices["bd_backfire_hole"].balls)
        self.assertModeRunning("backfire")
        # main timer should be running now
        self.assertEqual(True,
            self.machine.timers["backfire"].running)

        # ball is kicked out after 5 seconds
        self.advance_time_and_run(5)
        self.assertEqual(0,
            self.machine.ball_devices["bd_backfire_hole"].balls)

        # timer expires after 30 more seconds and mode ends
        self.advance_time_and_run(30)
        self.assertEqual(False,
            self.machine.timers["backfire"].running)
        self.assertModeNotRunning("backfire")

    # To complete:
    #
    # - Driver targets the pop bumpers
    # - If max is reached in time, immediately return player
    #   to green flag (fuel, lube and tires are max)
    def test_green_flag_resume(self):
        self._start()
        self._start_backfire()

        self.assertEqual(1,
            self.machine.game.player.backfire_counter_count)
        for i in range(9):
            self.assertEqual(i + 1,
                self.machine.game.player.backfire_counter_count)
            self.hit_and_release_switch("s_pop1")
            self.advance_time_and_run(1)
        self.assertModeNotRunning("green_flag")

        # one more hit and player is returned to green flag
        self.hit_and_release_switch("s_pop1")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")

        # count is always reset back to 1
        self.assertEqual(1,
            self.machine.game.player.backfire_counter_count)

    def test_scoring(self):
        self._start()
        self._start_backfire()
        self.assertModeRunning("pit")
        self.assertModeRunning("backfire")
        self.assertEqual(1, self.machine.game.player.multiplier)
        for i in range(9):
            self.assertEqual(i + 1,
                self.machine.game.player.backfire_counter_count)
            self._assertIncrement("score", "s_pop1", (i+1) * 1000)

        # final hit with default multiplier awards 10k
        self._assertIncrement("score", "s_pop1", 10000)
