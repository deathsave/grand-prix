from unittest.mock import patch
from mpfmc.config_players.sound_player import McSoundPlayer
from tests.support import death_save
from tests.support.death_save_mc_testing import DeathSaveMcTesting

class TestLuxurySound(DeathSaveMcTesting):

    def _requested(self):
        requested = []
        play = McSoundPlayer.play
        def spy(sound_player, settings, *args, **kwargs):
            requested.extend(str(sound) for sound in settings)
            return play(sound_player, settings, *args, **kwargs)
        patcher = patch.object(McSoundPlayer, "play", spy)
        patcher.start()
        self.addCleanup(patcher.stop)
        return requested

    def _start_luxury_multiball(self):
        self._start_and_expire_ball_save()
        self._start_green_flag()
        death_save._start_luxury(self)

    # A cash register under each shot's jackpot callout (and the 6th's
    # super jackpot), and coins on the pops
    def test_cash_and_coins(self):
        self._start_luxury_multiball()
        requested = self._requested()
        for switch in ["s_target_bonus", "s_hole_prix", "s_spinner"]:
            requested.clear()
            self.hit_switch_and_run(switch, 1)
            self.assertIn("cash_register", requested)
            self.assertIn("jackpot", requested)
        requested.clear()
        self.hit_and_release_switch("s_pop1")
        self.advance_time_and_run(0.1)
        self.assertIn("coins", requested)
        self.assertNotIn("green_flag_notes", requested)

    # the sounds exist (made by bin/cash)
    def test_sounds_exist(self):
        for name in ["cash_register", "coin1", "coin2", "coin3"]:
            self.assertIn(name, self.mc.sounds)
        self.assertIn("coins", self.mc.sounds)
