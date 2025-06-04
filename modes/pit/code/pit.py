from mpf.core.mode import Mode

class Pit(Mode):
    # Maps various states to corresponding lights
    #
    # - For boolean states, the value is the light name
    # - For multi-value states, the values appear in
    #   descending order following the first value which
    #   is the target light name
    # - For sequential counters, the value is a tuple of the
    #   light prefix and the max number in the sequence
    PROGRESS_MAP = {
        "is_grooveline_completed": "l_signal1",
        "is_luxury_completed": "l_signal2",
        "is_grand_completed": "l_signal3",
        "is_red_line_completed": "l_signal4",
        "grooveline_counter_count": [ "l_grooveline", 10 ],
        "luxury_counter_count": [ "l_spinner", 10 ],
        "grand_counter_count": [ "l_grand", 5 ],
        "prix_counter_count": [ "l_prix", 4 ],
        "multiplier": [ "l_multiplier", 3 ],
        "level_tires": [
            "l_pit_tires", "red", "magenta", "lime",
        ],
        "level_lube": [ "l_pit_lube", "red", "orange","cyan" ],
        "level_fuel": [ "l_pit_fuel", "red", "pink", "aqua" ]
    }

    index = 0

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
        for i, light in enumerate(self.machine.lights.values()):
            print("****************************************")
            print(f"Light {i}: {light.name}")
            print(light.hw_drivers.values())
            print("****************************************")
            light.off()
            if self.index >= len(self.machine.lights):
                self.index = 0
            if i == self.index:
                light.on()
                print(light.hw_drivers.values())
                self.index = i + 1
                break
            # print("****************************************")
            # print(f"Light {i}: {val}")
            # print("****************************************")
        # for state, value in self.PROGRESS_MAP.items():
        #     if state.startswith("is_"):
        #         self.handle_bool(state, value)
        #     elif state.startswith("level_"):
        #         self.handle_multi_value(state, value)
        #     else:
        #         self.handle_sequential_counter(state, value)

    def handle_bool(self, state, light_name):
        player = self.machine.game.player
        if getattr(player, state) == 1:
            self.machine.lights[light_name].on()
        else:
            self.machine.lights[light_name].off()

    def handle_multi_value(self, state, values):
        player = self.machine.game.player
        current_state = getattr(player, state)
        light_name = values[0]
        self.machine.lights[light_name]. \
            color(values[current_state + 1])

    def handle_sequential_counter(self, state, value_tuple):
        player = self.machine.game.player
        current_state = getattr(player, state)
        for i in range(1, value_tuple[1] + 1):
            light_name = f"{value_tuple[0]}_{i:0>2}"
            if i <= current_state:
                self.machine.lights[light_name].on()
            else:
                self.machine.lights[light_name].off()
