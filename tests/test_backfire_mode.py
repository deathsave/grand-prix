from tests.death_save_game_testing import DeathSaveGameTesting

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
        self.machine.events.post("pit_required_oil")
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
        self.hit_and_release_switch("s_backfire_hole")
        self.advance_time_and_run(1)

        self.assertModeRunning("backfire")
        # main timer should be running now
        self.assertEqual(True,
            self.machine.timers["backfire"].running)

        # ball is kicked out after 5 seconds
        self.advance_time_and_run(5)

        # timer expires after 30 more seconds and mode ends
        self.advance_time_and_run(30)
        self.assertEqual(False,
            self.machine.timers["backfire"].running)
        self.assertModeNotRunning("backfire")

    # To complete:
    #
    # - Each consecutive pop bumper hit increases
    #   linearly increasing the current bumpers
    #   value by 10% up to a maximum TBD
    # - If max is reached in time, immediately return player
    #   to green flag (fuel, oil and tires are max)
    #
    def test_scoring(self):
        pass
