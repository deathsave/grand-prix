import os
from mpf.tests.MpfMachineTestCase import MpfMachineTestCase
import tests.death_save as death_save

class DeathSaveGameTesting(MpfMachineTestCase):

    def _assertIncrement(self, var, switch, value):
        death_save._assertIncrement(self, var, switch, value)

    def _start(self):
        death_save._start(self)

    def _start_green_flag(self):
        death_save._start_green_flag(self)

    def _complete_lap(self):
        death_save._complete_lap(self)
