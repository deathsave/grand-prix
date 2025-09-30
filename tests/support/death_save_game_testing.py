from mpf.tests.MpfMachineTestCase import MpfMachineTestCase

import tests.support.death_save as death_save

# Extends MpfMachineTestCase with common helpers.
# We should use this as the base class for most tests.
class DeathSaveGameTesting(MpfMachineTestCase):
    def _assertIncrement(self, var, switch, value):
        death_save._assertIncrement(self, var, switch, value)

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
