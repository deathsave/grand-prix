from mpf.core.mode import Mode

class Pit(Mode):

    def mode_start(self, **kwargs):
        self._reset_grooveline_count()

    # Resets the grooveline counter on every ball start
    def _reset_grooveline_count(self):
        player = self.machine.game.player
        if player.is_player_var('grooveline_counter_count'):
            self.machine.counters['grooveline_counter'].reset()
