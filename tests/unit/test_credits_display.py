from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestCreditsDisplay(DeathSaveMcTesting):

    def _texts(self, key="credits"):
        found = []
        def walk(widget):
            if type(widget).__name__ == "Text" and \
                    key in (getattr(widget, "key", None) or ""):
                found.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    def _slide(self):
        return self.mc.targets["default"].current_slide.name

    def _coin(self):
        self.hit_and_release_switch("s_credit")
        self.advance_time_and_run(0.2)

    # Toggling says which it is, and start without coins asks for them
    def test_messages(self):
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(0.5)
        self.assertIn("CREDIT PLAY", self._texts())
        # (start is blocked for 5s after a toggle)
        self.advance_time_and_run(5)

        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(0.5)
        self.assertIn("INSERT COINS", self._texts())
        self.advance_time_and_run(4)

        self.post_event("toggle_credit_play")
        self.advance_time_and_run(0.5)
        self.assertIn("FREE PLAY", self._texts())

    # A coin shows the credits slide, up until 5s after the last one
    def test_credits_slide(self):
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(4)
        self._coin()
        self.assertEqual("credits_slide", self._slide())
        self.assertIn("1/2", self._texts(""))
        self.advance_time_and_run(3)
        self._coin()
        self.assertIn("1", self._texts(""))
        self.advance_time_and_run(4)
        # (7s since the first, 4 since the last)
        self.assertEqual("credits_slide", self._slide())
        self.advance_time_and_run(1.5)
        self.assertNotEqual("credits_slide", self._slide())

    # The attract splash shows FREE PLAY or the credits
    def test_splash(self):
        # (the attract rotation's splash, 12s in)
        self.advance_time_and_run(13)
        self.assertEqual("splash_slide",
            self.mc.targets["default"].current_slide_name)
        self.assertIn("FREE PLAY", self._texts(""))
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(0.5)
        self.assertIn("CREDITS 0", self._texts(""))
