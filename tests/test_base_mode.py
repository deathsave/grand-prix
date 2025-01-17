from tests.death_save_game_testing import DeathSaveGameTesting

class TestBaseMode(DeathSaveGameTesting):

    def test_scoring(self):
        score = "score"

        self._start()
        self.assertEqual(0, self.machine.game.player.score)
        self._assertIncrement(score, "s_pop1", 10)
        self._assertIncrement(score, "s_pop2", 10)
        self._assertIncrement(score, "s_grooveline", 50)

        self._assertIncrement(score, "s_oil", 100)
        self._assertIncrement(score, "s_tires", 100)
        self._assertIncrement(score, "s_podium_hole", 500)
        self._assertIncrement(score, "s_prix_hole", 100)
        self._assertIncrement(score, "s_grand_hole", 100)
        self._assertIncrement(score, "s_spinner", 10)
        self._assertIncrement(score, "s_grand_advance", 10)
        self._assertIncrement(score, "s_prix_advance", 10)
        self._assertIncrement(score, "s_podium_advance1", 10)
        self._assertIncrement(score, "s_podium_advance2", 10)
        self._assertIncrement(score, "s_slingshot1", 10)
        self._assertIncrement(score, "s_slingshot2", 10)
        self._assertIncrement(score, "s_inlane1", 25)
        self._assertIncrement(score, "s_inlane2", 25)
        self._assertIncrement(score, "s_outlane1", 50)
        self._assertIncrement(score, "s_outlane2", 50)
        # Activates green_flag mode, so check last
        # to prevent scoring false positives
        self._assertIncrement(score, "s_fuel", 100)
