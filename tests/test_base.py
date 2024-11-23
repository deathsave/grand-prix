"""Tests the Base Mode"""

from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase

class TestBase(FullMachineTestCase):

    """Tests start-up sequence"""

    def test_startup(self):
        self.assertModeRunning('attract')
