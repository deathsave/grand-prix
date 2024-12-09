#from objprint import op

##################
# Helper Methods #
##################

# For given :var, activate given :switch and check
# whether value has increased by given :value
#
# @param var: variable to check (score, bonus, etc.)
# @param switch: switch to activate (s_spinner, s_pop1, etc.)
# @param value: amount we expect the :var to increase by
#
# Example: self.assertIncrement("score", "s_spinner", 10)
#
def _assertIncrement(self, var, switch, value):
    current_val = getattr(self.machine.game.player, var)
    value, getattr(self.machine.game.player, var)
    self.hit_and_release_switch(switch)
    self.advance_time_and_run(1)
    new_val = getattr(self.machine.game.player, var)
    self.assertEqual(
        value, new_val - current_val,
        "Expected %s, got %s" % (value, new_val - current_val)
    )

def _start(self):
    self.assertEqual(3,
        self.machine.ball_devices.bd_trough.balls)
    self.assertModeRunning('attract')
    self.assertModeNotRunning('base')
    self.hit_and_release_switch("s_start")
    self.advance_time_and_run(1)
    self.assertEqual(2,
        self.machine.ball_devices["bd_trough"].balls)
    self.assertEqual(1,
        self.machine.ball_devices["bd_shooter_lane"].balls)
    self.assertEqual(0, self.machine.playfield.balls)
    self.hit_and_release_switch("s_shooter_lane")
    self.advance_time_and_run(4)
    self.assertEqual(1, self.machine.playfield.balls)
