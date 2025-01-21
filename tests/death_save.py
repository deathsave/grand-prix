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
        self.machine.ball_devices["bd_trough"].balls)
    self.assertModeRunning('attract')
    self.assertModeNotRunning('pit')
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

def _start_and_expire_ball_save(self):
    self._start()
    self.hit_and_release_switch("s_activate_playfield")
    self.advance_time_and_run(15)

# assumes pit mode is running (game started)
def _start_green_flag(self):
    # Player must "fill up" to start racing
    self.assertEqual(
        1, self.machine.game.player.level_fuel)
    self.assertEqual(1, self.machine.playfield.balls)

    # Hitting the first qualifier fills up the tank
    self.hit_and_release_switch("s_fuel")
    self.advance_time_and_run(1)
    self.assertModeRunning("green_flag")

def _complete_lap(self):
    self.hit_and_release_switch("s_spinner")
    self.hit_and_release_switch("s_grooveline")
    self.advance_time_and_run(1)

# assumes green_flag mode is running
def _start_grooveline(self):
    self.machine.events. \
        post("grooveline_qualifier_hit")
    self.advance_time_and_run(1)
    self.advance_time_and_run(4)
    self.assertModeRunning("grooveline")

# assumes green_flag mode is running
def _start_grand_prix(self):
    self.machine.events. \
        post("logicblock_grand_prix_counter_complete")
    self.advance_time_and_run(1)
    self.advance_time_and_run(4)
    self.assertModeRunning("grand_prix")

# From https://github.com/missionpinball/mpf/blob \
#   /dev/mpf/tests/MpfGameTestCase.py#L141
def _drain_one_ball(self):
    drain = self.machine.ball_devices.items_tagged("drain")[0]
    self.machine.default_platform.add_ball_to_device(drain)
