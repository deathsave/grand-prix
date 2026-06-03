from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestWearAndTear(DeathSaveGameTesting):

    def test_random_events(self):
        if self._is_unavailable("wear_and_tear"):
            print("Wear and Tear is not enabled")
            return None
        else:
            random_events = [
                "green_flag_smooth_sailing",
                "green_flag_degrade_fuel",
                "green_flag_degrade_lube",
                "green_flag_degrade_tires",
                "green_flag_degrade_all",
                "green_flag_under_red",
                "green_flag_bad_luck",
            ]
            random_events_fired = []

            # No random event should have occurred, yet
            for event in random_events:
                self.mock_event(event)
                self.assertEqual(0, self._events.get(event, 0))

            self._start()
            self._start_green_flag()

            for i in range(2):
                self._complete_lap()
            self.assertEqual(
                2, self.machine.game.player.lap_counter_count)

            # Still no random event, yet
            for event in random_events:
                self.mock_event(event)
                self.assertEqual(0, self._events.get(event, 0))

            # Recording 3 laps triggers a single random event
            self._complete_lap()
            for e in random_events:
                random_events_fired.append(self._events.get(e, 0))
            self.assertEqual(1, sum(random_events_fired))
            # NOTE: we're testing the event here, not the mode
            #       since the mode could end up stopped
