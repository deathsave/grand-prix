import random
from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestRedLineMode(DeathSaveGameTesting):

    def test_qualification(self):
        self._start()
        self._expire_ball_save()
        self._start_green_flag()
        self.assertModeRunning("green_flag")
        self.assertModeNotRunning("red_line")

        # Grooveline -> 1/3 (2 ball multiball)
        self._sim_grooveline()
        self.assertModeRunning("grooveline")
        self.advance_time_and_run(10) # expire mode ball save
        self._drain_one_ball()
        self.advance_time_and_run(1)

        self.assertEqual(
            1, self.machine.game.player.is_grooveline_completed)
        self.assertModeNotRunning("grooveline")
        self.assertModeNotRunning("red_line")
        self.assertModeRunning("green_flag")

        # Luxury -> 2/3 (2 ball multiball)
        self._start_luxury()
        self.assertModeRunning("luxury")
        self.advance_time_and_run(10) # expire mode ball save
        self._drain_one_ball()
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertModeNotRunning("luxury")
        self.assertEqual(
            1, self.machine.game.player.is_luxury_completed)
        self.assertModeNotRunning("red_line")
        self.assertModeRunning("green_flag")

        # Grand Prix -> 3/3 (3 ball multiball)
        self._sim_grand_prix()
        self.assertModeRunning("grand_prix")
        self.advance_time_and_run(20) # expire mode ball save
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(1)
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(
            1, self.machine.game.player.is_grand_prix_completed)
        self.assertModeNotRunning("red_line")
        self.assertModeRunning("green_flag")

        # With all 3 qualifying modes completed,
        # the red line mode is started by entering
        # ANY ONE OF THE HOLES on the playfield, so
        # we select a random one here
        holes = ["s_hole_grand", "s_hole_prix", "s_hole_backfire"]
        self.assertModeNotRunning("red_line")
        self.hit_and_release_switch(random.choice(holes))

        # The red line mode is started
        self.advance_time_and_run(1)
        self.assertModeRunning("red_line")
        self.assertEqual(True,
            self.machine.multiballs["red_line"].enabled)

    def _red_line_ready(self):
        player = self.machine.game.player
        player.is_grooveline_completed = 1
        player.is_luxury_completed = 1
        player.is_grand_prix_completed = 1

    # the lamp changes over a couple of seconds if it's blinking
    def _lamp_blinks(self, light):
        seen = set()
        for i in range(20):
            self.advance_time_and_run(0.1)
            seen.add(self.machine.lights[light].get_color().rgb)
        return len(seen) > 1

    def test_ready_lamp(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.advance_time_and_run(2)
        self.assertFalse(self._lamp_blinks("l_multiball"))
        self._red_line_ready()
        self.advance_time_and_run(2)
        self.assertTrue(self._lamp_blinks("l_multiball"))

    # Leaving Red Line resets Grooveline and Grand Prix (for another
    # go at the wizard), but Luxury stays completed (its chain is the
    # end of ball bonus)
    def test_leaving_resets_grooveline_and_grand_prix(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._red_line_ready()
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertModeRunning("red_line")
        self.advance_time_and_run(60) # expire mode ball save
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(1)
        self.assertModeNotRunning("red_line")

        player = self.machine.game.player
        self.assertEqual(0, player.is_grooveline_completed)
        self.assertEqual(0, player.is_grand_prix_completed)
        self.assertEqual(1, player.is_luxury_completed)
        self.assertEqual(1, player.is_red_line_completed)

        # a hole doesn't restart it
        self.hit_switch_and_run("s_hole_prix", 3)
        self.assertModeNotRunning("red_line")

        # Grooveline + Grand Prix get back to it
        player.is_grooveline_completed = 1
        player.is_grand_prix_completed = 1
        self.hit_switch_and_run("s_hole_prix", 3)
        self.assertModeRunning("red_line")

