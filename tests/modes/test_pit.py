from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestPitMode(DeathSaveGameTesting):

    def test_loop_gate(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)

        self.assertEqual(
            True, self.machine.diverters["loop_gate"].enabled)
        self.hit_and_release_switch("s_shooter_lane")
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

    def test_scoring(self):
        score = "score"

        self._start()
        self.hit_and_release_switch("s_shooter_lane")

        self.assertEqual(0, self.machine.game.player.score)
        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)

        # most switches only score 1 point
        self._assertIncrement(score, "s_pop1", 10)
        self._assertIncrement(score, "s_pop2", 10)
        self._assertIncrement(score, "s_grooveline", 10)
        self._assertIncrement(score, "s_backfire_hole", 10)
        self._assertIncrement(score, "s_prix_hole", 10)
        self._assertIncrement(score, "s_grand_hole", 10)
        self._assertIncrement(score, "s_spinner", 10)
        self._assertIncrement(score, "s_save_target", 10)
        self._assertIncrement(score, "s_bonus_target", 10)
        self._assertIncrement(score, "s_swerve1", 10)
        self._assertIncrement(score, "s_swerve2", 10)
        self._assertIncrement(score, "s_slingshot1", 10)
        self._assertIncrement(score, "s_slingshot2", 10)
        self._assertIncrement(score, "s_inlane1", 10)
        self._assertIncrement(score, "s_inlane2", 10)
        self._assertIncrement(score, "s_outlane1", 10)
        self._assertIncrement(score, "s_outlane2", 10)

        # Activates green_flag mode, so check last
        # to prevent scoring false positives
        self._assertIncrement(score, "s_pit_fuel", 100)
