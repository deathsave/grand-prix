"""Tests Green Flag Mode"""
from tests.death_save_game_testing import DeathSaveGameTesting
import pprint

class TestBase(DeathSaveGameTesting):

    def test_scoring(self):
        score = "score"

        # Workaround to use the incandescent
        # driver for the mini coils
        self.assertLightColor('x_loop_gate', 'black')

        self.__start_green_flag()

        # Mini coils is activated making it
        # possible to complete the loop
        self.assertLightColor('x_loop_gate', 'white')

        # Green Flag Mode is about the loop
        # TODO: Count the number of loops:
        #       both continuous and in total
        self.assertIncrement(score, "s_spinner", 20 * 2)
        self.assertIncrement(score, "s_grooveline", 500 * 2)
        # Only the grooveline adds to the bonus
        self.assertIncrement("bonus", "s_grooveline", 50 * 2)

        # Other switches score normally per Base Mode
        self.assertIncrement(score, "s_pop1", 10)
        self.assertIncrement(score, "s_podium_advance1", 10)
        self.assertIncrement(score, "s_slingshot2", 10)


    def test_qualification(self):
        self.__start_green_flag()
        self.assertEqual(
            1, self.machine.game.player.level_green_flag
        )
        self.hit_and_release_switch("s_disqualifier")
        self.assertModeNotRunning("green_flag")

        # Second time around, it requires hitting two
        # qualifiers to start the mode
        self.__qualify_level_two()

        # Third time around, it requires hitting
        # all three qualifiers
        self.__qualify_final_level()

        # Further attempts function the same way,
        # requiring all 3 qualifiers to be hit
        self.__qualify_final_level()

    def __start_green_flag(self):
        self.start_game()
        self.hit_and_release_switch("s_qualifier1")
        self.advance_time_and_run(1)
        self.assertModeRunning("green_flag")

    def __qualify_level_two(self):
        self.hit_and_release_switch("s_qualifier1")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier2")
        self.assertModeRunning("green_flag")
        self.hit_and_release_switch("s_disqualifier")

    def __qualify_final_level(self):
        self.hit_and_release_switch("s_qualifier1")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier2")
        self.assertModeNotRunning("green_flag")
        self.hit_and_release_switch("s_qualifier3")
        self.assertModeRunning("green_flag")
        self.hit_and_release_switch("s_disqualifier")
