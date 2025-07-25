from tests.death_save_mc_testing import DeathSaveMcTesting

class TestSegmentDisplays(DeathSaveMcTesting):

    def test_segment1(self):
        self._attract_show_plays()

        ## game begins and puts player1's score
        ## on the segment display
        self.hit_and_release_switch("s_start")
        self.hit_and_release_switch("s_shooter_lane")
        self.advance_time_and_run(1)

        self.assertEqual(self.machine.game.player.score,
            int(self.machine.segment_displays['segment1'].text))

        ## player scores 10 points by hitting the
        ## grand advance switch scoring 10 points
        self.hit_and_release_switch("s_save_target")
        self.advance_time_and_run(1)
        self.assertEqual(1,
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

        # back to Attract mode
        self.assertModeRunning("attract")

        self._attract_show_plays()
        self.advance_time_and_run(5)

    def _attract_show_plays(self):
        self.assertModeRunning("attract")
        self.advance_time_and_run(1)
        self.assertEqual(1986,
            int(self.machine.segment_displays['segment1'].text))

        self.advance_time_and_run(2)
        self.assertEqual(15,
            int(self.machine.segment_displays['segment2'].text))

        self.advance_time_and_run(4)
        self.assertEqual(50,
            int(self.machine.segment_displays['segment3'].text))

        self.advance_time_and_run(2)
        self.assertEqual(1337,
            int(self.machine.segment_displays['segment4'].text))

    def test_two_players(self):
        self._start()
        # add another player
        self.hit_and_release_switch("s_start")
        self.assertEqual(1, self.machine.game.player.number)
        self.advance_time_and_run(1)
        self.hit_and_release_switch("s_pop1")

        self.assertEqual(1,
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

        self.assertEqual(1,
            int(self.machine.segment_displays['segment1'].text))
        self.assertEqual(0,
            int(self.machine.segment_displays['segment2'].text))
