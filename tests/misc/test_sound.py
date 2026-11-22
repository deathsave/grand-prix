from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestSound(DeathSaveMcTesting):

    def test_attract_sound(self):
        self._assertMusicIs("playing", "the_distance")

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
