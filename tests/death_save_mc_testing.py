import os
from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase
import tests.death_save as death_save

class DeathSaveMcTesting(FullMachineTestCase):

    def _assertIncrement(self, var, switch, value):
        death_save._assertIncrement(self, var, switch, value)

    def _start(self):
        death_save._start(self)
