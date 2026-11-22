from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestJackpotDisplay(DeathSaveMcTesting):

    # The jackpot widgets show over the mode's slide in the
    # mode's color (60%) while the callout plays: the jackpot
    # sounds post *_callout_played and *_callout_stopped
    def test_grooveline_jackpots(self):
        self._start_grooveline()
        self.assertEqual("grooveline_slide", self._slide().name)
        self.assertIsNone(self._overlay())

        self.post_event("jackpot_callout_played")
        self.advance_time_and_run(0.1)
        self.assertEqual("Jackpot!", self._overlay_text())
        self._assertModeColor("grooveline", self._overlay())
        self.assertAlmostEqual(0.6, self._overlay().opacity)
        # still over the mode's slide
        self.assertEqual("grooveline_slide", self._slide().name)

        # twice as long as the callout (0.87s)
        self.post_event("jackpot_callout_stopped")
        self.advance_time_and_run(1.4)
        self.assertEqual("Jackpot!", self._overlay_text())
        self.advance_time_and_run(0.4)
        self.assertIsNone(self._overlay())

        # another jackpot restarts it
        self.post_event("jackpot_callout_played")
        self.advance_time_and_run(1)
        self.post_event("jackpot_callout_played")
        self.advance_time_and_run(1.4)
        self.assertEqual("Jackpot!", self._overlay_text())
        self.assertEqual(1, len(self._jackpot_widgets("Text")))

        # a super jackpot (queued behind a jackpot) replaces it
        # when it plays, for twice its callout (1.14s)
        self.post_event("super_jackpot_callout_played")
        self.advance_time_and_run(0.1)
        self.assertEqual(["SUPER JACKPOT!"],
            [ w.text for w in self._jackpot_widgets("Text") ])
        self.advance_time_and_run(2.1)
        self.assertEqual("SUPER JACKPOT!", self._overlay_text())
        self.advance_time_and_run(0.2)
        self.assertIsNone(self._overlay())

    # the widgets last twice as long as the callouts
    def test_widgets_last_twice_the_callouts(self):
        import subprocess
        from mpf.core.utility_functions import Util
        for sound, widget in [("jackpot", "jackpot"),
                ("jackpot_double", "super_jackpot")]:
            path = self.mc.sounds[sound].file
            length = float(subprocess.check_output(["ffprobe", "-v",
                "error", "-show_entries", "format=duration", "-of",
                "csv=p=0", path]))
            for mode in ["grooveline", "grand_prix", "luxury"]:
                event = ("super_" if widget == "super_jackpot" else "") \
                    + "jackpot_callout_played"
                settings = self.mc.modes[mode].config["widget_player"][
                    event][f"{widget}_{mode}"]["widget_settings"]
                self.assertAlmostEqual(2 * length,
                    Util.string_to_secs(settings["expire"]), delta=0.05)

    def test_grand_prix_jackpot_is_pink(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("grand_prix_multiball_ready")
        self.hit_switch_and_run("s_hole_backfire", 8)
        self.assertModeRunning("grand_prix")
        self.post_event("jackpot_callout_played")
        self.advance_time_and_run(0.1)
        self.assertEqual("Jackpot!", self._overlay_text())
        self._assertModeColor("grand_prix", self._overlay())

    def test_luxury_jackpot_is_yellow(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("luxury_qualifier_hit")
        self.advance_time_and_run(4)
        self.assertModeRunning("luxury")
        self.post_event("jackpot_callout_played")
        self.advance_time_and_run(0.1)
        self.assertEqual("Jackpot!", self._overlay_text())
        self._assertModeColor("luxury", self._overlay())

    # the jackpot sounds post the events the widgets follow
    def test_callouts_post_events(self):
        for sound, prefix in [("jackpot", "jackpot"),
                ("jackpot_double", "super_jackpot")]:
            config = self.mc.sounds[sound]
            self.assertEqual([f"{prefix}_callout_played"],
                config.events_when_played)
            self.assertEqual([f"{prefix}_callout_stopped"],
                config.events_when_stopped)

    def _start_grooveline(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.post_event("grooveline_qualifier_hit")
        self.advance_time_and_run(4)
        self.assertModeRunning("grooveline")

    def _slide(self):
        return self.mc.targets["default"].current_slide

    def _widgets(self):
        found = []
        def walk(widget):
            found.append(widget)
            for child in getattr(widget, "children", []):
                walk(child)
        walk(self.mc.targets["default"])
        return found

    # (widget_player keys its widgets "<mode>-<widget>")
    def _jackpot_widgets(self, kind):
        return [ w for w in self._widgets()
            if type(w).__name__ == kind
            and "jackpot" in (getattr(w, "key", None) or "") ]

    def _overlay(self):
        found = self._jackpot_widgets("Rectangle")
        return found[0] if found else None

    def _overlay_text(self):
        found = self._jackpot_widgets("Text")
        return found[0].text if found else None

    # the same color as the mode's tip title
    def _assertModeColor(self, mode, widget):
        title = self.mc.widgets[f"tip_title_{mode}"][0]
        for expected, actual in zip(title["color"], widget.color):
            self.assertAlmostEqual(expected, actual, places=2)
