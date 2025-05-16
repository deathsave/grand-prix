from mpf.core.mode import Mode

class Pit(Mode):
    # Maps various states to corresponding lights
    # For non-bool states, the value is a tuple of the
    # light prefix and the max number in the sequence
    PROGRESS_MAP = {
        "is_grooveline_completed": "l_signal1",
        "is_luxury_completed": "l_signal2",
        "is_grand_completed": "l_signal3",
        "is_red_line_completed": "l_signal4",
        "grooveline_counter_count": [ "l_grooveline", 10 ],
        "grand_counter_count": [ "l_grand", 5 ],
        "prix_counter_count": [ "l_prix", 4 ],
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
        for state, value in self.PROGRESS_MAP.items():
            print(f"Checking {state} for {value}")
            # if not player.is_player_var(state):
            #     return

            if state.startswith("is_"):
                print(f"Syncing boolean state {state}")
                if getattr(player, state) == 1:
                    self.machine.lights[value].on()
            else:
                if not player.is_player_var(state):
                    print(f"Skipping {state} for {value}")
                    continue
                print("TODO: Syncing counter")
                # print(f"Syncing counter {state}")
                current_state = getattr(player, state)
                # print(f"Current counter state: {current_state}")
                for i in range(1, value[1] + 1):
                    light_name = f"{value[0]}_{i:0>2}"
                    if i <= current_state:
                        self.machine.lights[light_name].on()
                    else:
                        self.machine.lights[light_name].off()
