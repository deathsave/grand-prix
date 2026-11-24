from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestSound(DeathSaveMcTesting):

    def test_attract_sound(self):
        self._assertMusicIs("playing", "the_distance")

    def _effects_playing(self):
        track = self.mc.sound_system.audio_interface. \
            get_track_by_name("effects")
        ids = [ sound["sound_id"] for sound in track.get_status()
            if sound["status"] == "playing" ]
        return [ name for name in ["engine_start", "engine_idle",
            "engine_pace"]
            if self.mc.sounds[name].id in ids ]

    # The engine starts up as the ball reaches the shooter lane, then
    # idles there until the plunge
    def test_engine_start_and_idle(self):
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertEqual(["engine_start"], self._effects_playing())
        self.advance_time_and_run(3)
        self.assertIn("engine_idle", self._effects_playing())
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self.assertEqual(["engine_pace"], self._effects_playing())

    # Plunging during the start up stops it, and it doesn't idle after
    def test_plunge_during_engine_start(self):
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(4)
        self.assertEqual(["engine_pace"], self._effects_playing())

    # At pace around the pit, until Green Flag (and back to pace for a
    # pit stop), and it stops when the ball ends
    def test_engine_pace(self):
        self._start()
        self.assertEqual(["engine_pace"], self._effects_playing())
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(2)
        self.assertModeRunning("green_flag")
        # through Off the Line's countdown, until the flag drops
        self.assertEqual(["engine_pace"], self._effects_playing())
        # (the countdown waits for its 2s sync, so it's 3.5-5.5s in)
        self.advance_time_and_run(4)
        self.assertEqual([], self._effects_playing())
        self.machine.game.player.level_tires = 1
        self.machine.events.post("pit_required_tires")
        self.advance_time_and_run(2)
        self.assertModeNotRunning("green_flag")
        self.assertEqual(["engine_pace"], self._effects_playing())
        # and through Backfire
        self.hit_and_release_switch("s_spinner")
        self.hit_switch_and_run("s_hole_backfire", 1)
        self.assertModeRunning("backfire")
        self.assertEqual(["engine_pace"], self._effects_playing())
        self.advance_time_and_run(6)
        self.assertModeRunning("backfire")
        self.assertEqual(["engine_pace"], self._effects_playing())
        self._expire_ball_save()
        self._drain_one_ball()
        self.advance_time_and_run(2)
        self.assertNotIn("engine_pace", self._effects_playing())

    def test_pit_sound(self):
        self._start()
        # allow a bit more time for the "player up" sound
        # to play since voice is limited to 1 sound at a time
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self._assertAmbienceIs("playing", "comm_noise_on")
        self.advance_time_and_run(5)
        self._assertAmbienceIs("playing", "comm_noise_loop")

        # every 15 seconds while players score is trash,
        # they will be reminded to fuel up
        self.advance_time_and_run(9)

        # NOTE: this is a flakey one
        # self._assertVoiceIs("playing", "fuel")

    def test_green_flag_sound(self):
        self._start()
        # start green flag
        self.hit_and_release_switch("s_pit_fuel")
        # call out AFTER the signal countdown
        self.advance_time_and_run(7)
        self._assertSoundEffectIs("playing", "real_pit")

    # Bad luck ends the ball with a callout for which bad luck it was
    # (checks which sounds the sound player is asked to play, as the
    # audio itself plays in real time while the test clock jumps ahead)
    def test_bad_luck_callout(self):
        from unittest.mock import patch
        from mpfmc.config_players.sound_player import McSoundPlayer
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        requested = []
        play = McSoundPlayer.play

        def spy(player, settings, *args, **kwargs):
            requested.extend(settings)
            return play(player, settings, *args, **kwargs)

        picked = []
        for event in ["bad_luck_blow_out", "bad_luck_seized_up",
                "bad_luck_fuel_line"]:
            self.machine.events.add_handler(event,
                lambda event=event, **kwargs: picked.append(event))
        with patch.object(McSoundPlayer, "play", spy):
            self.machine.events.post("green_flag_bad_luck")
            self.advance_time_and_run(1)
        self.assertEqual(1, len(picked))
        # the picked bad luck's pool (e.g. bad_luck_seized_up)
        self.assertIn(picked[0], requested)

    def _requested(self, event, **params):
        from unittest.mock import patch
        from mpfmc.config_players.sound_player import McSoundPlayer
        requested = []
        play = McSoundPlayer.play

        def spy(player, settings, *args, **kwargs):
            requested.extend(settings)
            return play(player, settings, *args, **kwargs)

        with patch.object(McSoundPlayer, "play", spy):
            self.machine.events.post(event, **params)
            self.advance_time_and_run(1)
        return requested

    # Every ball save gets a "that was close" callout (a pool of 3)
    def test_ball_save_callouts(self):
        self._start()
        for event in ["ball_save_ball_start_saving_ball",
                "outlane_save_redeemed", "multiball_grooveline_shoot_again",
                "multiball_luxury_shoot_again",
                "multiball_grand_prix_shoot_again",
                "multiball_red_line_shoot_again"]:
            self.assertIn("ball_saves",
                [str(sound) for sound in self._requested(event)], event)
        for name in ["ball_saves1", "ball_saves2", "ball_saves3"]:
            self.assertIn(name, self.mc.sounds)

    # Low on lube (synth for now)
    def test_lube_callout(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        self.machine.game.player.level_lube = 1
        self.assertIn("lube", self._requested("pit_required_lube"))

    # Wear and Tear's nothing burger gets a callout
    def test_smooth_sailing_callout(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        self.assertModeRunning("green_flag")
        self.assertIn("smooth_sailing",
            self._requested("green_flag_smooth_sailing"))

    # Grand Prix's leader bonus, every lap
    def test_leader_bonus_callout(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        self.machine.events.post("grand_prix_multiball_ready")
        self.hit_switch_and_run("s_hole_backfire", 8)
        self.assertModeRunning("grand_prix")
        self.assertIn("leader_bonus",
            self._requested("grand_prix_leader_bonus", laps=1, value=20000))

    # Under Red: the wreck, then the red flag call out 3s into it
    def test_under_red_crash_then_callout(self):
        from unittest.mock import patch
        from mpfmc.config_players.sound_player import McSoundPlayer
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        played = []
        play = McSoundPlayer.play

        def spy(player, settings, *args, **kwargs):
            for name, s in settings.items():
                if not s.get("delay"):
                    played.append((name, round(self.machine.clock.get_time()
                        - start, 1)))
            return play(player, settings, *args, **kwargs)

        with patch.object(McSoundPlayer, "play", spy):
            start = self.machine.clock.get_time()
            self.machine.events.post("green_flag_under_red")
            self.advance_time_and_run(5)
        self.assertModeRunning("under_red")
        names = [ name for name, _ in played ]
        self.assertIn("crash", names)
        self.assertIn("red_flag", names)
        crash = dict(played)["crash"]
        self.assertAlmostEqual(3, dict(played)["red_flag"] - crash, delta=0.2)

    # No pit ambience under a red flag
    def test_under_red_no_pit_ambience(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(7)
        self.machine.events.post("green_flag_under_red")
        self.advance_time_and_run(3)
        self.assertModeRunning("under_red")
        track = self.mc.sound_system.audio_interface. \
            get_track_by_name("music")
        playing = [ sound["sound_id"] for sound in track.get_status()
            if sound["status"] == "playing" ]
        self.assertNotIn(self.mc.sounds["pit_ambience"].id, playing)

    def _music_playing(self, name):
        track = self.mc.sound_system.audio_interface. \
            get_track_by_name("music")
        return self.mc.sounds[name].id in [ s["sound_id"]
            for s in track.get_status() if s["status"] == "playing" ]

    # Green Flag's music comes in 6s after it starts
    def test_green_flag_music(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(4)
        self.assertFalse(self._music_playing("blinding_lights"))
        self.advance_time_and_run(3)
        self.assertTrue(self._music_playing("blinding_lights"))

    # but not if the ball ends first: it carried on into the next
    # player's ball (in the pit)
    def test_green_flag_music_not_after_the_ball_ends(self):
        self._start()
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertEqual(2, len(self.machine.game.player_list))
        self._expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        self.hit_switch_and_run("s_trough1", 1)
        self.advance_time_and_run(15)
        self.assertEqual(2, self.machine.game.player.number)
        self.assertModeNotRunning("green_flag")
        self.assertFalse(self._music_playing("blinding_lights"))

    # The right outlane whooshes while the ball save's on, and welps
    # once it's over
    def test_right_outlane_during_ball_save(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        self.assertTrue(self.machine.ball_saves["ball_start"].enabled)
        requested = self._requested("s_outlane2_active")
        self.assertIn("whoosh", requested)
        self.assertNotIn("welp", requested)
        self._expire_ball_save()
        self.assertFalse(self.machine.ball_saves["ball_start"].enabled)
        requested = self._requested("s_outlane2_active")
        self.assertIn("welp", requested)
        self.assertNotIn("whoosh", requested)

    # The left outlane works the same, and both whoosh while the outlane
    # save's lit
    def test_left_outlane_and_the_outlane_save(self):
        self._start()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        requested = self._requested("s_outlane1_active")
        self.assertIn("whoosh", requested)
        self._expire_ball_save()
        requested = self._requested("s_outlane1_active")
        self.assertIn("welp", requested)
        self.machine.game.player.is_outlane_save_lit = 1
        requested = self._requested("s_outlane1_active")
        self.assertIn("whoosh", requested)
        self.assertNotIn("welp", requested)
