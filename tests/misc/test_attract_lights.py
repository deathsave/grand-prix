from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestAttractLights(DeathSaveGameTesting):

    def _states(self, names):
        return tuple(self.machine.lights[n].get_color().rgb for n in names)

    # The generated show (bin/attract-lights) runs in attract,
    # lighting both the RGB LEDs and the lamps, and loops
    def test_show_plays_and_loops(self):
        self.assertModeRunning("attract")
        rgb = ["l_loop01", "l_grooveline05", "l_pit_lube"]
        lamps = ["l_bonus05", "l_grand3", "l_signal2"]
        seen_rgb, seen_lamps = set(), set()
        for i in range(90):  # just over a loop (42.5s)
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
        lights = ["l_loop01", "l_loop09", "l_loop18", "l_bonus05"]
        before = self._states(lights)
        self.advance_time_and_run(3)
        self.assertEqual(before, self._states(lights))

    # Game over, tilt and shoot again aren't part of the show
    def test_leaves_info_lights_alone(self):
        steps = self.machine.shows["attract"].get_show_steps()
        names = { getattr(light, "name", light) for step in steps
            for light in step.get("lights", {}) }
        self.assertIn("l_backbox_ball1", names)
        for light in ["l_backbox_game_over", "l_backbox_tilt",
                "l_backbox_shoot_again", "l_shoot_again"]:
            self.assertNotIn(light, names)
