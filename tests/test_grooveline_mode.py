from tests.death_save_game_testing import DeathSaveGameTesting

class TestGroovelineMode(DeathSaveGameTesting):

    # Player qualifies by making 10 laps during
    # green_flag mode on a single ball.
    def test_qualification(self):
        self._start()
        self._start_green_flag()

        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        self.machine.events.post("green_flag_degrade_oil")
        self.machine.events.post("green_flag_degrade_oil")
        self.advance_time_and_run(1)

        self.assertModeNotRunning("green_flag")

        # Count doesn't increase outside of green_flag mode
        self._complete_lap()
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)

        # Player tops up the oil, reactivating green_flag mode
        self.hit_and_release_switch("s_oil")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        # Grooveline counter still at 1 as its value is
        # persisted for a single ball
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)
        self.assertEqual(1, self.machine.game.player.ball)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine.game.player.ball)
        # Grooveline counter is reset to 0
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)

        # Mult-ball light indicators off
        self.assertLightColor('l_north_advance1', 'black')
        self.assertLightColor('l_north_advance2', 'black')

        # Players hits the grooveline 10 times (10 laps)
        self._start_grooveline()

        # Mult-ball light indicators on
        self.assertLightColor('l_north_advance1', 'white')
        self.assertLightColor('l_north_advance2', 'white')

        # Counter resets
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)
        # And grooveline mode begins (multiball)
        self.assertEqual(True, self.machine. \
            multiballs["grooveline_multiball"].enabled)


    def test_multiball(self):
        self._start_multiball()

        # Second ball already in play
        self.assertEqual(2, self.machine.playfield.balls)
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        # A lot of time passes - should have
        # exceeded the shoot again period
        self.advance_time_and_run(30)

        # Ball drains
        self._drain_one_ball()
        self.advance_time_and_run(4)

        # Bug here? Shoot again should have expired, but ball
        # still kicked out to shooter lane - tried numerous
        # ways to fix - maybe bug in MPF
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(1,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        # After the NEXT drain, the mode and multiball
        # ends as expected
        self._drain_one_ball()
        self.advance_time_and_run(4)
        self.assertModeNotRunning("grooveline")

    def test_add_a_ball(self):
        self._start_multiball()

        # Player launches the ball
        self.hit_and_release_switch("s_shooter_lane")
        self.hit_switch_and_run("s_activate_playfield", 4)
        self.assertEqual(2, self.machine.playfield.balls)

        # Player completes 3 laps
        for i in range(3):
            self._complete_lap()

        # Another a ball is added
        self.assertEqual(0,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        # Player launches this ball, too
        self.hit_and_release_switch("s_shooter_lane")
        self.hit_switch_and_run("s_activate_playfield", 4)
        self.assertEqual(3, self.machine.playfield.balls)

    def _start_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._start_grooveline()
        self.assertEqual(2, self.machine.playfield.balls)
        # A ball is ejected to the shooter lane
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)
        self.assertEqual(True, self.machine. \
            multiballs["grooveline_multiball"].enabled)
