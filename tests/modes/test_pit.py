from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestPitMode(DeathSaveGameTesting):

    def test_loop_gate(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)

        self.assertEqual(
            True, self.machine.diverters["loop_gate"].enabled)
        self.hit_and_release_switch("s_shooter_lane")
        self.assertEqual(
            True, self.machine.diverters["loop_gate"].active)
        self.hit_and_release_switch("s_grooveline")
        self.assertEqual(
            False, self.machine.diverters["loop_gate"].active)

    def test_scoring(self):
        score = "score"

        self._start()
        self.hit_and_release_switch("s_shooter_lane")

        self.assertEqual(0, self.machine.game.player.score)
        self._assertIncrement(score, "s_pit_lube", 100)
        self._assertIncrement(score, "s_pit_tires", 100)

        # most switches only score 1 point
        self._assertIncrement(score, "s_pop1", 10)
        self._assertIncrement(score, "s_pop2", 10)
        self._assertIncrement(score, "s_grooveline", 10)
        self._assertIncrement(score, "s_hole_backfire", 10)
        self._assertIncrement(score, "s_hole_prix", 10)
        self._assertIncrement(score, "s_hole_grand", 10)
        self._assertIncrement(score, "s_spinner", 10)
        self._assertIncrement(score, "s_target_save", 10)
        self._assertIncrement(score, "s_target_bonus", 10)
        self._assertIncrement(score, "s_swerve1", 10)
        self._assertIncrement(score, "s_swerve2", 10)
        self._assertIncrement(score, "s_slingshot1", 10)
        self._assertIncrement(score, "s_slingshot2", 10)
        self._assertIncrement(score, "s_inlane1", 10)
        self._assertIncrement(score, "s_inlane2", 10)
        self._assertIncrement(score, "s_outlane1", 10)
        self._assertIncrement(score, "s_outlane2", 10)

        # Activates green_flag mode, so check last
        # to prevent scoring false positives
        self._assertIncrement(score, "s_pit_fuel", 100)

    # The signals show each completed special mode:
    # Grooveline, Luxury, Grand Prix and Red Line
    def test_progress_signals(self):
        self._start()
        player = self.machine.game.player
        pit = self.machine.modes["pit"]
        signals = {"is_grooveline_completed": "l_signal1",
            "is_luxury_completed": "l_signal2",
            "is_grand_prix_completed": "l_signal3",
            "is_red_line_completed": "l_signal4"}
        for variable, light in signals.items():
            pit.update_progress()
            self.assertLightColor(light, "black")
            setattr(player, variable, 1)
            pit.update_progress()
            self.assertLightColor(light, "white")

    def _count(self, *events):
        counts = {event: 0 for event in events}
        def counter(event):
            def handler(**kwargs):
                counts[event] += 1
            return handler
        for event in events:
            self.machine.events.add_handler(event, counter(event))
        return counts

    # A pit target only "fills" (and plays its sound) when its
    # resource is low, otherwise it's the bell
    def test_fill_only_when_low(self):
        counts = self._count("pit_fuel_filled", "pit_lube_filled",
            "pit_resource_full")
        self._start_and_expire_ball_save()
        player = self.machine.game.player
        self.assertEqual(1, player.level_fuel)
        self.assertEqual(2, player.level_lube)

        self.hit_and_release_switch("s_pit_lube")
        self.advance_time_and_run(1)
        self.assertEqual(0, counts["pit_lube_filled"])
        self.assertEqual(1, counts["pit_resource_full"])

        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        self.assertEqual(1, counts["pit_fuel_filled"])
        self.assertEqual(2, player.level_fuel)
        # (and that was the last one, so it's racing)
        self.assertModeRunning("green_flag")

        # pit targets during Green Flag are just the bell
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(1)
        self.assertEqual(1, counts["pit_fuel_filled"])
        self.assertEqual(2, counts["pit_resource_full"])

    def _flashing(self, light):
        seen = set()
        for i in range(10):
            self.advance_time_and_run(0.05)
            seen.add(self.machine.lights[light].get_color().rgb)
        return len(seen) > 1

    # A low resource flashes its pit insert until it's filled
    # (and fuel its "shoot" insert too), at ball start and after
    # leaving Green Flag
    def test_low_resources_flash(self):
        self._start_and_expire_ball_save()
        self.advance_time_and_run(2)
        self.assertTrue(self._flashing("l_pit_fuel"))
        self.assertTrue(self._flashing("l_pit_shoot_fuel"))
        self.assertFalse(self._flashing("l_pit_lube"))

        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        self.assertModeRunning("green_flag")
        self.assertFalse(self._flashing("l_pit_fuel"))
        self.assertFalse(self._flashing("l_pit_shoot_fuel"))

        # the tires wear out, so it's back to the pit
        self.machine.game.player.level_tires = 1
        self.machine.events.post("pit_required_tires")
        self.advance_time_and_run(2)
        self.assertModeNotRunning("green_flag")
        self.assertTrue(self._flashing("l_pit_tires"))
        self.assertFalse(self._flashing("l_pit_fuel"))
