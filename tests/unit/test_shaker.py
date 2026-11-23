from unittest.mock import MagicMock
from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestShaker(DeathSaveGameTesting):

    def _watch(self):
        self.pulses = []
        def pulse(pulse_ms=None, *args, **kwargs):
            self.pulses.append(pulse_ms)
        self.machine.coils["c_shaker_motor"].pulse = MagicMock(
            side_effect=pulse)

    # A long rumble (3 full pulses) when a multiball starts
    def test_multiball_rumble(self):
        self._start()
        self._watch()
        self.post_event("multiball_started")
        self.advance_time_and_run(1)
        self.assertEqual(3, len(self.pulses))

    # and on the super jackpots, but not Luxury's shot group starting
    def test_super_jackpot_rumble(self):
        self._start()
        self._watch()
        self.post_event_with_params("luxury_complete", state="available")
        self.advance_time_and_run(1)
        self.assertEqual([], self.pulses)
        for event in ["grooveline_super_jackpot", "grand_prix_super_jackpot",
                "red_line_checkered_flag"]:
            self.post_event(event)
            self.advance_time_and_run(1)
        self.post_event_with_params("luxury_complete", state="claimed")
        self.advance_time_and_run(1)
        self.assertEqual(12, len(self.pulses))

    # A short kick on a jackpot, a skill shot or a replay
    def test_jackpot_kick(self):
        self._start()
        self._watch()
        for event in ["grooveline_jackpot", "luxury_jackpot",
                "grand_prix_jackpot", "red_line_shift", "off_the_line_hit",
                "skill_backfire_hit", "replay_awarded"]:
            self.post_event(event)
            self.advance_time_and_run(0.5)
        self.assertEqual([150] * 7, self.pulses)

    # Backfire Pops kick harder as they climb
    def test_backfire_pops(self):
        self._start()
        self._start_backfire()
        self._watch()
        for i in range(10):
            self.hit_and_release_switch("s_pop1")
            self.advance_time_and_run(0.3)
        self.assertEqual(80, self.pulses[0])
        self.assertIn(160, self.pulses)
        self.assertEqual(255, self.pulses[-2])
