from tests.death_save_game_testing import DeathSaveGameTesting
from unittest.mock import MagicMock

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

        # TODO: doesn't put the balls onto the playfield
        # self.assertEqual(3, self.machine.playfield.balls)

    def test_reactivation(self):
        self.machine.coils["c_grand_hole"]. \
            pulse = MagicMock()
        self.machine.coils["c_prix_hole"]. \
            pulse = MagicMock()
        self.machine.coils["c_backfire_hole"]. \
            pulse = MagicMock()

        self._start_and_expire_ball_save()
        self._start_green_flag()

        # lock 2 balls
        self._qualify_grand()
        # self.hit_and_release_switch("s_shooter_lane")
        # self.advance_time_and_run(1)
        self._qualify_prix()

        # locks have not released yet
        self.assertEqual(0, self.machine. \
            coils["c_grand_hole"].pulse.call_count)
        self.assertEqual(0, self.machine. \
            coils["c_prix_hole"].pulse.call_count)
        self.assertEqual(0, self.machine. \
            coils["c_backfire_hole"].pulse.call_count)

        # getting into the backfire hole starts
        # the mode and releases the locks
        self.hit_switch_and_run("s_backfire_hole", 1)
        self.assertModeRunning("grand_prix")
        self.assertEqual(1, self.machine. \
            coils["c_grand_hole"].pulse.call_count)
        self.assertEqual(1, self.machine. \
            coils["c_prix_hole"].pulse.call_count)
        self.assertEqual(1, self.machine. \
            coils["c_backfire_hole"].pulse.call_count)
        self.assertEqual(0, self.machine. \
            multiball_locks["grand_hole"].locked_balls)
        self.assertEqual(0, self.machine. \
            multiball_locks["prix_hole"].locked_balls)
        self.assertEqual(False, self.machine. \
            ball_holds["backfire_hole"].is_full())

        # Playfield is waiting for the 3 locked balls
        self.assertEqual(3, self.machine. \
            playfields["playfield"].num_balls_requested)
        self.assertEqual(3, self.machine. \
            playfields["playfield"].available_balls)

        # TODO: Can't seem to get balls onto the playfield
        #       in this test. seems to have no issue doing
        #       so on Dev though as you can watch the device
        #       monitor and see the ball counts move from
        #       "requested"/"available" to "balls"
        # self.machine.events.post("sw_playfield_active")
        # self.advance_time_and_run(10)
        # self.assertEqual(3, self.machine. \
        #     playfields["playfield"].balls)


        # # # two balls drain
        # for i in range(2):
        #     self._drain_one_ball()
        #     self.advance_time_and_run(4)
        # self.assertEqual(1, self.machine.playfield.balls)
        # self.assertEqual(2,
        #     self.machine.ball_devices["bd_trough"].balls)

        # # Mode has ended
        # self.assertModeNotRunning("grand_prix")
        # self.assertEqual(None,
        #     self.machine.multiballs["grand_prix"].enabled)

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

        # getting back into the backfire hole
        # DOES NOT restart the mode
        self.hit_switch_and_run("s_backfire_hole", 2)
        self.assertModeNotRunning("grand_prix")

        # Can be repeated later in the game
        self._qualify_grand()
        self.assertModeNotRunning("grand_prix")
        self._qualify_prix()
        self.assertModeNotRunning("grand_prix")
        self.hit_switch_and_run("s_backfire_hole", 2)
        self.assertModeRunning("grand_prix")

    def _qualify_grand(self):
        for i in range(5):
            self.hit_and_release_switch("s_save_target")
            self.assertModeRunning("green_flag")

        # after a the next "sync", all the
        # grand inserts should be lit
        self.advance_time_and_run(3)
        for i in range(5):
            self.assertLightColor("l_grand_0{}". \
                format(i + 1), 'white')

        # Ball is held after entering the grand hole
        self.hit_switch_and_run("s_grand_hole", 1)
        self.assertEqual(False,
            self.machine.counters["grand_counter"].enabled)
        self.assertEqual(True, self.machine. \
            multiball_locks["grand_hole"].is_virtually_full)
        self.assertEqual(1, self.machine. \
            multiball_locks["grand_hole"].locked_balls)

    def _qualify_prix(self):
        for i in range(4):
            self.hit_and_release_switch("s_bonus_target")

        # after a the next "sync", all the
        # prix inserts should be lit
        self.advance_time_and_run(3)
        for i in range(4):
            self.assertLightColor("l_prix_0{}". \
                format(i + 1), 'white')

        # Ball is held after entering the prix hole
        self.hit_switch_and_run("s_prix_hole", 1)
        self.assertEqual(False,
            self.machine.counters["prix_counter"].enabled)
        self.assertEqual(True, self.machine. \
            multiball_locks["prix_hole"].is_virtually_full)
        self.assertEqual(1, self.machine. \
            multiball_locks["prix_hole"].locked_balls)

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

