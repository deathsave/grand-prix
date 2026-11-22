from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestGroovelineMode(DeathSaveGameTesting):

    # Player qualifies by making 10 laps during
    # green_flag mode on a single ball.
    def test_qualification(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()

        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        self.machine.events.post("green_flag_degrade_lube")
        self.machine.events.post("green_flag_degrade_lube")
        self.advance_time_and_run(1)

        self.assertModeNotRunning("green_flag")

        # Count doesn't increase outside of green_flag mode
        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        # Player tops up the lube, reactivating green_flag mode
        self.hit_and_release_switch("s_pit_lube")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        # Grooveline counter still at 1 as its value is
        # persisted for a single ball
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)
        self.assertEqual(1, self.machine.game.player.ball)

        # ball drains and ball 2 begins
        self.hit_switch_and_run("s_trough1", 3)

        # wait for end of ball bonus
        self.advance_time_and_run(15)

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine.game.player.ball)

        # Grooveline counter persists across balls
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        # Mult-ball light indicators off
        self.assertLightColor('l_multiball', 'black')

        # Players hits the grooveline 10 times (10 laps)
        self._sim_grooveline()

        # Mult-ball light indicators on
        self.assertLightColor('l_multiball', 'white')

        # Counter resets
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)
        # And grooveline mode begins (multiball)
        self.assertEqual(True,
            self.machine.multiballs["grooveline"].enabled)

    def test_multiball(self):
        self._start_multiball()
        # started, but not completed, yet
        self.assertEqual(
            0, self.machine.game.player.is_grooveline_completed)

        # Second ball already in play
        self.assertEqual(2, self.machine.playfield.balls)
        # only 2 left in the trough
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        self._expire_ball_save()

        # Ball drains
        self._drain_one_ball()
        self.advance_time_and_run(4)

        # the mode and multiball ends
        self.assertModeNotRunning("grooveline")

        self.advance_time_and_run(4)

        # And wizard progress is updated
        self.assertEqual(
            1, self.machine.game.player.is_grooveline_completed)

    # The multiball target hit that starts the mode is not a shot
    def test_starting_hit_is_not_a_shot(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.machine.events.post("logicblock_grooveline_counter_complete")
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_target_multiball")
        self.advance_time_and_run(4)
        self.assertModeRunning("grooveline")
        self.assertEqual(0, self._count("grooveline_jackpot"))

    # The top Grooveline insert, multiball lamp and top Grand
    # insert blink. Any of the shots lights the Grooveline
    # inserts from the bottom up, paying a growing jackpot,
    # and the 10th pays the super jackpot.
    def test_shots(self):
        self._start_multiball()
        self.assertEqual([], self._lit_inserts())
        for light in ["l_grooveline01", "l_multiball", "l_grand1"]:
            self.assertTrue(self._blinking(light), light)

        switches = ["s_grooveline", "s_target_multiball",
            "s_target_save"]
        for hit in range(1, 10):
            score = self.machine.game.player.score
            self.hit_and_release_switch(switches[hit % 3])
            self.advance_time_and_run(1)
            self.assertEqual(hit, self._count("grooveline_jackpot"))
            self.assertEqual(40000 + 10000 * hit,
                self._jackpot_values[-1])
            self.assertGreaterEqual(
                self.machine.game.player.score - score,
                40000 + 10000 * hit)
            self.assertEqual(list(range(11 - hit, 11)),
                self._lit_inserts())
        self.assertTrue(self._blinking("l_grooveline01"))
        self.assertEqual(0, self._count("grooveline_super_jackpot"))

        # the Grand hole counts too
        score = self.machine.game.player.score
        self.hit_switch_and_run("s_hole_grand", 3)
        self.assertEqual(1, self._count("grooveline_super_jackpot"))
        self.assertGreaterEqual(
            self.machine.game.player.score - score, 640000)
        self.assertEqual(list(range(1, 11)), self._lit_inserts())
        for light in ["l_multiball", "l_grand1"]:
            self.assertFalse(self._blinking(light), light)

        # done for this multiball
        self.hit_and_release_switch("s_grooveline")
        self.advance_time_and_run(1)
        self.assertEqual(10, self._count("grooveline_jackpot"))

    # Completing the shots bumps the multiplier until the mode ends
    def test_completing_shots_bumps_multiplier(self):
        self._start_multiball()
        player = self.machine.game.player
        self.assertEqual(1, player.multiplier)
        self._complete_shots()
        self.assertEqual(2, player.multiplier)
        self.assertLightColor("l_multiplier2", "white")

        # outlasts the 30s multiplier timer
        self.advance_time_and_run(40)
        self.assertEqual(2, player.multiplier)

        self._expire_ball_save()
        self._drain_one_ball()
        self.advance_time_and_run(4)
        self.assertModeNotRunning("grooveline")
        self.assertEqual(1, player.multiplier)
        self.assertEqual(0, player.is_grooveline_boosted)

    # 2X (from swerves) goes up to 5X
    def test_bump_from_2x(self):
        self._start_multiball()
        player = self.machine.game.player
        player.multiplier = 2
        self.advance_time_and_run(1)
        self._complete_shots()
        self.assertEqual(5, player.multiplier)
        self.advance_time_and_run(40)
        self.assertEqual(5, player.multiplier)

    def _complete_shots(self):
        for _ in range(10):
            self.hit_and_release_switch("s_grooveline")
            self.advance_time_and_run(0.5)
        self.assertEqual(1, self._count("grooveline_super_jackpot"))

    # The shots' lights are removed when the mode ends
    def test_shot_lights_end_with_mode(self):
        self._start_multiball()
        self.hit_and_release_switch("s_grooveline")
        self.advance_time_and_run(1)
        self._expire_ball_save()
        self._drain_one_ball()
        self.advance_time_and_run(4)
        self.assertModeNotRunning("grooveline")
        for light in self.machine.lights:
            for entry in light.stack:
                self.assertNotEqual("grooveline_shots", entry.key)

    def _lit_inserts(self):
        return [ i for i in range(1, 11) if self.machine.lights[
            f"l_grooveline{i:02}"].get_color().rgb != (0, 0, 0)
            and not self._blinking(f"l_grooveline{i:02}") ]

    # on, then off, within a blink
    def _blinking(self, light):
        seen = set()
        for _ in range(6):
            seen.add(self.machine.lights[light].get_color().rgb
                != (0, 0, 0))
            self.advance_time_and_run(0.1)
        return seen == {True, False}

    def _count(self, event):
        return self._event_counts.get(event, 0)

    def setUp(self):
        super().setUp()
        self._event_counts = {}
        self._jackpot_values = []
        for event in ["grooveline_jackpot", "grooveline_super_jackpot"]:
            self.machine.events.add_handler(event, self._count_event,
                event_name=event)

    def _count_event(self, event_name, value=None, **kwargs):
        self._event_counts[event_name] = \
            self._event_counts.get(event_name, 0) + 1
        if value is not None:
            self._jackpot_values.append(value)

    def _start_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._sim_grooveline()
        self.assertEqual(2, self.machine.playfield.balls)
        # A ball is ejected to the shooter lane
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)
        self.assertEqual(True, self.machine. \
            multiballs["grooveline"].enabled)
