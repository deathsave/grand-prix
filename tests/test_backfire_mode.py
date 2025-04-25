from tests.death_save_game_testing import DeathSaveGameTesting

class TestBackfireMode(DeathSaveGameTesting):

    # To qualify:
    #
    # - Top saucer is lit for 15 seconds when
    #   leaving green flag mode (pit stop)
    # - During that time, first hit the spinner
    # - Then enter the top saucer to start the mode
    #
    def test_qualification(self):
        self._start()
        self._start_green_flag()
        self.assertModeRunning("green_flag")
        self.assertEqual(1, self.machine.game.player.pit_count)

        # player returns to the pit
        self.machine.events.post("pit_required_oil")
        self.advance_time_and_run(1)
        self.assertEqual(2, self.machine.game.player.pit_count)
        self.assertModeNotRunning("green_flag")
        self.assertModeNotRunning("backfire")
        self.assertEqual(True,
            self.machine.timers["backfire_timer"].running)

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
