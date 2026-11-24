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
        player.is_grooveline_played = 1
        player.is_luxury_played = 1
        player.is_grand_prix_played = 1

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

    # Revving, every switch is just a rev (the other switch sounds
    # are silenced). At the red line, the drums loop and switches are
    # just the bell, until the shift: the max rev, a backfire and the
    # jackpot
    def test_rev_bell_and_shift_sounds(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        player = self.machine.game.player
        player.is_grooveline_played = 1
        player.is_luxury_played = 1
        player.is_grand_prix_played = 1
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertModeRunning("red_line")

        # what actually reaches the tracks (after any blocking)
        played = []
        system = self.mc.sound_system
        interface = system.audio_interface
        class Track:
            def __init__(self, track):
                self.track = track
            def play_sound(self, sound, context, settings):
                played.append(sound.name)
                return self.track.play_sound(sound, context, settings)
            def stop_sound(self, sound, *args):
                played.append(sound.name)
                return self.track.stop_sound(sound, *args)
            def __getattr__(self, name):
                return getattr(self.track, name)
        class Interface:
            def get_track_by_name(self, name):
                track = interface.get_track_by_name(name)
                return track and Track(track)
            def __getattr__(self, name):
                return getattr(interface, name)
        def sounds():
            names = list(played)
            played.clear()
            return names

        with patch.object(system, "audio_interface", Interface()):
            self.hit_and_release_switch("s_slingshot1")
            self.advance_time_and_run(0.2)
            heard = sounds()
            self.assertIn("rev", heard)
            self.assertNotIn("boing", heard)

            for _ in range(9):
                self.hit_and_release_switch("s_spinner")
                self.advance_time_and_run(0.1)
            self.assertIn("red_line_drums", sounds())

            self.hit_and_release_switch("s_slingshot1")
            self.advance_time_and_run(0.2)
            heard = sounds()
            self.assertIn("bell", heard)
            self.assertNotIn("rev", heard)
            self.assertNotIn("boing", heard)

            self.hit_switch_and_run("s_hole_backfire", 1)
            heard = sounds()
            self.assertIn("backfire", heard)
            self.assertIn("jackpot", heard)
            self.assertIn("max_rev_end", heard)
            self.assertIn("red_line_drums", heard)  # (stopped)

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
                "red_line_at_the_track", "red_line_drums", "max_rev_end"]:
            self.assertIn(name, self.mc.sounds)
