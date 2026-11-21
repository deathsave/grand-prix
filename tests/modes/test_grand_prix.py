from tests.support.death_save_game_testing import DeathSaveGameTesting
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

    # Shots: get back into the Grand, Prix and Backfire holes

    # Each hole holds a ball and pays a jackpot
    def test_holes_hold_balls_for_jackpots(self):
        self._start_multiball()
        self._enter("s_grand_hole")
        self.assertEqual(1, self._held())
        self.assertEqual(1, self._jackpots())
        self._enter("s_prix_hole")
        self.assertEqual(2, self._held())
        self.assertEqual(2, self._jackpots())
        self.assertEqual(1, self.machine.ball_devices["bd_grand_hole"].balls)
        self.assertEqual(1, self.machine.ball_devices["bd_prix_hole"].balls)

    # 30s without another hole ejects ONE ball (the most
    # recent), then 30s more ejects the next
    def test_hurry_up_ejects_one_ball(self):
        self._start_multiball()
        self._enter("s_grand_hole")
        self.advance_time_and_run(20)
        self._enter("s_prix_hole")
        # 30s is counted from the 2nd hole
        self.advance_time_and_run(25)
        self.assertEqual(2, self._held())
        self.advance_time_and_run(6)
        self.assertEqual(1, self._held())
        self.assertEqual(1, self.machine.ball_devices["bd_grand_hole"].balls)
        self.assertEqual(0, self.machine.ball_devices["bd_prix_hole"].balls)
        self.advance_time_and_run(30)
        self.assertEqual(0, self._held())
        self.assertEqual(0, self.machine.ball_devices["bd_grand_hole"].balls)

    # Getting back into a hole that timed out holds the ball
    # again, and every hole shares the one 30s timer
    def test_reentering_timed_out_hole(self):
        self._start_multiball()
        grand = self.machine.ball_devices["bd_grand_hole"]
        self._enter("s_grand_hole")
        self.advance_time_and_run(31)
        self.assertEqual(0, self._held())
        self.advance_time_and_run(3)
        self._enter("s_grand_hole")
        self.assertEqual(1, self._held())
        self.advance_time_and_run(20)
        self._enter("s_prix_hole")
        # 29s after the prix hole (49s after grand):
        # both still held
        self.advance_time_and_run(28)
        self.assertEqual(2, self._held())
        self.assertEqual(1, grand.balls)
        self.assertEqual(0, self._lost() - 1)
        # 30s after the prix hole: it is ejected, grand stays
        self.advance_time_and_run(2)
        self.assertEqual(1, self._held())
        self.assertEqual(1, grand.balls)

    # Going 2 -> 1 -> 2 does not pay the 2nd jackpot again
    def test_jackpots_once_per_sequence(self):
        self._start_multiball()
        self._enter("s_grand_hole")
        self._enter("s_prix_hole")
        self.assertEqual(2, self._jackpots())
        self.advance_time_and_run(31)
        self.assertEqual(1, self._held())
        # the ejected ball comes back around
        self.advance_time_and_run(3)
        self._enter("s_prix_hole")
        self.assertEqual(2, self._held())
        self.assertEqual(2, self._jackpots())

    # All 3 held: super jackpot, all ejected, sequence restarts
    def test_super_jackpot(self):
        self._start_multiball()
        score = self.machine.game.player.score
        self._enter("s_grand_hole")
        self._enter("s_prix_hole")
        self._enter("s_backfire_hole")
        self.assertEqual(3, self._jackpots())
        self.assertEqual(1, self._super_jackpots())
        self.assertGreaterEqual(self.machine.game.player.score - score,
            3 * 100000 + 500000)
        self.advance_time_and_run(3)
        self.assertEqual(0, self._held())
        for hole in ["grand", "prix", "backfire"]:
            self.assertEqual(0, self.machine. \
                ball_devices[f"bd_{hole}_hole"].balls)
        # and the sequence pays jackpots again
        self._enter("s_prix_hole")
        self.assertEqual(4, self._jackpots())

    # A drain empties every hole
    def test_drain_empties_holes(self):
        self._start_multiball()
        self._enter("s_grand_hole")
        self._enter("s_prix_hole")
        self._drain_one_ball()
        self.advance_time_and_run(3)
        self.assertEqual(0, self._held())
        self.assertEqual(0, self.machine.ball_devices["bd_grand_hole"].balls)
        self.assertEqual(0, self.machine.ball_devices["bd_prix_hole"].balls)
        self.assertModeRunning("grand_prix")
        # and the hurry up is cancelled (no further ejects)
        self.advance_time_and_run(31)
        self.assertEqual(0, self._lost())

    # Ending the multiball with a ball held ejects it
    def test_multiball_end_ejects_held_ball(self):
        self._start_multiball()
        # past the shoot again period
        self.advance_time_and_run(20)
        self._drain_one_ball()
        self.advance_time_and_run(4)
        self.assertEqual(2, self.machine.game.balls_in_play)
        self._enter("s_grand_hole")
        self.assertEqual(1, self._held())
        self._drain_one_ball()
        self.advance_time_and_run(4)
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(0, self.machine.ball_devices["bd_grand_hole"].balls)
        self.assertEqual(1, self.machine.game.balls_in_play)

    # GRAND chases 5 -> 1 and PRIX 1 -> 4 (each light staying
    # on until all go off) while the swerve lights alternate
    def test_light_shows(self):
        self._start_multiball()
        grand = [f"l_grand_0{i}" for i in range(5, 0, -1)]
        prix = [f"l_prix_0{i}" for i in range(1, 5)]
        grand_seen, prix_seen, swerve_seen = set(), set(), set()
        # sample every ~1/4 step (steps are 1s / 2.3)
        for i in range(60):
            self.advance_time_and_run(0.1)
            grand_seen.add(self._lit_prefix(grand))
            prix_seen.add(self._lit_prefix(prix))
            swerve = (self._lit("l_swerve1"), self._lit("l_swerve2"))
            self.assertNotEqual(swerve[0], swerve[1])
            swerve_seen.add(swerve)
        self.assertEqual(set(range(6)), grand_seen)
        self.assertEqual(set(range(5)), prix_seen)
        self.assertEqual(2, len(swerve_seen))

    # A hole's area stays lit while it holds a ball
    def test_held_hole_lights_stay_on(self):
        self._start_multiball()
        grand = [f"l_grand_0{i}" for i in range(1, 6)]
        prix = [f"l_prix_0{i}" for i in range(1, 5)]
        swerve = ["l_swerve1", "l_swerve2"]
        self._enter("s_grand_hole")
        self._enter("s_backfire_hole")
        prix_counts = set()
        for i in range(30):
            self.advance_time_and_run(0.1)
            for light in grand + swerve:
                self.assertTrue(self._lit(light), light)
            prix_counts.add(self._lit_prefix(prix))
        # while prix (not held) is still chasing
        self.assertEqual(set(range(5)), prix_counts)
        # the backfire ball times out: swerve back to alternating
        self.advance_time_and_run(28)
        self.assertEqual(1, self._held())
        seen = set()
        for i in range(10):
            self.advance_time_and_run(0.1)
            seen.add((self._lit("l_swerve1"), self._lit("l_swerve2")))
            for light in grand:
                self.assertTrue(self._lit(light), light)
        self.assertEqual({(True, False), (False, True)}, seen)
        # a drain ejects grand and its chase resumes
        self._drain_one_ball()
        self.advance_time_and_run(3)
        self.assertEqual(0, self._held())
        counts = set()
        for i in range(30):
            self.advance_time_and_run(0.1)
            counts.add(self._lit_prefix(grand[::-1]))
        self.assertEqual(set(range(6)), counts)

    def _lit(self, light):
        return self.machine.lights[light].get_color().rgb != (0, 0, 0)

    # How many lights are on, asserting they are on
    # in order (the first n)
    def _lit_prefix(self, lights):
        lit = [self._lit(light) for light in lights]
        n = lit.count(True)
        self.assertEqual([True] * n + [False] * (len(lights) - n), lit)
        return n

    # (the virtual platform releases the switch on eject)
    def _enter(self, switch):
        self.hit_switch_and_run(switch, 1)

    def _held(self):
        return self.machine.ball_holds["grand_prix_holes"].balls_held

    def _jackpots(self):
        return self._count("grand_prix_jackpot")

    def _super_jackpots(self):
        return self._count("grand_prix_super_jackpot")

    def _lost(self):
        return self._count("grand_prix_hole_lost")

    def _count(self, event):
        return self._event_counts.get(event, 0)

    def setUp(self):
        super().setUp()
        self._event_counts = {}
        for event in ["grand_prix_jackpot", "grand_prix_super_jackpot",
                "grand_prix_hole_lost"]:
            self.machine.events.add_handler(event,
                self._count_event, event_name=event)

    def _count_event(self, event_name, **kwargs):
        self._event_counts[event_name] = \
            self._event_counts.get(event_name, 0) + 1

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
        self._sim_grand_prix()
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

