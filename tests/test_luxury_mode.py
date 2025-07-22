from tests.death_save_game_testing import DeathSaveGameTesting

class TestLuxuryMode(DeathSaveGameTesting):

    # Player qualifies by hitting the spinner a number of times
    # accumulating across all 3 balls
    def test_qualification(self):
        self._start()
        self._start_green_flag()

        self._complete_lap()
        # we made a lap
        self.assertEqual(
            1, self.machine.game.player.grooveline_counter_count)
        # and that means the spinner at least was hit once
        self.assertEqual(
            1, self.machine.game.player.spin_counter_count)
        # but it takes a lot of spins to qualify 1 luxury step
        self.assertEqual(
            0, self.machine.game.player.luxury_counter_count)

        for i in range(8):
            self.hit_and_release_switch("s_spinner")
            self.advance_time_and_run(1)
        self.assertEqual(
            9, self.machine.game.player.spin_counter_count)
        self.hit_and_release_switch("s_spinner")
        self.assertEqual(
            0, self.machine.game.player.spin_counter_count)
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        # wait for end of ball bonus
        self.advance_time_and_run(6)

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        # Count doesn't reset between balls
        # in contrast with grooveline mode
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)

        # Lights in top-east chain show progress
        self.assertLightColor('l_bonus_01', 'white')
        self.assertLightColor('l_bonus_02', 'black')
        self.assertLightColor('l_bonus_03', 'black')
        # etc...

        # Mult-ball light indicator off
        self.assertLightColor('l_multiball', 'black')

        # Player hits the spinner a lot
        self._start_luxury()

        # Mult-ball light indicator on
        self.assertLightColor('l_multiball', 'white')

    def test_multiball(self):
        self._start_multiball()
        # started, but not completed, yet
        self.assertEqual(
            0, self.machine.game.player.is_luxury_completed)

        # A lot of time passes - should have
        # exceeded the shoot again period
        self.advance_time_and_run(10)

        # ball drains
        self._drain_one_ball()
        self.advance_time_and_run(4)

        # the mode and multiball ends
        self.assertModeNotRunning("luxury")

        self.advance_time_and_run(4)

        # And wizard progress is updated
        self.assertEqual(
            1, self.machine.game.player.is_luxury_completed)

    def _start_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._start_luxury()
        self.assertEqual(2, self.machine.playfield.balls)
        # A ball is ejected to the shooter lane
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)
        self.assertEqual(True, self.machine. \
            multiballs["luxury"].enabled)
