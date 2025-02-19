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
        self.hit_and_release_switch("s_grand_advance")
        self.advance_time_and_run(1)
        self.assertEqual(10,
            int(self.machine.segment_displays['segment1'].text))

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
