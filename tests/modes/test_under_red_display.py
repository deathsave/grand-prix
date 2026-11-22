from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestUnderRedDisplay(DeathSaveMcTesting):

    # Under Red shows its red flag slide (like the other modes')
    def test_under_red_slide(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        self.post_event("green_flag_under_red")
        self.advance_time_and_run(1)
        self.assertEqual("under_red_slide",
            self.mc.targets["default"].current_slide.name)
        texts = []
        def walk(widget):
            if type(widget).__name__ == "Text":
                texts.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        self.assertIn("Red Flag", texts)
        images = []
        def walk_images(widget):
            if type(widget).__name__ == "ImageWidget":
                images.append(widget.config["image"])
            for child in getattr(widget, "children", []):
                walk_images(child)
        walk_images(self.mc.targets["default"])
        self.assertIn("red-flag", images)
