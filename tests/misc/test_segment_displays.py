from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestSegmentDisplays(DeathSaveMcTesting):

    def test_segment1(self):
        self._attract_show_plays()

        ## game begins and puts player1's score
        ## on the segment display
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)
        self.assertModeRunning("pit")

        self.assertEqual(self.machine.game.player.score,
            int(self.machine.segment_displays['segment1'].text))

        ## player scores 10 points by hitting the
        ## grand advance switch scoring 10 points
        self.hit_and_release_switch("s_target_save")
        self.advance_time_and_run(1)
        self.assertEqual(10,
            int(self.machine.segment_displays['segment1'].text))

    def test_clearing(self):
        self.assertModeRunning("attract")
        self.advance_time_and_run(10)
        self.assertEqual(1986,
            int(self.machine.segment_displays['segment1'].text))
        self.assertEqual(15,
            int(self.machine.segment_displays['segment2'].text))
        self.assertEqual(50,
            int(self.machine.segment_displays['segment3'].text))
        self.assertEqual(1337,
            int(self.machine.segment_displays['segment4'].text))

        # game starts
        self.hit_and_release_switch("s_start")
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)

        # player 1's score is on segment1
        self.assertEqual(self.machine.game.player.score,
            int(self.machine.segment_displays['segment1'].text))

        # other segments are cleared
        self.assertEqual("       ",
            self.machine.segment_displays['segment2'].text)
        self.assertEqual("       ",
            self.machine.segment_displays['segment3'].text)
        self.assertEqual("       ",
            self.machine.segment_displays['segment4'].text)

    def test_subsequent_game(self):
        self._attract_show_plays()

        # start a game
        self._start()

        # play through all the balls
        for i in range(3):
            self.assertEqual(i + 1, self.machine.game.player.ball)
            self.hit_and_release_switch("s_shooter_lane")
            self.hit_and_release_switch("s_activate_playfield")
            self._expire_ball_save()
            # drain (no bonus to wait out)
            self.hit_switch_and_run("s_trough1", 2)

        # advance through the match mode (the 6s spin, and the scores
        # back for a second, or 2 if it matched)
        self.assertModeRunning("match")
        self.advance_time_and_run(9)

        # back to Attract mode
        self.assertModeRunning("attract")

        self._attract_show_plays()
        self.advance_time_and_run(5)

    # waits (up to `within` seconds) for the display to show a number
    def _assert_shows(self, number, display, within=3):
        for i in range(int(within / 0.1)):
            text = str(self.machine.segment_displays[display].text).strip()
            if text == str(number):
                return
            self.advance_time_and_run(0.1)
        self.fail(f"{display} never showed {number} (it shows {text!r})")

    # the attract messages, in order, then the top 4 high scores
    def _attract_show_plays(self):
        self.assertModeRunning("attract")
        self._assert_shows(1986, "segment1")
        self._assert_shows(15, "segment2")
        self._assert_shows(50, "segment3")
        self._assert_shows(1337, "segment4")
        for n in range(1, 5):
            self._assert_shows(self.machine.variables.get_machine_var(
                f"score{n}_value"), f"segment{n}")

    def test_two_players(self):
        self._start()
        # add another player
        self.hit_and_release_switch("s_start")
        self.assertEqual(1, self.machine.game.player.number)
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_pop1")

        self.assertEqual(10,
            int(self.machine.segment_displays['segment1'].text))
        self.assertEqual(0,
            int(self.machine.segment_displays['segment2'].text))

        self._expire_ball_save()
        # Driver 1 ball drains
        self._drain_one_ball()

        # wait out bonus
        self.advance_time_and_run(18)

        # Next driver's turn
        self.assertEqual(2, self.machine.game.player.number)

        self.assertEqual(10,
            int(self.machine.segment_displays['segment1'].text))
        self.assertEqual(0,
            int(self.machine.segment_displays['segment2'].text))
