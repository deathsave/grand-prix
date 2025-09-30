import os
from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase
import tests.support.death_save as death_save

# Extends FullMachineTestCase with common helpers.
# Only use this when we need to test media controller
# elements as it's much slower.
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

    def _start_green_flag(self):
        death_save._start_green_flag(self)

    def _complete_lap(self):
        death_save._complete_lap(self)

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
        self._assertSound("music", state, sound_name)

    def _assertVoiceIs(self, state, sound_name):
        self._assertSound("voice", state, sound_name)

    def _assertAmbienceIs(self, state, sound_name):
        self._assertSound("ambience", state, sound_name)

    def _assertSoundEffectIs(self, state, sound_name):
        self._assertSound("effects", state, sound_name)

