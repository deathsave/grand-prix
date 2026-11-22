from unittest.mock import patch
from mpfmc.config_players.sound_player import McSoundPlayer
from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestRedLineSound(DeathSaveMcTesting):

    # Red Line is just the breathing and the crowd (both
    # reverbed, see misc/reverb.yaml) with no music, which
    # comes back after, along with Green Flag's dry crowd
    def test_breathing_and_crowd_no_music(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        music = self.mc.sound_system.audio_interface. \
            get_track_by_name("music")
        player = self.machine.game.player
        player.is_grooveline_completed = 1
        player.is_luxury_completed = 1
        player.is_grand_prix_completed = 1

        requested = []
        play = McSoundPlayer.play
        def spy(sound_player, settings, *args, **kwargs):
            requested.append(dict(settings))
            return play(sound_player, settings, *args, **kwargs)

        with patch.object(McSoundPlayer, "play", spy):
            self.hit_switch_and_run("s_hole_backfire", 2)
            self.assertModeRunning("red_line")
            self.assertAlmostEqual(0, music.volume, places=2)
            started = self._actions(requested)
            self.assertEqual("play", started.get("red_line_breathing"))
            self.assertEqual("play", started.get("red_line_heartbeat"))
            self.assertEqual("play", started.get("red_line_at_the_track"))
            self.assertEqual("stop", started.get("at_the_track"))

            requested.clear()
            self.machine.modes["red_line"].stop()
            self.advance_time_and_run(2)
            self.assertModeNotRunning("red_line")
            stopped = self._actions(requested)
            self.assertEqual("stop", stopped.get("red_line_breathing"))
            self.assertEqual("stop", stopped.get("red_line_heartbeat"))
            self.assertEqual("stop", stopped.get("red_line_at_the_track"))
            self.assertEqual("play", stopped.get("at_the_track"))
        self.assertAlmostEqual(
            self.mc.machine_config["sound_system"]["tracks"]["music"][
                "volume"], music.volume, places=2)

    # the last action asked of each sound
    def _actions(self, requested):
        actions = {}
        for settings in requested:
            for sound, s in settings.items():
                actions[str(sound)] = s.get("action", "play") \
                    if isinstance(s, dict) else "play"
        return actions

    # the reverbed sounds exist (made by bin/reverb)
    def test_reverbed_sounds_exist(self):
        for name in ["red_line_breathing", "red_line_heartbeat",
                "red_line_at_the_track"]:
            self.assertIn(name, self.mc.sounds)
