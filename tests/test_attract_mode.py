from tests.death_save_game_testing import DeathSaveGameTesting

class TestAttractMode(DeathSaveGameTesting):

    def test_sound(self):
        self._assertMusicIs("playing", "the_distance")
