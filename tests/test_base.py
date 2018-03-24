"""Tests the Base Mode"""

from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class TestBase(MpfMachineTestCase):

    """Tests start-up sequence"""

    def test_startup(self):
        self.assertModeRunning('attract')