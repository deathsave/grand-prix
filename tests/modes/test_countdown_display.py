from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestCountdownDisplay(DeathSaveMcTesting):

    # Getting under green counts down 3, 2, 1, Race! on the
    # display with the chimes (shows/under_green.yaml), the
    # last on the final ding (green_flag_dropped)
    def test_countdown_with_chimes(self):
        self.seen = []
        for event in ["off_the_line_countdown3",
                "off_the_line_countdown2", "off_the_line_countdown1",
                "green_flag_dropped"]:
            self.machine.events.add_handler(event, self._chimed,
                event_name=event)
        self._start_and_expire_ball_save()
        # fill up the tank to get under green (not _start_green_flag,
        # which waits out the countdown)
        self.hit_and_release_switch("s_pit_fuel")
        for _ in range(160):  # 8s, every 50ms
            texts = self._texts()
            if texts and (not self.seen or self.seen[-1][1] != texts):
                self.seen.append(("show", texts))
            self.advance_time_and_run(0.05)
        shown = [ texts for kind, texts in self.seen if kind == "show" ]
        self.assertEqual([["3"], ["2"], ["1"], ["Race!"]], shown)
        # each one appears with its chime's event
        order = [ entry[1] if entry[0] == "event" else entry[1][0]
            for entry in self.seen ]
        self.assertEqual(["off_the_line_countdown3", "3",
            "off_the_line_countdown2", "2", "off_the_line_countdown1", "1",
            "green_flag_dropped", "Race!"], order)
        self.assertEqual([], self._texts())

    # Race! is over the green flag image, on lime at 60%
    def test_race_background(self):
        from mpf.core.rgb_color import RGBColor
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        for _ in range(160):
            self.advance_time_and_run(0.05)
            if self._texts() == ["Race!"]:
                break
        self.assertEqual(["Race!"], self._texts())
        widgets = self._countdown_widgets()
        image = [ w for w in widgets if type(w).__name__ == "ImageWidget" ]
        self.assertEqual(1, len(image))
        self.assertEqual("green-flag-background", image[0].config["image"])
        rect = [ w for w in widgets if type(w).__name__ == "Rectangle" ][0]
        self.assertAlmostEqual(0.6, rect.opacity)
        lime = RGBColor(self.mc.machine_config["named_colors"]["lime"]).rgb
        for expected, actual in zip(lime, rect.color):
            self.assertAlmostEqual(expected / 255, actual, places=2)

    def _chimed(self, event_name, **kwargs):
        self.seen.append(("event", event_name))

    def _texts(self):
        return [ w.text for w in self._countdown_widgets()
            if type(w).__name__ == "Text" ]

    def _countdown_widgets(self):
        found = []
        def walk(widget):
            if "countdown" in (getattr(widget, "key", None) or ""):
                found.append(widget)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found
