from mpf.core.mode import Mode

class Pit(Mode):
    PROGRESS_MAP = {
        "is_grooveline_completed": "l_signal1",
        "is_luxury_completed": "l_signal2",
        "is_grand_completed": "l_signal3",
        "is_red_line_completed": "l_signal4",
    }

    def mode_start(self, **kwargs):
        self.reset_grooveline_count()
        self.update_progress()
        self.add_mode_event_handler("player_pit_eternal_tick",
            self.update_progress)

    # Resets the grooveline counter on every ball start
    def reset_grooveline_count(self):
        player = self.machine.game.player
        if player.is_player_var('grooveline_counter_count'):
            self.machine.counters['grooveline_counter'].reset()

    # Checks and lights up the direct progress lights
    # per the PROGRESS_MAP
    def update_progress(self, **kwargs):
        player = self.machine.game.player
        for event_name, light_name in self.PROGRESS_MAP.items():
            if not player.is_player_var(event_name):
                return

            if getattr(player, event_name) == 1:
                self.machine.lights[light_name].on()
