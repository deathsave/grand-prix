from mpfmc.tests.FullMpfMachineTestCase import FullMachineTestCase

class TestDisplays(FullMachineTestCase):

    def test_game_loop(self):
        self.assertModeRunning("attract")

        # TODO: decide what to display on the segments
        #       during the attract mode
        widgets = self._get_display_text_widgets()
        self.assertIn(
            "1234567", [x.text for x in widgets]
        )

        # game begins and puts player1's score
        # on the segment display
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(1)

        widgets = self._get_display_text_widgets()
        self.assertIn(
            self.machine.game.player.score,
            [int(x.text) for x in widgets]
        )

        # start game and player scores 10 points
        # by hitting the grand advance switch
        self.hit_and_release_switch("s_shooter_lane")
        self.hit_and_release_switch("s_grand_advance")
        self.advance_time_and_run(4)
        widgets = self._get_display_text_widgets()
        self.assertIn(10, [int(x.text) for x in widgets])

    #############
    ## Helpers ##
    #############

    def _get_display_text_widgets(self):
        current_widgets = []
        for wgt in self.mc.displays['apron'].current_slide.widgets:
            if hasattr(wgt.widget, 'text'):
                current_widgets.append(wgt.widget)
        return current_widgets
