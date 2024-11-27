"""Tests General/Base Functionality"""

import os
from mpf.tests.MpfTestCase import MagicMock
from mpf.tests.MpfFakeGameTestCase import MpfFakeGameTestCase
from mpf.tests.MpfGameTestCase import MpfGameTestCase
from mpf.tests.MpfMachineTestCase import MpfMachineTestCase
from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase


class TestGeneral(MpfMachineTestCase):

    """Tests start-up sequence"""

    def get_config_file(self):
        return 'development.yaml'

    def get_machine_path(self):
        return os.path.abspath(os.path.join(
            os.path.realpath(__file__),
            os.pardir,os.pardir
        ))

    def test_start(self):
        self.assertModeRunning('attract')
