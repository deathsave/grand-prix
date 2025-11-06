from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestSkillShots(DeathSaveGameTesting):

    # After launch, get into the backfire hole
    def test_backfire_skillshot(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_shooter_lane")

        # skill shot timer should be running now
        self.assertEqual(True,
            self.machine.timers["skill_shot"].running)

        # show plays alternating lights
        # at the top of the playfield
        self.advance_time_and_run(0.1)
        self.assertLightColor('l_swerve1', 'white')
        self.assertLightColor('l_backfire', 'black')
        self.assertLightColor('l_swerve2', 'black')
        self.advance_time_and_run(0.2)
        self.assertLightColor('l_swerve1', 'black')
        self.assertLightColor('l_backfire', 'white')
        self.assertLightColor('l_swerve2', 'black')
        self.advance_time_and_run(1)
        self.assertLightColor('l_swerve1', 'black')
        self.assertLightColor('l_backfire', 'black')
        self.assertLightColor('l_swerve2', 'white')

        self.hit_and_release_switch("s_backfire_hole")
        self.assertEqual(self.machine.game.player.score, 25000)

        # restores all pit resources to max
        self.assertEqual(
            2, self.machine.game.player.level_fuel)
        self.assertEqual(
            2, self.machine.game.player.level_lube)
        self.assertEqual(
            2, self.machine.game.player.level_tires)

        # and starts green flag
        self.assertModeRunning("green_flag")

    def test_off_the_line_skill_shot_timeout(self):
        self._qualify_off_the_line_skill_shot()

        # player has only a half second to get
        # a solid start off the line
        self.advance_time_and_run(0.5)
        self.assertEqual(False,
            self.machine.timers["off_the_line"].running)
        # skill shot failed
        self.assertEqual(0,
            self.machine.shots["off_the_line"].state)

    def test_off_the_line_skill_shot_plunge(self):
        self._qualify_off_the_line_skill_shot()
        score = self.machine.game.player.score

        # player successfully gets the ball out of the
        # shooter lane during the brief window
        self.hit_and_release_switch("s_shooter_lane")
        # print("*******************************")
        # print(self.machine.shots["off_the_line"].state)
        # print("*******************************")
        # skill shot succeeded
        self.assertEqual(1,
            self.machine.shots["off_the_line"].state)
        self.assertEqual(score + 5000,
            self.machine.game.player.score)

    def _qualify_off_the_line_skill_shot(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()

        # ball drains and ball 2 begins
        self.hit_switch_and_run("s_trough1", 3)

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine.game.player.ball)

        # "under green" show runs... ding, ding, ding... dong!
        self.advance_time_and_run(2.5)

        # off the line timer should be running now
        self.assertEqual(True,
            self.machine.timers["off_the_line"].running)
