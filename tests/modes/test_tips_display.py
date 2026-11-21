from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestTipsDisplay(DeathSaveMcTesting):

    def _slide(self):
        return self.mc.targets["default"].current_slide_name

    # Intro -> splash -> tip (with its mode background)
    def test_rotation_slides(self):
        self.advance_time_and_run(1)
        self.assertEqual("dspc_animation_slide", self._slide())

        self.advance_time_and_run(12)
        self.assertEqual("splash_slide", self._slide())

        self.advance_time_and_run(15)
        self.assertEqual("tip_green_flag_slide", self._slide())

        self.advance_time_and_run(15)
        self.assertEqual("splash_slide", self._slide())

    # A flipper jumps straight to the tip slide
    def test_flipper_shows_tip_slide(self):
        self.advance_time_and_run(14)
        self.assertEqual("splash_slide", self._slide())
        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(1)
        self.assertEqual("tip_green_flag_slide", self._slide())
