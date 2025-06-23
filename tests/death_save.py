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
    self.advance_time_and_run(4)
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
    self._expire_ball_save()

def _expire_ball_save(self):
    active_time = 10
    hurry_up_time = 5
    grace_period = 2
    full_delay = active_time + hurry_up_time + grace_period

    # ensure the playfield is active
    self.hit_and_release_switch("s_activate_playfield")
    self.advance_time_and_run(full_delay)
    print("-----------------------------------------")
    print("Ball save simulation ended")
    print("-----------------------------------------")

# assumes pit mode is running (game started)
def _start_green_flag(self):
    # Player must "fill up" to start racing
    self.assertEqual(
        1, self.machine.game.player.level_fuel)
    self.assertEqual(1, self.machine.playfield.balls)

    # Hitting the first qualifier fills up the tank
    self.hit_and_release_switch("s_pit_fuel")
    self.advance_time_and_run(1)
    self.assertModeRunning("green_flag")
    # call out AFTER the signal countdown
    self.advance_time_and_run(6)
    self._assertSoundEffectIs("playing", "real_pit")
    self.advance_time_and_run(1)
    self._assertVoiceIs("playing", "pit_done")

def _start_backfire(self):
    self._start_green_flag()
    # player returns to the pit
    self.machine.events.post("pit_required_lube")
    self.advance_time_and_run(1)

    # player hits the spinner
    self.hit_and_release_switch("s_spinner")
    self.advance_time_and_run(1)

    # then enters the top hole
    self.hit_switch_and_run("s_backfire_hole", 1)
    self.assertModeRunning("backfire")

    # ball kicked out
    self.advance_time_and_run(5)
    self.assertEqual(True,
        self.machine.counters["backfire_counter"].enabled)

def _complete_lap(self):
    self.hit_and_release_switch("s_spinner")
    self.hit_and_release_switch("s_grooveline")
    self.advance_time_and_run(1)

# assumes green_flag mode is running
def _start_grooveline(self):
    self.machine.events. \
        post("grooveline_qualifier_hit")
    self.advance_time_and_run(4)
    self.assertModeRunning("grooveline")

# assumes green_flag mode is running
def _start_luxury(self):
    self.machine.events. \
        post("logicblock_luxury_counter_complete")
    self.hit_and_release_switch("s_multiball_target")
    self.advance_time_and_run(8)
    self.assertModeRunning("luxury")

# assumes green_flag mode is running
def _start_grand_prix(self):
    self.machine.events.post("grand_prix_qualifier_hit")
    self.advance_time_and_run(4)
    self.assertModeRunning("grand_prix")

def _assertSound(self, track, state, sound_name):
    track = self.mc.sound_system.audio_interface. \
        get_track_by_name(track)
    for sound in track.get_status():
        if self.mc.sounds[sound_name].id == sound['sound_id']:
            found_sound = sound
            break
    if "found_sound" not in locals():
        self.fail(sound_name + " not found in track.")
    self.assertEqual(state, found_sound['status'])

def _assertMusicIs(self, state, sound_name):
    _assertSound(self, "music", state, sound_name)

def _assertVoiceIs(self, state, sound_name):
    _assertSound(self, "voice", state, sound_name)

def _assertAmbienceIs(self, state, sound_name):
    _assertSound(self, "ambience", state, sound_name)

def _assertSoundEffectIs(self, state, sound_name):
    _assertSound(self, "effects", state, sound_name)

# From https://github.com/missionpinball/mpf/blob \
#   /dev/mpf/tests/MpfGameTestCase.py#L141
def _drain_one_ball(self):
    drain = self.machine.ball_devices.items_tagged("drain")[0]
    self.machine.default_platform.add_ball_to_device(drain)
