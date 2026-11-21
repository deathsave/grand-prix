from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestAttractLights(DeathSaveGameTesting):

    def _states(self, names):
        return tuple(self.machine.lights[n].get_color().rgb for n in names)

    # The generated show (bin/attract-lights) runs in attract,
    # lighting both the RGB LEDs and the lamps, and loops
    def test_show_plays_and_loops(self):
        self.assertModeRunning("attract")
        rgb = ["l_loop_01", "l_grooveline_05", "l_pit_lube"]
        lamps = ["l_bonus_05", "l_grand_03", "l_signal2"]
        seen_rgb, seen_lamps = set(), set()
        for i in range(140):  # just over a loop (66.5s)
            self.advance_time_and_run(0.5)
            seen_rgb.add(self._states(rgb))
            seen_lamps.add(self._states(lamps))
        self.assertGreater(len(seen_rgb), 50)
        self.assertGreater(len(seen_lamps), 5)
        self.assertTrue(self.machine.shows["attract"])

    # Starting a game stops it (the lights go back to the game)
    def test_stops_for_a_game(self):
        self.advance_time_and_run(20)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertModeNotRunning("attract")
        lights = ["l_loop_01", "l_loop_09", "l_loop_18", "l_bonus_05"]
        before = self._states(lights)
        self.advance_time_and_run(3)
        self.assertEqual(before, self._states(lights))
