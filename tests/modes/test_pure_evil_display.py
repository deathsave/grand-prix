from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestPureEvilDisplay(DeathSaveMcTesting):

    # the track's volume in config/common/sound_system.yaml
    def _volume(self, track):
        return self.mc.machine_config["sound_system"]["tracks"][track][
            "volume"]

    def _slide(self):
        return self.mc.targets["default"].current_slide

    # The Pure Evil slide pulsates once a second
    def test_slide_pulsates(self):
        self.machine.variables.set_machine_var("is_pure_evil_available", 1)
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("pure_evil_enters")
        self.advance_time_and_run(1)
        self.assertEqual("pure_evil_slide", self._slide().name)

        image = self._slide().widgets[0].widget
        samples = []
        for i in range(40):  # 2s, every 50ms
            self.advance_time_and_run(0.05)
            samples.append(image.opacity)
        # dips toward 0.35 and comes back to full
        self.assertLess(min(samples), 0.45)
        self.assertGreater(max(samples), 0.95)
        # twice in 2 seconds: count the dips
        dips = sum(1 for a, b, c in zip(samples, samples[1:], samples[2:])
            if b < a and b <= c and b < 0.5)
        self.assertEqual(2, dips)

    # A taunt plays on the voice track 5 seconds in
    def test_taunt_plays(self):
        self.machine.variables.set_machine_var("is_pure_evil_available", 1)
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("pure_evil_enters")
        track = self.mc.sound_system.audio_interface. \
            get_track_by_name("voice")
        # (the track reports the pool's id)
        taunt = self.mc.sounds["pure_evil_taunt"].id
        self.advance_time_and_run(4)
        heard = False
        for i in range(20):  # 4 to 9 seconds in
            self.advance_time_and_run(0.25)
            heard = heard or any(s["sound_id"] == taunt
                and s["status"] == "playing" for s in track.get_status())
        self.assertTrue(heard, "no taunt played")

    # Only the sirens: the music and ambience are silenced
    # during the mode and come back after
    def test_silences_background(self):
        self.machine.variables.set_machine_var("is_pure_evil_available", 1)
        self._start_and_expire_ball_save()
        self._start_green_flag()
        music = self.mc.sound_system.audio_interface. \
            get_track_by_name("music")
        ambience = self.mc.sound_system.audio_interface. \
            get_track_by_name("ambience")
        self.assertAlmostEqual(self._volume("music"), music.volume, places=2)
        self.post_event("pure_evil_enters")
        self.advance_time_and_run(2)
        self.assertModeRunning("pure_evil")
        self.assertAlmostEqual(0, music.volume, places=2)
        self.assertAlmostEqual(0, ambience.volume, places=2)
        self._assertSoundEffectIs("playing", "civil_siren")

        self.post_event("pure_evil_exits")
        self.advance_time_and_run(2)
        self.assertModeNotRunning("pure_evil")
        self.assertAlmostEqual(self._volume("music"), music.volume, places=2)
        self.assertAlmostEqual(self._volume("ambience"), ambience.volume, places=2)
