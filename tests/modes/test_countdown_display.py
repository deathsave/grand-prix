from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestCountdownDisplay(DeathSaveMcTesting):

    # Getting under green says Get Ready (straight away, before the
    # green flag slide can show alone), then counts down 3, 2, 1, Race! on the
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
        self.assertEqual([["Get Ready"], ["3"], ["2"], ["1"], ["Race!"]],
            shown)
        # each one appears with its chime's event
        order = [ entry[1] if entry[0] == "event" else entry[1][0]
            for entry in self.seen ]
        self.assertEqual(["Get Ready", "off_the_line_countdown3", "3",
            "off_the_line_countdown2", "2", "off_the_line_countdown1", "1",
            "green_flag_dropped", "Race!"], order)
        self.assertEqual([], self._texts())

    # Something's always up from Get Ready to Race! (a gap flashed the
    # green flag slide through)
    def test_no_gaps(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        samples = []
        for _ in range(400):  # 8s, every 20ms
            self.advance_time_and_run(0.02)
            samples.append(self._texts())
        first = next(i for i, t in enumerate(samples) if t)
        race = next(i for i, t in enumerate(samples) if t == ["Race!"])
        self.assertEqual([], [ i for i in range(first, race)
            if not samples[i] ])

    def _texts_with(self, key):
        found = []
        def walk(widget):
            if type(widget).__name__ == "Text" and \
                    key in (getattr(widget, "key", None) or ""):
                found.append(widget.text)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    # A successful Off the Line skill shot takes over from Race!
    def test_off_the_line_slide(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        for _ in range(160):
            self.advance_time_and_run(0.05)
            if self._texts() == ["Race!"]:
                break
        self.post_event("off_the_line_hit")
        self.advance_time_and_run(0.1)
        self.assertEqual([], self._texts_with("countdown_race"))
        self.assertEqual(["Off the line!", "SKILL SHOT  25,000"],
            self._texts_with("off_the_line"))
        self.advance_time_and_run(3.5)
        self.assertEqual([], self._texts_with("off_the_line"))

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

    # Get Ready is up straight away, so the green flag slide never
    # shows on its own before the countdown
    def test_get_ready_straight_away(self):
        self._start_and_expire_ball_save()
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(0.1)
        self.assertEqual(["Get Ready"], self._texts())

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
