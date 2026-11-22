from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestCreditsDisplay(DeathSaveMcTesting):

    def _texts(self):
        found = []
        def walk(widget):
            if type(widget).__name__ == "Text" and \
                    "credits" in (getattr(widget, "key", None) or ""):
                found.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    # Toggling says which it is, and coins show the credits
    def test_messages(self):
        self.advance_time_and_run(10)
        self.post_event("toggle_credit_play")
        self.advance_time_and_run(0.5)
        self.assertIn("CREDIT PLAY", self._texts())
        self.advance_time_and_run(4)

        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(0.5)
        self.assertIn("INSERT COINS", self._texts())
        self.advance_time_and_run(4)

        for i in range(2):
            self.hit_and_release_switch("s_credit")
            self.advance_time_and_run(0.2)
        self.assertIn("CREDITS 1", self._texts())
        self.advance_time_and_run(3)

        self.post_event("toggle_credit_play")
        self.advance_time_and_run(0.5)
        self.assertIn("FREE PLAY", self._texts())
