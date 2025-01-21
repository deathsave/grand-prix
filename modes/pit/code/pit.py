from mpf.core.mode import Mode

class Pit(Mode):

    def mode_start(self, **kwargs):
        player = self.machine.game.player
        if player.is_player_var('grooveline_counter_count'):
            self.machine.counters['grooveline_counter'].reset()
