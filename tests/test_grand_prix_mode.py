from tests.death_save_game_testing import DeathSaveGameTesting

class TestGrandPrixMode(DeathSaveGameTesting):

    # To qualify:
    #
    # - Advance "GRAND" by hitting s_grand_advance
    # - With GRAND lit, hit s_grand_hole to qualify "PRIX"
    # - Advance "PRIX" by hitting s_prix_advance
    # - With PRIX lit, hit s_prix_hole to lock in one letter
    # - Repeat 3 more times to qualify "GRAND PRIX" and
    #   start multiball
    #
    def test_qualification(self):
        self._start()
        self._start_green_flag()
        self.assertEqual(1, self.machine.playfield.balls)
        self.assertEqual(True,
            self.machine.counters["grand_counter"].enabled)
        self.assertEqual(False,
            self.machine.counters["prix_counter"].enabled)
        self.assertEqual(0,
            self.machine.game.player.grand_prix_counter_count)

        # After lighting GRAND, the prix_counter is
        # enabled and the grand_counter is disabled
        self._light_grand()
        self.assertEqual(5,
            self.machine.game.player.grand_counter_count)
        # Main counter unaffected so far
        self.assertEqual(0,
            self.machine.game.player.grand_prix_counter_count)

        # After lighting PRIX, the grand_counter is
        # re-enabled and user hits it 4 times
        self._light_prix()
        # Counter resets immediately
        self.assertEqual(0,
            self.machine.game.player.prix_counter_count)
        # And increases "Main" grand_prix_counter
        self.assertEqual(1,
            self.machine.game.player.grand_prix_counter_count)

        # Mult-ball light indicators off
        self.assertLightColor('l_north_advance1', 'black')
        self.assertLightColor('l_north_advance2', 'black')

        # Repeat sequence 3 more times
        for i in range(3):
            self._light_grand()
            self._light_prix()
        self.assertEqual(4,
            self.machine.game.player.grand_prix_counter_count)

        self.assertModeRunning("grand_prix")


    def test_grand_disqualification(self):
        self._start()
        self._start_green_flag()
        self.hit_and_release_switch("s_grand_advance")
        self.assertEqual(1,
            self.machine.game.player.grand_counter_count)
        self.hit_and_release_switch("s_grand_advance")
        self.assertEqual(2,
            self.machine.game.player.grand_counter_count)
        self.hit_and_release_switch("s_grand_hole")
        self.assertEqual(0,
            self.machine.game.player.grand_counter_count)

    def test_prix_disqualification(self):
        self._start()
        self._start_green_flag()
        self._light_grand()

        # Grand counter disabled as progress is now
        # moved to the prix counter
        self.assertEqual(False,
            self.machine.counters["grand_counter"].enabled)

        # Driver advances Prix counter a couple times
        self.hit_and_release_switch("s_prix_advance")
        self.assertEqual(1,
            self.machine.game.player.prix_counter_count)
        self.hit_and_release_switch("s_prix_advance")
        self.assertEqual(2,
            self.machine.game.player.prix_counter_count)

        # Hitting Grand Hole is safe
        self.hit_and_release_switch("s_grand_hole")
        self.assertEqual(2,
            self.machine.game.player.prix_counter_count)

        # Hitting Prix Hole disqualifies
        self.hit_and_release_switch("s_prix_hole")
        self.assertEqual(0,
            self.machine.game.player.prix_counter_count)
        self.assertEqual(False,
            self.machine.counters["prix_counter"].enabled)

        # Driver must do it all over again
        self.advance_time_and_run(1)
        self.assertEqual(True,
            self.machine.counters["grand_counter"].enabled)

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
        self.assertEqual(3,
            self.machine.ball_devices["bd_trough"].balls)

        # Mode ends
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(None,
            self.machine.multiballs["grand_prix"].enabled)

        # And wizard progress is updated
        self.assertEqual(
            1, self.machine.game.player.is_grand_prix_completed)

    def _light_grand(self):
        for i in range(5):
            self.hit_and_release_switch("s_grand_advance")
            self.assertModeRunning("green_flag")
        self.assertEqual(True,
            self.machine.counters["prix_counter"].enabled)
        self.assertEqual(False,
            self.machine.counters["grand_counter"].enabled)

    def _light_prix(self):
        for i in range(4):
            self.hit_and_release_switch("s_prix_advance")
        self.assertEqual(True,
            self.machine.counters["grand_counter"].enabled)
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
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)

        # Mult-ball light indicators on
        self.assertLightColor('l_north_advance1', 'white')
        self.assertLightColor('l_north_advance2', 'white')

