from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestPitMode(DeathSaveGameTesting):

    def test_loop_gate(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)

        self.assertEqual(
            True, self.machine.diverters["loop_gate"].enabled)
        self.hit_and_release_switch("s_shooter_lane")
        # (it's a plunge once the switch has stayed open 80ms)
        self.advance_time_and_run(0.1)
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
        # (low tires as well as fuel, so the left inlane's Tune Up only
        # fills one of two and doesn't start Green Flag)
        self.machine.game.player.level_tires = 1
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

    # The shooter lane switch bounces open as a ball rolls in and
    # settles: that's not a plunge (the gate stays shut, the skill shot
    # timer doesn't start), and the real plunge still opens the gate
    def test_shooter_lane_bounce_isnt_a_plunge(self):
        self.mock_event("shooter_lane_plunged")
        self._start()
        # (_start plunged ball 1; ball 2 for a fresh first plunge)
        self._expire_ball_save()
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(20)
        self.assertEqual(2, self.machine.game.player.ball)
        self.mock_event("shooter_lane_plunged")
        gate = self.machine.diverters["loop_gate"]
        self.release_switch_and_run("s_shooter_lane", 0.034)
        self.hit_switch_and_run("s_shooter_lane", 1)
        self.assertEventNotCalled("shooter_lane_plunged")
        self.assertFalse(gate.active)
        self.assertFalse(self.machine.timers["skill_shot"].running)
        self.release_switch_and_run("s_shooter_lane", 0.1)
        self.assertEventCalled("shooter_lane_plunged")
        self.assertTrue(gate.active)

    # The left inlane/outlane (which fire with no ball, after coils)
    # don't count as the ball reaching the playfield: a ball that
    # falls back into the shooter lane waits for a plunge, it isn't
    # auto launched
    def test_left_lanes_dont_confirm_a_launch(self):
        from unittest.mock import MagicMock
        self._start()
        self._expire_ball_save()
        self.hit_switch_and_run("s_trough1", 3)
        self.advance_time_and_run(20)
        self.assertEqual(2, self.machine.game.player.ball)
        kicker = self.machine.coils["c_auto_kicker"]
        kicker.pulse = MagicMock()
        gate = self.machine.diverters["loop_gate"]
        # the ball rolls off the switch, the phantom pair fires, and the
        # ball rolls back
        self.release_switch_and_run("s_shooter_lane", 0.25)
        self.hit_and_release_switch("s_inlane1")
        self.hit_and_release_switch("s_outlane1")
        self.advance_time_and_run(0.3)
        self.assertTrue(gate.active)
        self.hit_switch_and_run("s_shooter_lane", 5)
        self.assertEqual(0, kicker.pulse.call_count)
        self.assertEqual(0, self.machine.game.player.is_playfield_active)

    # A soft plunge holds the gate open 5s (it shut at 2s, so a slow
    # ball dropped toward the Backfire Hole), and one that rolls back
    # into the shooter lane within 3s gets the gate (and the skill shot
    # timer) again on the next plunge
    def test_soft_plunge_rolls_back(self):
        # (ball 1, in the shooter lane)
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertEqual(1, self.machine.ball_devices["bd_shooter_lane"].balls)
        self.mock_event("shooter_lane_rolled_back")
        gate = self.machine.diverters["loop_gate"]
        timer = self.machine.timers["skill_shot"]
        # a soft plunge: open, and still open 2.5s later (it was 2s)
        self.release_switch_and_run("s_shooter_lane", 2.5)
        self.assertTrue(gate.active)
        self.assertTrue(timer.running)
        # it rolled back without reaching the playfield
        self.hit_switch_and_run("s_shooter_lane", 0.5)
        self.assertEventCalled("shooter_lane_rolled_back")
        self.assertFalse(gate.active)
        self.assertFalse(timer.running)
        self.assertEqual(7, timer.ticks)
        # and the next plunge opens it again (after the gate's 1s cool
        # down, about how long a re-plunge takes anyway)
        self.advance_time_and_run(1.5)
        self.release_switch_and_run("s_shooter_lane", 0.5)
        self.assertTrue(gate.active)
        self.assertTrue(timer.running)
