from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase

import tests.death_save as death_save

class DeathSaveGameTesting(FullMachineTestCase):

    def _assertIncrement(self, var, switch, value):
        death_save._assertIncrement(self, var, switch, value)

    def _assertMusicIs(self, state, track):
        death_save._assertMusicIs(self, state, track)

    def _assertAmbienceIs(self, state, track):
        death_save._assertAmbienceIs(self, state, track)

    def _assertVoiceIs(self, state, track):
        death_save._assertVoiceIs(self, state, track)

    def _assertSoundEffectIs(self, state, track):
        death_save._assertSoundEffectIs(self, state, track)

    def _start(self):
        death_save._start(self)

    def _expire_ball_save(self):
        death_save._expire_ball_save(self)

    def _start_and_expire_ball_save(self):
        death_save._start_and_expire_ball_save(self)

    def _start_green_flag(self):
        death_save._start_green_flag(self)

    def _start_backfire(self):
        death_save._start_backfire(self)

    def _start_grooveline(self):
        death_save._start_grooveline(self)

    def _start_luxury(self):
        death_save._start_luxury(self)

    def _start_grand_prix(self):
        death_save._start_grand_prix(self)

    def _complete_lap(self):
        death_save._complete_lap(self)

    def _drain_one_ball(self):
        death_save._drain_one_ball(self)
