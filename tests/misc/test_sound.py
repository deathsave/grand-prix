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
        self._assertVoiceIs("playing", "fuel")

    def test_green_flag_sound(self):
        self._start()
        # start green flag
        self.hit_and_release_switch("s_pit_fuel")
        # call out AFTER the signal countdown
        self.advance_time_and_run(7)
        self._assertSoundEffectIs("playing", "real_pit")
