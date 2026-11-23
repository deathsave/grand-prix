from tests.support.death_save_game_testing import DeathSaveGameTesting

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
        # each lap is a luxury step
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

        # and so is every 8 spins
        for i in range(6):
            self.hit_and_release_switch("s_spinner")
            self.advance_time_and_run(1)
        self.assertEqual(
            7, self.machine.game.player.spin_counter_count)
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)
        self.hit_and_release_switch("s_spinner")
        self.assertEqual(
            0, self.machine.game.player.spin_counter_count)
        self.assertEqual(
            2, self.machine.game.player.luxury_counter_count)

        # ball drains and ball 2 begins
        for i in range(2):
            self.hit_switch_and_run("s_trough1", 4)
            self.hit_and_release_switch("s_shooter_lane")

        # wait for end of ball bonus
        self.advance_time_and_run(6)

        # Green flag mode resumes
        self.assertModeNotRunning("luxury")
        self.assertModeRunning("green_flag")
        # Count doesn't reset between balls
        # in contrast with grooveline mode
        self.assertEqual(
            2, self.machine.game.player.luxury_counter_count)
        self.assertEqual(
            0, self.machine.game.player.grooveline_counter_count)

        # Lights in top-east chain show progress
        self.assertLightColor('l_bonus01', 'white')
        self.assertLightColor('l_bonus02', 'white')
        self.assertLightColor('l_bonus03', 'black')
        # etc...

        # Mult-ball light indicator off
        self.assertLightColor('l_multiball', 'black')

        # Player hits the spinner a lot
        self._start_luxury()

    def test_multiball(self):
        self._start_luxury_multiball()
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

    def test_multiball_scoring(self):
        self._start_luxury_multiball()

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_target_bonus", 1)
        self.assertEqual(
            score + 75000, self.machine.game.player.score)

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_hole_prix", 1)
        self.assertEqual(
            score + 75000, self.machine.game.player.score)

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_spinner", 1)
        self.assertEqual(
            score + 75000, self.machine.game.player.score)

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_grooveline", 1)
        # (after the spinner, that's a lap too: 5k)
        self.assertEqual(
            score + 75000 + 5000, self.machine.game.player.score)

        score = self.machine.game.player.score
        self.hit_switch_and_run("s_hole_grand", 1)
        self.assertEqual(
            score + 75000, self.machine.game.player.score)

        # Getting 6/6 shots is only the super jackpot
        score = self.machine.game.player.score
        self.hit_switch_and_run("s_target_save", 1)
        self.assertEqual(
            score + 300000, self.machine.game.player.score)

        # Completion also ends the mode, once the jackpot
        # callouts have had a few seconds
        self.assertModeRunning("luxury")
        self.advance_time_and_run(3)
        self.assertModeNotRunning("luxury")

    def _start_luxury_multiball(self):
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

    # With the multiplier, each spin counts that many times
    def test_multiplier_spins(self):
        self._start()
        self._start_green_flag()
        player = self.machine.game.player
        player.multiplier = 2
        for i in range(3):
            self.hit_and_release_switch("s_spinner")
            self.advance_time_and_run(0.5)
        self.assertEqual(6, player.spin_counter_count)
        self.assertEqual(0, player.luxury_counter_count)
        # reaching 8 (or more) completes a step
        # (extra counts past 8 are not carried over)
        player.multiplier = 3
        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(0.5)
        self.assertEqual(1, player.luxury_counter_count)
        self.assertEqual(0, player.spin_counter_count)
        # back to 1X
        player.multiplier = 1
        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(0.5)
        self.assertEqual(1, player.spin_counter_count)

    # The skill shot (which drops the green flag) is a step
    def test_skill_shot_step(self):
        self._start()
        self.assertModeNotRunning("green_flag")
        self.hit_switch_and_run("s_hole_backfire", 2)
        self.assertModeRunning("green_flag")
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

    # Off the line is a step
    def test_off_the_line_step(self):
        self._start()
        self._start_green_flag()
        self.machine.events.post("off_the_line_hit")
        self.advance_time_and_run(1)
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

    # Completing Backfire Pops (back to green) is a step
    def test_backfire_pops_step(self):
        self._start()
        self._start_backfire()
        self.assertEqual(
            0, self.machine.game.player.luxury_counter_count)
        for i in range(10):
            self.hit_and_release_switch("s_pop1")
            self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")
        self.assertEqual(
            1, self.machine.game.player.luxury_counter_count)

    # Swerve hits count like spinner hits
    def test_swerve_counts_as_spins(self):
        self._start()
        self._start_green_flag()
        player = self.machine.game.player
        self.hit_and_release_switch("s_swerve1")
        self.hit_and_release_switch("s_swerve2")
        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(0.5)
        self.assertEqual(3, player.spin_counter_count)
        # and count extra with the multiplier
        player.multiplier = 2
        self.hit_and_release_switch("s_swerve1")
        self.advance_time_and_run(0.5)
        self.assertEqual(5, player.spin_counter_count)
        # 8 total is a luxury step
        for i in range(3):
            self.hit_and_release_switch("s_swerve2")
            self.advance_time_and_run(0.5)
        self.assertEqual(1, player.luxury_counter_count)

    # Not outside of green flag
    def test_swerve_needs_green_flag(self):
        self._start()
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_swerve1")
        self.advance_time_and_run(0.5)
        self.assertEqual(0, self.machine.game.player.spin_counter_count)

    # Completing Luxury counts for the bonus, but not its shot group
    # starting (which also posts luxury_complete)
    def test_completion_for_the_bonus(self):
        self._start_luxury_multiball()
        player = self.machine.game.player
        self.assertEqual(0, player.is_luxury_super)
        for switch in ["s_target_bonus", "s_hole_prix", "s_spinner",
                "s_grooveline", "s_hole_grand", "s_target_save"]:
            self.hit_switch_and_run(switch, 1)
        self.assertEqual(1, player.is_luxury_super)
