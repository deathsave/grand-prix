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
        self.assertEqual(self.machine.game.player.score, 1000)

        # restores all pit resources to max
        self.assertEqual(
            2, self.machine.game.player.level_fuel)
        self.assertEqual(
            2, self.machine.game.player.level_lube)
        self.assertEqual(
            2, self.machine.game.player.level_tires)

        # and starts green flag
        self.assertModeRunning("green_flag")
