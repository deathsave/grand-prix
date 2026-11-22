import random
from mpf.core.mode import Mode

# Numbered lights: groups that reach 10 are zero padded (l_bonus01),
# smaller groups aren't (l_grand1)
def numbered_light(prefix, number, count):
    return f"{prefix}{number:02}" if count >= 10 else f"{prefix}{number}"


class Pit(Mode):
    # Maps various states to corresponding lights
    #
    # - For one off-offs, we use "_" and don't pass any arguments
    # - For boolean states, the value is the light name
    # - For multi-value states, the values appear in
    #   descending order following the first value which
    #   is the target light name
    # - For sequential counters, the value is a tuple of the
    #   light prefix and the max number in the sequence
    PROGRESS_MAP = {
        "multiplier": "_",
        "awareness": "_",
        "multiball_ready": "_",
        "is_grooveline_completed": "l_signal1",
        "is_luxury_completed": "l_signal2",
        "is_grand_prix_completed": "l_signal3",
        "is_red_line_completed": "l_signal4",
        "grooveline_counter_count": [ "l_grooveline", 10 ],
        "luxury_counter_count": [ "l_bonus", 10 ],
        "grand_counter_count": [ "l_grand", 5 ],
        "level_tires": [
            "l_pit_tires", "red", "magenta", "lime",
        ],
        "level_lube": [ "l_pit_lube", "red", "orange","cyan" ],
        "level_fuel": [ "l_pit_fuel", "red", "pink", "aqua" ]
    }

    # A low resource flashes its pit insert until it's filled
    # (and fuel also flashes its "shoot" insert)
    LOW_FLASH_SPEED = 4
    SHOOT_LIGHTS = { "level_fuel": "l_pit_shoot_fuel" }

    # when the engine start up (3.25s) crossfades into the idle (over
    # its last 0.75s, see the pit's sound_player)
    ENGINE_START_MS = 2500

    MULTIPLIER_STEPS = { 1: 2, 2: 5 }

    index = 0

    def mode_start(self, **kwargs):
        self.flashing = {}
        self.engine_started = False
        self.ball_ending = False
        self.racing = False
        self.add_mode_event_handler("s_shooter_lane_active",
            self.engine_on)
        self.add_mode_event_handler("s_shooter_lane_inactive",
            self.plunged)
        self.add_mode_event_handler("ball_will_end", self.ball_will_end)
        self.add_mode_event_handler("multiplier_step",
            self.step_multiplier)
        self.add_mode_event_handler("green_flag_dropped",
            self.race)
        self.add_mode_event_handler("mode_green_flag_stopped",
            self.pit_stop)
        self.clear_segments()

        self.update_progress()
        self.add_mode_event_handler("player_pit_eternal_tick",
            self.update_progress)

        self.machine.game.player.name = self.driver_name()

        self.machine.game.player.evil_number = random.randint( \
            self.machine.game.player.lap_count or 1,
            self.machine.game.player.ball * 10)

    def mode_stop(self, **kwargs):
        self.machine.events.post("engine_pace_off")
        for show, _ in self.flashing.values():
            show.stop()
        self.flashing = {}

    # The engine starts up when the ball first reaches the shooter
    # lane on a turn, then idles there (and goes straight to idling
    # if it's back there again, like after a ball save)
    def engine_on(self, **kwargs):
        if self.engine_started:
            self.machine.events.post("engine_idle")
            return
        self.engine_started = True
        self.machine.events.post("engine_start")
        self.delay.reset(self.ENGINE_START_MS, self.engine_idle,
            "engine_idle")

    def engine_idle(self):
        if self.machine.switches["s_shooter_lane"].state:
            self.machine.events.post("engine_idle")

    def engine_off(self, **kwargs):
        self.delay.remove("engine_idle")
        self.machine.events.post("engine_off")

    # From the plunge it's at pace around the pit, through Off the
    # Line's countdown until the green flag drops (Green Flag has its
    # own sounds from there), and back to pace when Green Flag ends
    # for a pit stop, until the ball ends
    def plunged(self, **kwargs):
        self.engine_off()
        self.pace_on()

    def race(self, **kwargs):
        self.racing = True
        self.pace_off()

    def pit_stop(self, **kwargs):
        self.racing = False
        self.pace_on()

    def pace_on(self, **kwargs):
        if not self.ball_ending and not self.racing and \
                not self.machine.switches["s_shooter_lane"].state:
            self.machine.events.post("engine_pace")

    def pace_off(self, **kwargs):
        self.machine.events.post("engine_pace_off")

    def ball_will_end(self, **kwargs):
        self.ball_ending = True
        self.engine_off()
        self.pace_off()

    # 1x -> 2x -> 5x (as the pit, for the 2x callout), on the
    # multiplier timer (see timers.yaml)
    def step_multiplier(self, **kwargs):
        player = self.machine.game.player
        stepped = self.MULTIPLIER_STEPS.get(player.multiplier)
        if stepped:
            player.set_with_kwargs("multiplier", stepped, source="pit")

    def clear_segments(self):
        self.machine.segment_displays["segment1"].add_text("")
        self.machine.segment_displays["segment2"].add_text("")
        self.machine.segment_displays["segment3"].add_text("")
        self.machine.segment_displays["segment4"].add_text("")

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
            if state == "multiplier":
                self.handle_multiplier()
            elif state == "awareness":
                self.handle_prix()
            elif state == "multiball_ready":
                self.handle_multiball_ready()
            elif state.startswith("is_"):
                self.handle_bool(state, value)
            elif state.startswith("level_"):
                self.handle_multi_value(state, value)
            else:
                self.handle_sequential_counter(state, value)

    # Lights the current multiplier and turns the others off
    #
    #   Example: handle_multiplier()
    #
    def handle_multiplier(self):
        for i in range(1, 4):
            self.machine.lights[numbered_light("l_multiplier", i, 3)].off()
        if self.machine.game.player.multiplier == 5:
            self.machine.lights["l_multiplier3"].on()
        elif self.machine.game.player.multiplier == 2:
            self.machine.lights["l_multiplier2"].on()
        else:
            self.machine.lights["l_multiplier1"].on()

    # Turns a light on or off by checking
    # the current :state (player variable) value.
    #
    #   Example:
    #       handle_bool("is_grand_prix_completed", "l_signal3")
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
        color = values[current_state + 1]
        self.machine.lights[light_name].color(color)
        low = current_state < 2
        self.flash(light_name, low, "flash_color",
            { "led": light_name, "color": color },
            self.priority + 1, self.LOW_FLASH_SPEED)
        if state in self.SHOOT_LIGHTS:
            shoot_light = self.SHOOT_LIGHTS[state]
            self.flash(shoot_light, low, "flash_color",
                { "led": shoot_light, "color": "white" },
                self.priority + 1, self.LOW_FLASH_SPEED)

    # Blinks the multiball lamp in Green Flag while a multiball is
    # ready (except Grand Prix, which starts from the holes), or
    # Red Line is (any hole starts it)
    #
    # (from here, rather than a show_player on the eternal tick,
    # which replayed the show every second and could leave the lamp
    # steady on instead of blinking)
    def handle_multiball_ready(self):
        player = self.machine.game.player
        modes = self.machine.modes
        multiball_active = any(modes[name].active for name in
            ["grooveline", "luxury", "grand_prix", "red_line"])
        red_line_ready = player.is_grooveline_completed == 1 and \
            player.is_luxury_completed == 1 and \
            player.is_grand_prix_completed == 1
        ready = modes["green_flag"].active and not multiball_active and \
            player.is_grand_prix_multiball_ready != 1 and \
            (player.is_multiball_ready == 1 or red_line_ready)
        self.flash("l_multiball", ready, "lights_blink",
            { "lights": "l_multiball" }, modes["green_flag"].priority)

    # Plays a show on a light while :on (replacing it if its tokens
    # change), or stops it
    def flash(self, light_name, on, show_name, tokens, priority,
            speed=1):
        show, playing = self.flashing.get(light_name, (None, None))
        if show and (not on or playing != tokens):
            show.stop()
            del self.flashing[light_name]
            show = None
        if on and not show:
            show = self.machine.shows[show_name].play(
                priority=priority, speed=speed, show_tokens=tokens)
            self.flashing[light_name] = (show, tokens)

    # Handles sequential counters by matching the base
    # name of the light value_tuple[0] with the
    # coorresponding player variable :state and lighting
    # up to the current value, not exceeding the maximum
    # value (value_tuple[1]).
    #
    #   Example:
    #       handle_sequential_counter("grand_counter_count",
    #           [ "l_grand", 4 ])
    #
    def handle_sequential_counter(self, state, value_tuple):
        player = self.machine.game.player
        current_state = getattr(player, state)
        for i in range(1, value_tuple[1] + 1):
            light_name = numbered_light(value_tuple[0], i, value_tuple[1])
            if i <= current_state:
                self.machine.lights[light_name].on()
            else:
                self.machine.lights[light_name].off()

    # Handles the awkward prix / awareness sequences. Prix lights
    # the inserts and Awareness (Extra Ball) turns them off.
    #
    #   Example: handle_prix()
    #
    def handle_prix(self):
        player = self.machine.game.player
        awareness_state = getattr(player, "awareness_counter_count")
        # player has extra ball lit, defer to
        # modes/green_flag/config/show_player.yaml
        if awareness_state < 4:
            if awareness_state > 0:
                for i in range(1, 5):
                    light_name = numbered_light("l_prix", i, 4)
                    if i <= awareness_state:
                        self.machine.lights[light_name].off()
            else:
                prix_state = getattr(player, "prix_counter_count")
                for i in range(1, 5):
                    light_name = numbered_light("l_prix", i, 4)
                    if i <= prix_state:
                        self.machine.lights[light_name].on()
