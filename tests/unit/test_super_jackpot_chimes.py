from unittest.mock import MagicMock
from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestSuperJackpotChimes(DeathSaveGameTesting):

    # A super jackpot rolls the chimes 1-2-3 three times, then the
    # "Double jackpot!" callout plays (super_jackpot_chimes_done)
    def test_rolls_then_callout(self):
        self._start()
        order = []
        for coil in ["c_chime1", "c_chime2", "c_chime3"]:
            self.machine.coils[coil].pulse = MagicMock(
                side_effect=lambda *a, coil=coil, **k: order.append(coil))
        self.machine.events.add_handler("super_jackpot_chimes_done",
            lambda **kwargs: order.append("callout"))
        for event in ["grooveline_super_jackpot", "grand_prix_super_jackpot",
                "red_line_checkered_flag"]:
            order.clear()
            self.post_event(event)
            self.advance_time_and_run(1)
            # (the callout waits for the rolls)
            self.assertNotIn("callout", order)
            self.advance_time_and_run(1)
            self.assertEqual(
                ["c_chime1", "c_chime2", "c_chime3"] * 3 + ["callout"], order)
        order.clear()
        self.post_event_with_params("luxury_complete", state="available")
        self.advance_time_and_run(2)
        self.assertEqual([], order)
        self.post_event_with_params("luxury_complete", state="claimed")
        self.advance_time_and_run(2)
        self.assertEqual(10, len(order))
