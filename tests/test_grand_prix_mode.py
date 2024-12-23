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

        # Repeat sequence 3 more times
        for i in range(3):
            self._light_grand()
            self._light_prix()
        self.assertEqual(4,
            self.machine.game.player.grand_prix_counter_count)

        self.assertModeRunning("grand_prix")

    def test_multiball(self):
        self._start_multiball()

        # Player launches the ball
        self.hit_and_release_switch("s_shooter_lane")
        self.hit_switch_and_run("s_podium_advance2", 4)
        self.assertEqual(2, self.machine.playfield.balls)


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
        self.assertEqual(2, self.machine.playfield.balls)
        # A ball is ejected to the shooter lane
        self.assertEqual(1,
            self.machine.ball_devices["bd_trough"].balls)
        self.assertEqual(0,
            self.machine.ball_devices["bd_shooter_lane"].balls)
