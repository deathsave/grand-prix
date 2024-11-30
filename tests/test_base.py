"""Tests Base Mode"""
import os

from mpf.tests.MpfGameTestCase import MpfGameTestCase

class TestBase(MpfGameTestCase):

    def get_config_file(self):
        return 'development.yaml'

    def get_machine_path(self):
        return os.path.abspath(os.path.join(
            os.path.realpath(__file__),
            os.pardir,os.pardir
        ))

    def test_scoring(self):
        self.start_game()
        v = "score"

        score = 0
        self.assertEqual(score, self.machine.game.player.score)

        self.__increment(v, "s_pop1", 10)
        self.__increment(v, "s_pop2", 10)
        self.__increment(v, "s_grooveline", 25)
        self.__increment(v, "s_qualifier1", 100)
        self.__increment(v, "s_qualifier2", 100)
        self.__increment(v, "s_qualifier3", 100)
        self.__increment(v, "s_podium_hole", 500)
        self.__increment(v, "s_prix_hole", 100)
        self.__increment(v, "s_grand_hole", 100)
        self.__increment(v, "s_spinner", 10)
        self.__increment(v, "s_grand_advance", 10)
        self.__increment(v, "s_prix_advance", 10)
        self.__increment(v, "s_podium_advance1", 10)
        self.__increment(v, "s_podium_advance2", 10)
        self.__increment(v, "s_slingshot1", 10)
        self.__increment(v, "s_slingshot2", 10)
        self.__increment(v, "s_inlane1", 25)
        self.__increment(v, "s_inlane2", 25)
        self.__increment(v, "s_outlane1", 50)
        self.__increment(v, "s_outlane2", 50)

    def __increment(self, var, switch, value):
        current_val = getattr(self.machine.game.player, var)
        value, getattr(self.machine.game.player, var)
        self.hit_and_release_switch(switch)
        self.advance_time_and_run(1)
        new_val = getattr(self.machine.game.player, var)
        self.assertEqual(
            value, new_val - current_val,
            "Expected %s, got %s" % (value, new_val - current_val)
        )
