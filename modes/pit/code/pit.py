import random
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
        "luxury_counter_count": [ "l_bonus", 10 ],
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
        self.update_progress()
        self.add_mode_event_handler("player_pit_eternal_tick",
            self.update_progress)
        self.machine.segment_displays["segment1"].add_text("")
        self.machine.segment_displays["segment2"].add_text("")
        self.machine.segment_displays["segment3"].add_text("")
        self.machine.segment_displays["segment4"].add_text("")
        self.machine.game.player.name = self.driver_name()
        self.machine.game.player.evil_number = random.randint( \
            self.machine.game.player.lap_count or 1,
            self.machine.game.player.ball * 10)

    def driver_name(self):
        match self.machine.game.player.number:
            case 2:
                return "Deuce"
            case 3:
                return "Trey"
            case 4:
                return "Ford"
            case _:
                return "Juan"

    # Checks and lights up the direct progress lights
    # per the PROGRESS_MAP
    def update_progress(self, **kwargs):
        for state, value in self.PROGRESS_MAP.items():
            if state.startswith("is_"):
                self.handle_bool(state, value)
            elif state.startswith("level_"):
                self.handle_multi_value(state, value)
            else:
                self.handle_sequential_counter(state, value)

    # Turns a light on or off by checking
    # the current :state (player variable) value.
    #
    #   Example:
    #       handle_bool("is_grand_completed", "l_signal3")
    #
    def handle_bool(self, state, light_name):
        player = self.machine.game.player
        if getattr(player, state) == 1:
            self.machine.lights[light_name].on()
        else:
            self.machine.lights[light_name].off()

    # Matches the value of the tuple of [light, *values]
    # to the current :state of the player variable.
    #
    #   Example:
    #       handle_multi_value("level_foo",
    #           [ "l_foo", "red", "green", "blue" ])
    #
    def handle_multi_value(self, state, values):
        player = self.machine.game.player
        current_state = getattr(player, state)
        light_name = values[0]
        self.machine.lights[light_name]. \
            color(values[current_state + 1])

    # Handles sequential counters by matching the base
    # name of the light value_tuple[0] with the
    # coorresponding player variable :state and lighting
    # up to the current value, not exceeding the maximum
    # value (value_tuple[1]).
    #
    #   Example:
    #       handle_sequential_counter("prix_counter_count",
    #           [ "l_prix", 4 ])
    #
    def handle_sequential_counter(self, state, value_tuple):
        player = self.machine.game.player
        current_state = getattr(player, state)
        for i in range(1, value_tuple[1] + 1):
            light_name = f"{value_tuple[0]}_{i:0>2}"
            if i <= current_state:
                self.machine.lights[light_name].on()
            else:
                self.machine.lights[light_name].off()
