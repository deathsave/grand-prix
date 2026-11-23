from tests.support.death_save_game_testing import DeathSaveGameTesting

class TestSkillShots(DeathSaveGameTesting):

    # After launch, get into the backfire hole
    def test_backfire_skillshot(self):
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_shooter_lane")
        # (it's a plunge once the switch has stayed open 80ms)
        self.advance_time_and_run(0.08)

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

        self.hit_and_release_switch("s_hole_backfire")
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

        # player has under a second (0.8s) to get
        # a solid start off the line
        self.advance_time_and_run(0.7)
        self.assertEqual(True,
            self.machine.timers["off_the_line"].running)
        self.assertEventNotCalled("off_the_line_late")
        self.advance_time_and_run(0.2)
        self.assertEqual(False,
            self.machine.timers["off_the_line"].running)
        # skill shot failed
        self.assertEqual(0,
            self.machine.shots["off_the_line"].state)
        # and the player is told they're late
        self.assertEventCalled("off_the_line_late")

    # The window is centered on the final ding (the green
    # flag dropping): 0.4s before it to 0.4s after
    def test_off_the_line_window_centered(self):
        times = {}

        def record(name):
            def handler(**kwargs):
                times.setdefault(name, self.machine.clock.get_time())
            return handler

        for event in ["off_the_line_open", "green_flag_dropped",
                "timer_off_the_line_complete"]:
            self.machine.events.add_handler(event, record(event))
        self._qualify_off_the_line_skill_shot()
        self.advance_time_and_run(2)
        dropped = times["green_flag_dropped"]
        self.assertAlmostEqual(-0.4,
            times["off_the_line_open"] - dropped, delta=0.05)
        self.assertAlmostEqual(0.4,
            times["timer_off_the_line_complete"] - dropped, delta=0.15)

    # Plunging just before the final ding counts
    def test_off_the_line_before_final_ding(self):
        self._qualify_off_the_line_skill_shot()
        self.advance_time_and_run(0.2)
        self.assertEventNotCalled("green_flag_dropped")
        score = self.machine.game.player.score
        self.hit_and_release_switch("s_shooter_lane")
        # (it's a plunge once the switch has stayed open 80ms)
        self.advance_time_and_run(0.1)
        self.assertEqual(1, self.machine.shots["off_the_line"].state)
        self.assertEqual(score + 25000, self.machine.game.player.score)

    # Plunging in time isn't late
    def test_off_the_line_skill_shot_not_late(self):
        self._qualify_off_the_line_skill_shot()
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self.assertEventNotCalled("off_the_line_late")

    # Plunging before the window opens neither scores
    # nor is late
    def test_off_the_line_skill_shot_early(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self.mock_event("off_the_line_late")
        self.mock_event("off_the_line_hit")
        self.mock_event("off_the_line_open")
        self.hit_switch_and_run("s_trough1", 3)
        self.assertModeRunning("green_flag")
        self.assertEventNotCalled("off_the_line_open")
        # plunged during the countdown
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(5)
        self.assertEventCalled("off_the_line_open")
        self.assertEventNotCalled("off_the_line_hit")
        self.assertEventNotCalled("off_the_line_late")

    def test_off_the_line_skill_shot_plunge(self):
        self._qualify_off_the_line_skill_shot()
        score = self.machine.game.player.score
        # (late in the window still counts)
        self.advance_time_and_run(0.6)

        # player successfully gets the ball out of the
        # shooter lane during the brief window
        self.hit_and_release_switch("s_shooter_lane")
        # (it's a plunge once the switch has stayed open 80ms)
        self.advance_time_and_run(0.1)
        # skill shot succeeded
        self.assertEqual(1,
            self.machine.shots["off_the_line"].state)
        self.assertEqual(score + 25000,
            self.machine.game.player.score)

    # Starts ball 2 under green and runs until the Off the
    # Line window opens (0.4s before the final ding)
    def _qualify_off_the_line_skill_shot(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        for event in ["off_the_line_late", "off_the_line_open",
                "green_flag_dropped"]:
            self.mock_event(event)

        # ball drains and ball 2 begins
        self.hit_switch_and_run("s_trough1", 3)

        # Green flag mode resumes
        self.assertModeRunning("green_flag")
        self.assertEqual(2, self.machine.game.player.ball)

        # "under green" show runs... ding, ding, ding...
        for i in range(200):  # (up to 10s)
            if self._events["off_the_line_open"]:
                break
            self.advance_time_and_run(0.05)

        # off the line timer should be running now
        self.assertEqual(True,
            self.machine.timers["off_the_line"].running)

    # A successful Off the Line skill shot runs the chimes up, twice
    def test_off_the_line_chimes(self):
        from unittest.mock import MagicMock
        self._qualify_off_the_line_skill_shot()
        pulses = []
        for coil in ["c_chime1", "c_chime2", "c_chime3"]:
            self.machine.coils[coil].pulse = MagicMock(
                side_effect=lambda *a, coil=coil, **k: pulses.append(coil))
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1.5)
        self.assertEqual(1, self.machine.shots["off_the_line"].state)
        # (the green flag's final ding, c_chime3, lands in there too)
        self.assertEqual(2, pulses.count("c_chime1"))
        self.assertEqual(2, pulses.count("c_chime2"))
        self.assertIn(pulses.count("c_chime3"), [2, 3])
