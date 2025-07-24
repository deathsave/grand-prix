import os
from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase
import tests.death_save as death_save

class DeathSaveMcTesting(FullMachineTestCase):

    def _assertIncrement(self, var, switch, value):
        death_save._assertIncrement(self, var, switch, value)

    def _start(self):
        death_save._start(self)

    def _expire_ball_save(self):
        death_save._expire_ball_save(self)

    def _start_and_expire_ball_save(self):
        death_save._start_and_expire_ball_save(self)

    def _expire_ball_save(self):
        death_save._expire_ball_save(self)

    def _drain_one_ball(self):
        death_save._drain_one_ball(self)

    # Helper function to check for existence
    # of test on the display.
    #
    # Example:
    #
    #    self.assertIn('Some value',
    #        [x.text for x in self._get_display_text_widgets])
    #
    def _get_display_text_widgets(self):
        current_widgets = []
        for w in self.mc.displays['apron'].current_slide.widgets:
            if hasattr(w.widget, 'text'):
                current_widgets.append(w.widget)
        return current_widgets
