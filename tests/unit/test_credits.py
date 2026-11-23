from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestCredits(DeathSaveGameTesting):

    def _credits(self):
        return self.machine.variables.get_machine_var("credits_whole_num")

    def _coin(self, quarters=1):
        for i in range(quarters):
            self.hit_and_release_switch("s_credit")
            self.advance_time_and_run(0.2)

    def _credit_play(self):
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        # (start is blocked for 5s after a toggle)
        self.advance_time_and_run(5.5)
        self.assertFalse(
            self.machine.settings.get_setting_value("free_play"))

    # Free play by default (games start without coins)
    def test_free_play_by_default(self):
        self.advance_time_and_run(10)
        self.assertTrue(self.machine.settings.get_setting_value("free_play"))
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNotNone(self.machine.game)

    # 50 cents a game: a quarter isn't enough, two is a game
    def test_fifty_cents_a_game(self):
        self._credit_play()
        self.mock_event("not_enough_credits")
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNone(self.machine.game)
        self.assertEventCalled("not_enough_credits")

        self._coin()
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNone(self.machine.game)

        self._coin()
        self.assertEqual(1, self._credits())
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNotNone(self.machine.game)
        self.assertEqual(0, self._credits())

    # 3 for a dollar
    def test_three_for_a_dollar(self):
        self._credit_play()
        self._coin(4)
        self.assertEqual(3, self._credits())

    # start + the left flipper, held 2s, toggles free play
    def test_combo_toggles_free_play(self):
        self.advance_time_and_run(10)
        self.hit_switch_and_run("s_flipper1", 0.1)
        self.hit_switch_and_run("s_start", 2.5)
        self.release_switch_and_run("s_start", 0.1)
        self.release_switch_and_run("s_flipper1", 1)
        self.assertFalse(
            self.machine.settings.get_setting_value("free_play"))
        self.hit_switch_and_run("s_flipper1", 0.1)
        self.hit_switch_and_run("s_start", 2.5)
        self.release_switch_and_run("s_start", 0.1)
        self.release_switch_and_run("s_flipper1", 1)
        self.assertTrue(
            self.machine.settings.get_setting_value("free_play"))

    # A match is a free credit for each player who matched, in credit play
    def test_match_awards_a_credit(self):
        self._credit_play()
        self._coin(2)
        self.assertEqual(1, self._credits())
        self.post_event_with_params("match_has_match", winners=1,
            winner_number=30)
        self.advance_time_and_run(1)
        self.assertEqual(2, self._credits())
        self.post_event_with_params("match_has_match", winners=2,
            winner_number=30)
        self.advance_time_and_run(1)
        self.assertEqual(4, self._credits())

    # but not in free play
    def test_no_match_credit_in_free_play(self):
        self.advance_time_and_run(10)
        self.post_event_with_params("match_has_match", winners=1,
            winner_number=30)
        self.advance_time_and_run(1)
        self.assertTrue(self.machine.settings.get_setting_value("free_play"))
        self.assertEqual(0, self.machine.variables.get_machine_var(
            "credit_units") or 0)

    def _combo(self):
        self.hit_switch_and_run("s_flipper1", 0.1)
        self.hit_switch_and_run("s_start", 2.5)
        self.release_switch_and_run("s_start", 0.1)
        self.release_switch_and_run("s_flipper1", 0.5)

    # Letting go of start after the combo doesn't start a game, nor does
    # pressing it again within 5s; after that it does
    def test_combo_doesnt_start_a_game(self):
        self.advance_time_and_run(10)
        self._combo()
        self.assertFalse(
            self.machine.settings.get_setting_value("free_play"))
        self.assertIsNone(self.machine.game)
        # back to free play, and start straight away
        self._combo()
        self.assertTrue(self.machine.settings.get_setting_value("free_play"))
        self.assertIsNone(self.machine.game)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNone(self.machine.game)
        self.advance_time_and_run(4)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertIsNotNone(self.machine.game)
