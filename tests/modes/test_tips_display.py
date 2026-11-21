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

        self.advance_time_and_run(10)
        self.assertEqual("tip_backfire_slide", self._slide())

        # through the other 6 tips and back to the splash
        self.advance_time_and_run(70)
        self.assertEqual("splash_slide", self._slide())

    # The left flipper steps back from the splash
    # to the last tip
    def test_left_flipper_rewinds_slide(self):
        self.advance_time_and_run(14)
        self.assertEqual("splash_slide", self._slide())
        self.hit_and_release_switch("s_flipper2")
        self.advance_time_and_run(1)
        self.assertEqual("tip_pure_evil_slide", self._slide())

    # The right flipper advances to the first tip slide
    def test_flipper_shows_tip_slide(self):
        self.advance_time_and_run(14)
        self.assertEqual("splash_slide", self._slide())
        self.hit_and_release_switch("s_flipper1")
        self.advance_time_and_run(1)
        self.assertEqual("tip_green_flag_slide", self._slide())

    # Each tip uses its mode's look when it has one
    def test_tip_slides_by_mode(self):
        expected = [
            "tip_green_flag_slide",
            "tip_backfire_slide",
            "tip_grooveline_slide",
            "tip_luxury_slide",
            "tip_grand_prix_slide",
            "tip_extra_ball_slide",
            "tip_red_line_slide",
            "tip_pure_evil_slide",
        ]
        self.advance_time_and_run(1)
        for slide in expected:
            self.hit_and_release_switch("s_flipper1")
            self.advance_time_and_run(1)
            self.assertEqual(slide, self._slide())
