from tests.death_save_game_testing import DeathSaveGameTesting

class TestGrandPrixMode(DeathSaveGameTesting):

    # To qualify:
    #
    # - Advance "GRAND" by hitting s_save_target
    # - With GRAND lit, hit s_grand_hole to qualify "PRIX"
    # - Ball will be locked
    # - Advance "PRIX" by hitting s_bonus_target
    # - With PRIX lit, hit s_prix_hole to lock another ball
    # - Hit the multiball target to start the multiball
    #
    def test_qualification(self):
        self._start()
        self._start_green_flag()
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertEqual(True,
            self.machine.counters["grand_counter"].enabled)
        self.assertEqual(True,
            self.machine.counters["prix_counter"].enabled)
        self.assertEqual(0,
            self.machine.game.player.grand_prix_counter_count)

        # After lighting GRAND, the prix_counter is
        # enabled and the grand_counter is disabled
        self._qualify_grand()

        # Same goes for PRIX
        self._qualify_prix()

        self.assertModeNotRunning("grand_prix")
        # Mult-ball is ready, but we still need to activate it
        # but NOT by hitting the multiball target
        self.assertEqual(1,
            self.machine.game.player.is_multiball_ready)
        self.assertEqual(1,
            self.machine.game.player.is_grand_prix_multiball_ready)
        self.assertLightColor('l_multiball', 'black')

        # Player needs to get into the backfire hole,
        self.hit_switch_and_run("s_backfire_hole", 2)
        self.assertModeRunning("grand_prix")

    def test_grand_disqualification(self):
        self._start()
        self._start_green_flag()
        self.hit_and_release_switch("s_save_target")
        self.assertEqual(1,
            self.machine.game.player.grand_counter_count)
        self.hit_and_release_switch("s_save_target")
        self.assertEqual(2,
            self.machine.game.player.grand_counter_count)
        self.hit_and_release_switch("s_grand_hole")
        # TODO: consider also raising the disqualifier
        #       drop target here
        self.assertEqual(0,
            self.machine.game.player.grand_counter_count)

    def test_prix_disqualification(self):
        self._start()
        self._start_green_flag()
        self.hit_and_release_switch("s_bonus_target")
        self.assertEqual(1,
            self.machine.game.player.prix_counter_count)
        self.hit_and_release_switch("s_bonus_target")
        self.assertEqual(2,
            self.machine.game.player.prix_counter_count)
        self.hit_and_release_switch("s_prix_hole")
        # TODO: consider also raising the disqualifier
        #       drop target here
        self.assertEqual(0,
            self.machine.game.player.prix_counter_count)

    def test_multiball(self):
        self._start_multiball()
        # started, but not completed, yet
        self.assertEqual(
            0, self.machine.game.player.is_grand_prix_completed)

        # Player launches the ball
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)
        self.assertEqual(True,
            self.machine.multiballs["grand_prix"].shoot_again)

        # Counters should have been reset
        self.assertEqual(
            0, self.machine.game.player.grand_counter_count)
        self.assertEqual(
            0, self.machine.game.player.prix_counter_count)

        # And locks disabled
        self.assertEqual(False,
            self.machine.multiball_locks["grand_hole"].enabled)
        self.assertEqual(False,
            self.machine.multiball_locks["prix_hole"].enabled)

        # couple balls drain during shoot_again period
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(4)
        self.assertModeRunning("grand_prix")
        self.advance_time_and_run(4)
        # and those balls are returned to the playfield
        self.assertEqual(3, self.machine.playfield.balls)

        # shoot_again period expires after 8 more seconds
        self.advance_time_and_run(8)
        self.assertEqual(False,
            self.machine.multiballs["grand_prix"].shoot_again)

        # # two balls drain
        for i in range(2):
            self._drain_one_ball()
            self.advance_time_and_run(4)
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertEqual(2,
            self.machine.ball_devices["bd_trough"].balls)

        # Mode ends
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(None,
            self.machine.multiballs["grand_prix"].enabled)

        # And wizard progress is updated
        self.assertEqual(
            1, self.machine.game.player.is_grand_prix_completed)

        # Can be repeated later in the game
        self._qualify_grand()
        self._qualify_prix()
        self.hit_switch_and_run("s_backfire_hole", 2)
        self.assertModeRunning("grand_prix")

    def _qualify_grand(self):
        for i in range(5):
            self.hit_and_release_switch("s_save_target")
            self.assertModeRunning("green_flag")
        # Ball is held
        self.hit_switch_and_run("s_grand_hole", 1)
        self.assertEqual(False,
            self.machine.counters["grand_counter"].enabled)

    def _qualify_prix(self):
        for i in range(4):
            self.hit_and_release_switch("s_bonus_target")
        # Ball is held
        self.hit_switch_and_run("s_prix_hole", 1)
        self.assertEqual(False,
            self.machine.counters["prix_counter"].enabled)

    def _start_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        self._start_grand_prix()
        self.assertModeRunning("grand_prix")
        self.assertEqual(True,
            self.machine.multiballs["grand_prix"].enabled)

        # 3 ball multiball
        self.advance_time_and_run(4)
        self.assertEqual(3, self.machine.playfield.balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        # Mult-ball light indicator on
        self.assertLightColor('l_multiball', 'white')

