from tests.death_save_mc_testing import DeathSaveMcTesting

class TestSegmentDisplays(DeathSaveMcTesting):

    def test_segment1(self):
         self.assertModeRunning("attract")
         self.assertEqual(1986,
             int(self.machine.segment_displays['segment1'].text))

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
