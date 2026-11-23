from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestReplayDisplay(DeathSaveMcTesting):

    def _texts(self):
        found = []
        def walk(widget):
            if type(widget).__name__ == "Text" and \
                    "replay" in (getattr(widget, "key", None) or ""):
                found.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    # The REPLAY! overlay (EXTRA BALL on free play) and the call out
    def test_fanfare(self):
        from unittest.mock import patch
        from mpfmc.config_players.sound_player import McSoundPlayer
        requested = []
        play = McSoundPlayer.play

        def spy(player, settings, *args, **kwargs):
            requested.extend(settings)
            return play(player, settings, *args, **kwargs)

        self._start()
        with patch.object(McSoundPlayer, "play", spy):
            self.machine.game.player.score += 1600000
            self.advance_time_and_run(0.5)
        self.assertEqual(["REPLAY!", "EXTRA BALL"], self._texts())
        self.assertIn("replay", requested)
        self.advance_time_and_run(3)
        self.assertEqual([], self._texts())
