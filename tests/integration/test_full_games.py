from tests.support.death_save_game_testing import DeathSaveGameTesting

# Whole games, played start to finish in different ways, checking the
# game's state stays sane at every step (see _assert_sane): the balls
# are all accounted for, the player's vars are in range, modes that
# can't run together don't, the lamps match the state, and the game
# ends cleanly into attract.
#
# (Random events are off for these, as in the other tests: WEAR_AND_TEAR
# and PURE_EVIL are 0. The Racing Gods' events are posted directly)

MULTIBALLS = ["grooveline", "luxury", "grand_prix", "red_line"]
SIGNALS = {"grooveline": "l_signal1", "luxury": "l_signal2",
    "grand_prix": "l_signal3", "red_line": "l_signal4"}
BALL_DEVICES = ["bd_trough", "bd_shooter_lane", "bd_hole_grand",
    "bd_hole_prix", "bd_hole_backfire"]
TOTAL_BALLS = 3


class FullGameTesting(DeathSaveGameTesting):

    # -- the sanity check --

    def _lit(self, light):
        return self.machine.lights[light].get_color().rgb != (0, 0, 0)

    def _balls(self):
        return {name: self.machine.ball_devices[name].balls
            for name in BALL_DEVICES}

    def _assert_sane(self, step):
        machine = self.machine
        # every ball's somewhere: in a device or on the playfield. (A
        # ball just launched isn't counted on the playfield until its
        # eject's confirmed, 3s for the shooter lane, so steps wait that
        # out)
        balls = self._balls()
        self.assertEqual(TOTAL_BALLS,
            sum(balls.values()) + machine.playfield.balls,
            f"{step}: balls {balls}, playfield {machine.playfield.balls}")

        game = machine.game
        if not game:
            self.assertModeRunning("attract")
            for mode in ["pit", "green_flag", "backfire", "under_red",
                    "pure_evil", "bonus"] + MULTIBALLS:
                self.assertModeNotRunning(mode)
            self.assertEqual(TOTAL_BALLS, balls["bd_trough"], step)
            return

        modes = machine.modes
        # (the game's ending: high score entry, then the match)
        if modes["high_score"].active or modes["match"].active:
            for mode in ["pit", "green_flag", "backfire", "under_red",
                    "pure_evil"] + MULTIBALLS:
                self.assertModeNotRunning(mode)
            self.assertEqual(TOTAL_BALLS, balls["bd_trough"], step)
            return
        self.assertModeRunning("pit")
        # never racing and stopped at once
        self.assertFalse(modes["green_flag"].active
            and modes["under_red"].active, step)
        self.assertFalse(modes["green_flag"].active
            and modes["backfire"].active, step)

        for player in game.player_list:
            self.assertIn(player.multiplier, [1, 2, 5], step)
            for resource in ["fuel", "lube", "tires"]:
                self.assertIn(player[f"level_{resource}"], [0, 1, 2],
                    f"{step}: {resource}")
            for name, top in [("grooveline_counter_count", 10),
                    ("luxury_counter_count", 10),
                    ("grand_counter_count", 5),
                    ("prix_counter_count", 4)]:
                self.assertTrue(0 <= player[name] <= top,
                    f"{step}: {name} {player[name]}")
            for name in MULTIBALLS:
                self.assertIn(player[f"is_{name}_played"], [0, 1], step)
                self.assertIn(player[f"is_{name}_super"], [0, 1], step)
            self.assertIn(player.is_outlane_save_lit, [0, 1], step)
            self.assertGreaterEqual(player.score, 0, step)

        # the current player's lamps match their state (the pit
        # refreshes them every tick; shows and multiballs borrow some,
        # like Off the Line's start tree on the signals, so only when
        # the pit's is what's showing)
        player = game.player
        lamps = {light: bool(player[f"is_{name}_played"])
            for name, light in SIGNALS.items()}
        lamps["l_outlane_bottom1"] = bool(player.is_outlane_save_lit)
        for light, on in lamps.items():
            stack = self.machine.lights[light].stack
            if stack and stack[0].key == "":
                self.assertEqual(on, self._lit(light), f"{step}: {light}")

    def _settle(self, step, secs=1):
        self.advance_time_and_run(secs)
        self._assert_sane(step)

    # -- playing --

    def _plunge(self):
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_activate_playfield")
        self.advance_time_and_run(1)

    # (after any ball save's run out, so it isn't put back)
    def _drain(self, step):
        self._drain_one_ball()
        self._settle(step, 6)

    # drains the ball and waits out the bonus (and the next ball's feed)
    def _lose_ball(self, step):
        ball, number = self.machine.game.player.ball, \
            self.machine.game.player.number
        self._drain_one_ball()
        for i in range(60):
            self.advance_time_and_run(1)
            game = self.machine.game
            if not game or (game.player.ball, game.player.number) != \
                    (ball, number):
                break
        self._settle(step, 2)

    def _race(self):
        self.hit_and_release_switch("s_pit_fuel")
        self.advance_time_and_run(8)
        self.assertModeRunning("green_flag")

    def _laps(self, count):
        for i in range(count):
            self.hit_and_release_switch("s_spinner")
            self.hit_and_release_switch("s_grooveline")
            # (past the 15s quick lap window, so each counts once)
            self.advance_time_and_run(16)

    def _hit(self, switch, times=1, secs=0.5):
        for i in range(times):
            self.hit_and_release_switch(switch)
            self.advance_time_and_run(secs)

    def _hole(self, switch, secs=5):
        self.hit_switch_and_run(switch, secs)

    def _play_out(self, step):
        while self.machine.game:
            # (high score entry: wait out its initials)
            if self.machine.modes["high_score"].active:
                self._settle(f"{step}: high score")
                self.advance_time_and_run(100)
                continue
            if self.machine.modes["match"].active:
                self._settle(f"{step}: match", 5)
                continue
            if self.machine.ball_devices["bd_shooter_lane"].balls:
                self._plunge()
                self.advance_time_and_run(3)
            self._lose_ball(step)

    def _start_game(self, players=1):
        self.advance_time_and_run(10)
        self._assert_sane("attract")
        for i in range(players):
            self.hit_and_release_switch("s_start")
            self.advance_time_and_run(1)
        self.assertEqual(players, len(self.machine.game.player_list))
        self._plunge()
        self._settle("ball 1")


class TestFullGames(FullGameTesting):

    # One driver, all the way: every multiball (winning Grooveline's
    # and Luxury's, losing Grand Prix's), Red Line, then out of balls
    # and back to attract
    def test_the_whole_race(self):
        self._start_game()
        player = self.machine.game.player
        self._race()
        self._settle("racing")

        # Grooveline: 10 laps (which also fill Luxury's chain), the
        # target, 10 shots for the super. (Not the target again: with
        # Luxury qualified, that'd stack it, see test_stacked)
        self._laps(10)
        self.assertEqual(10, player.luxury_counter_count)
        self._settle("grooveline qualified")
        self._hit("s_target_multiball", secs=4)
        self.assertModeRunning("grooveline")
        self._settle("grooveline")
        for switch in ["s_grooveline", "s_target_save"] * 5:
            self._hit(switch, secs=1)
        self.assertEqual(1, player.is_grooveline_super)
        # (the Grand target 5 times: GRAND's lit, and the outlane save)
        self.assertEqual(5, player.grand_counter_count)
        self.assertEqual(1, player.is_outlane_save_lit)
        self.assertModeNotRunning("luxury")
        self._settle("grooveline won", 10)
        self._drain("grooveline down to one")
        self.assertModeNotRunning("grooveline")
        self.assertEqual(1, player.is_grooveline_played)
        self.assertEqual(1, player.multiplier)
        self._settle("after grooveline")

        # Luxury: its chain's already full, so the target, its 6 shots
        self._hit("s_target_multiball", secs=4)
        self.assertModeRunning("luxury")
        self._settle("luxury")
        for switch in ["s_target_bonus", "s_hole_prix", "s_spinner",
                "s_grooveline", "s_hole_grand", "s_target_save"]:
            self._hit(switch, secs=1)
        self.assertEqual(1, player.is_luxury_super)
        self._settle("luxury won", 6)
        self.assertModeNotRunning("luxury")
        self._drain("luxury down to one")
        self.assertEqual(1, player.is_luxury_played)
        self._settle("after luxury")

        # Grand Prix: (GRAND's lit) the Pot Hole lock, PRIX, the Oil
        # Slick lock, the Backfire Hole to start; then lose it
        self._hole("s_hole_grand")
        self._settle("grand locked")
        self._hit("s_target_bonus", 4)
        self._hole("s_hole_prix")
        self._settle("prix locked")
        self._hole("s_hole_backfire", 8)
        self.assertModeRunning("grand_prix")
        self._settle("grand prix", 25)
        self._drain("grand prix down to two")
        self._drain("grand prix down to one")
        self.assertModeNotRunning("grand_prix")
        self.assertEqual(1, player.is_grand_prix_played)
        self.assertEqual(0, player.is_grand_prix_super)
        self._settle("after grand prix")

        # Red Line: any hole, rev to the red line and shift
        self._hole("s_hole_grand", 5)
        self.assertModeRunning("red_line")
        # (its other balls launched one after another)
        self._settle("red line", 8)
        self._hit("s_spinner", 10, secs=0.1)
        self._hole("s_hole_backfire")
        self.assertEqual(1, player.shift_count)
        self._settle("shifted", 60)
        self._drain("red line down to two")
        self._drain("red line down to one")
        self.assertModeNotRunning("red_line")
        self.assertEqual(1, player.is_red_line_played)
        # (back for Grooveline and Grand Prix again; Luxury stays)
        self.assertEqual(0, player.is_grooveline_played)
        self.assertEqual(0, player.is_grand_prix_played)
        self.assertEqual(1, player.is_luxury_played)
        self._settle("after red line")

        self._play_out("playing out")
        self._settle("game over", 15)
        self.assertIsNone(self.machine.game)

    # Grooveline and Luxury qualified (10 laps fill both), then a pit
    # stop and a lost ball before the target: both still start on the
    # next ball, stacked, and both are lost early
    def test_stacked_after_a_pit_stop_and_a_drain(self):
        self._start_game()
        player = self.machine.game.player
        self._race()
        self._laps(10)
        self._settle("both qualified")
        self.post_event("pit_required_lube")
        self._settle("pit stop", 2)
        self.assertModeNotRunning("green_flag")
        self._hit("s_pit_lube", secs=8)
        self._settle("back racing")
        self._lose_ball("lost ball 1")
        self.assertEqual(2, self.machine.game.player.ball)
        self._plunge()
        self._race()
        self.assertEqual(10, player.grooveline_counter_count)
        self.assertEqual(10, player.luxury_counter_count)

        # the target: Grooveline, then (as a Grooveline shot) Luxury too
        self._hit("s_target_multiball", secs=4)
        self.assertModeRunning("grooveline")
        self.assertModeNotRunning("luxury")
        self._hit("s_target_multiball", secs=4)
        self.assertModeRunning("grooveline")
        self.assertModeRunning("luxury")
        self._settle("stacked", 15)

        # both lost early
        while self.machine.game.balls_in_play > 1:
            self._drain("losing them")
        self._settle("both over", 8)
        for name in ["grooveline", "luxury"]:
            self.assertModeNotRunning(name)
            self.assertEqual(1, player[f"is_{name}_played"])
            self.assertEqual(0, player[f"is_{name}_super"])
        self._play_out("playing out")
        self._settle("game over", 15)

    # Two players: each keeps their own progress
    def test_two_players(self):
        self._start_game(players=2)
        game = self.machine.game
        one = game.player
        self._race()
        self._laps(10)
        self._hit("s_target_save", 3)
        self.post_event("racing_gods_lucky_charm")
        self._settle("player 1's progress")
        self._lose_ball("to player 2")

        two = game.player
        self.assertEqual(2, two.number)
        self._plunge()
        self._settle("player 2's ball")
        for name in ["grooveline_counter_count", "luxury_counter_count",
                "grand_counter_count", "is_outlane_save_lit", "lap_count"]:
            self.assertEqual(0, two[name], name)
        self.assertFalse(self._lit("l_outlane_bottom1"))
        self._race()
        # (player 2's target is just a target)
        self._hit("s_target_multiball", secs=4)
        self.assertModeNotRunning("grooveline")
        self._settle("player 2 racing")
        self._lose_ball("back to player 1")

        self.assertIs(one, game.player)
        self._plunge()
        self._settle("player 1 again")
        self.assertEqual(10, one.grooveline_counter_count)
        self.assertEqual(3, one.grand_counter_count)
        self.assertEqual(1, one.is_outlane_save_lit)
        self.assertTrue(self._lit("l_outlane_bottom1"))
        self._race()
        self._hit("s_target_multiball", secs=4)
        self.assertModeRunning("grooveline")
        self._settle("player 1's grooveline", 15)
        while game.balls_in_play > 1:
            self._drain("losing it")
        self._play_out("playing out")
        self._settle("game over", 15)

    # A tilt during a multiball: the ball (all of them) ends, and the
    # next one starts clean
    def test_tilt_during_a_multiball(self):
        self._start_game()
        self._race()
        self._laps(10)
        self._hit("s_target_multiball", secs=6)
        self.assertModeRunning("grooveline")
        self._settle("grooveline", 12)
        for i in range(3):
            self._hit("s_tilt", secs=1)
        self.assertModeRunning("tilt")
        self.assertTrue(self.machine.game.tilted)
        # (the balls drain, the flippers are dead)
        while self.machine.playfield.balls:
            self._drain_one_ball()
            self.advance_time_and_run(3)
        for i in range(30):
            self.advance_time_and_run(1)
            if self.machine.game.player.ball == 2:
                break
        self._settle("after the tilt", 3)
        self.assertEqual(2, self.machine.game.player.ball)
        self.assertFalse(self.machine.game.tilted)
        self.assertModeNotRunning("grooveline")
        self._plunge()
        self.assertTrue(self.machine.flippers["left_flipper"]._enabled)
        self._settle("ball 2")
        self._play_out("playing out")
        self._settle("game over", 15)

    # The Racing Gods, good and bad: a wreck, bad luck, a safety car, a
    # lucky charm
    def test_the_racing_gods(self):
        self._start_game()
        player = self.machine.game.player
        self._race()

        # a wreck: the red flag, out through the Pot Hole
        self.post_event("green_flag_under_red")
        self._settle("red flag", 4)
        self.assertModeRunning("under_red")
        self.assertModeNotRunning("green_flag")
        self._hole("s_hole_grand")
        self._settle("back to green", 4)
        self.assertModeNotRunning("under_red")
        self.assertModeRunning("green_flag")

        # a safety car: a drain's saved
        self.post_event("racing_gods_safety_car")
        self._drain("saved by the safety car")
        self.assertEqual(1, self.machine.game.player.ball)
        self._settle("still ball 1", 3)

        # a lucky charm: an outlane kicks out another ball
        self.post_event("racing_gods_lucky_charm")
        self._settle("charmed", 20)
        self._hit("s_outlane2")
        self._settle("outlane saved", 6)
        self.assertEqual(0, player.is_outlane_save_lit)
        self._drain("the outlaned ball drains")
        self.assertEqual(1, self.machine.game.player.ball)

        # bad luck: dead flippers until the ball's over
        self.post_event("green_flag_bad_luck")
        self._settle("bad luck")
        self.assertFalse(self.machine.flippers["left_flipper"]._enabled)
        self._lose_ball("bad luck's ball over")
        self._plunge()
        self.assertTrue(self.machine.flippers["left_flipper"]._enabled)
        self._settle("ball 2")
        self._play_out("playing out")
        self._settle("game over", 15)
