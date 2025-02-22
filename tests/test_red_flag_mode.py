from tests.death_save_game_testing import DeathSaveGameTesting

class TestRedFlagMode(DeathSaveGameTesting):

    def test_qualification(self):
        self._start()
        self.advance_time_and_run(17) # expire main ball save
        self._start_green_flag()
        self.assertModeRunning("green_flag")
        self.assertModeNotRunning("red_flag")

        # Grooveline -> 1/3
        self._start_grooveline() # no ball save here
        self.assertModeRunning("grooveline")
        self._drain_one_ball()
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.is_grooveline_completed)
        self.assertModeNotRunning("grooveline")
        self.assertModeNotRunning("red_flag")
        self.assertModeRunning("green_flag")
        self.assertEqual(1, self.machine. \
            counters["red_flag_counter"].value)
        self.assertEqual(False, self.machine. \
            counters["red_flag_counter"].check_complete())

        # Luxury -> 2/3
        self._start_luxury()
        self.assertModeRunning("luxury")
        self.advance_time_and_run(10) # expire mode ball save
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertModeNotRunning("luxury")
        self.assertEqual(
            1, self.machine.game.player.is_luxury_completed)
        self.assertModeNotRunning("red_flag")
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine. \
            counters["red_flag_counter"].value)
        self.assertEqual(False, self.machine. \
            counters["red_flag_counter"].check_complete())

        # Grand Prix -> 3/3
        self._start_grand_prix()
        self.assertModeRunning("grand_prix")
        self.advance_time_and_run(20) # expire mode ball save
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(1)
        #self.assertEqual(1, self.machine.playfield.balls)
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(
            1, self.machine.game.player.is_grand_prix_completed)
        self.assertModeNotRunning("red_flag")
        self.assertModeRunning("green_flag")
        self.assertEqual(3, self.machine. \
            counters["red_flag_counter"].value)
        self.assertEqual(True, self.machine. \
            counters["red_flag_counter"].check_complete())

        # TODO: final sequence for mode start here
