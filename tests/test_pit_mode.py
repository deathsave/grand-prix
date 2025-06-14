from tests.death_save_game_testing import DeathSaveGameTesting

class TestPitMode(DeathSaveGameTesting):

    def test_sound(self):
        self._start()
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self._assertVoiceIs("playing", "fuel")
        self._assertAmbienceIs("playing", "comm_noise_on")
        self.advance_time_and_run(5)
        self._assertAmbienceIs("playing", "comm_noise_loop")

    def test_scoring(self):
        score = "score"

        self._start()
        self.hit_and_release_switch("s_shooter_lane")

        self.assertEqual(0, self.machine.game.player.score)
        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)

        # most switches only score 1 point
        self._assertIncrement(score, "s_pop1", 1)
        self._assertIncrement(score, "s_pop2", 1)
        self._assertIncrement(score, "s_grooveline", 1)
        self._assertIncrement(score, "s_backfire_hole", 1)
        self._assertIncrement(score, "s_prix_hole", 1)
        self._assertIncrement(score, "s_grand_hole", 1)
        self._assertIncrement(score, "s_spinner", 1)
        self._assertIncrement(score, "s_save_target", 1)
        self._assertIncrement(score, "s_bonus_target", 1)
        self._assertIncrement(score, "s_swerve1", 1)
        self._assertIncrement(score, "s_swerve2", 1)
        self._assertIncrement(score, "s_slingshot1", 1)
        self._assertIncrement(score, "s_slingshot2", 1)
        self._assertIncrement(score, "s_inlane1", 1)
        self._assertIncrement(score, "s_inlane2", 1)
        self._assertIncrement(score, "s_outlane1", 1)
        self._assertIncrement(score, "s_outlane2", 1)

        # Activates green_flag mode, so check last
        # to prevent scoring false positives
        self._assertIncrement(score, "s_pit_fuel", 100)
