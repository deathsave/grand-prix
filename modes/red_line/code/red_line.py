from mpf.core.mode import Mode

class RedLine(Mode):
    # The wizard mode: rev the engine to the red line, shift, and
    # repeat up to 5th gear, then the final run for the checkered flag.
    #
    # - Rev up: every playfield switch lights one more of the 10 Rev
    #   Match lights (the tach, left to right) and plays a rev. Every
    #   10s, the tach drains one light.
    # - Red line (all 10 lit): the tach stays full and flashes and the
    #   Backfire hole is lit to shift, for as
    #   long as it takes. Until then, every other switch scores like the
    #   pit (10, see variable_player.yaml) with just the bell.
    # - Shift (the Backfire hole at the red line): the max rev, a
    #   backfire and a
    #   jackpot worth 250,000 x the gear, then up a gear and the tach
    #   empties.
    # - 5th gear: the top Grooveline, Grand and Prix inserts blink.
    #   Hitting all three (the Grooveline lane, Grand and Prix holes)
    #   is the super jackpot (the checkered flag), then back to 1st.
    #
    # The gear is shown on the signal lights (1 for 2nd ... 4 for 5th).
    # Sounds and scoring are in config (sound_player.yaml,
    # variable_player.yaml), from the events posted here.
    TACH = [ f"l_backbox_match{n}0" for n in range(1, 10) ] \
        + [ "l_backbox_match00" ]
    GEAR_LIGHTS = [ f"l_signal{n}" for n in range(1, 5) ]
    TOP_GEAR = 5
    SHIFT = "s_hole_backfire"
    SHIFT_LIGHT = "l_backfire"
    FINAL = {
        "s_grooveline": "l_grooveline01",
        "s_hole_grand": "l_grand1",
        "s_hole_prix": "l_prix4",
    }
    # (the playfield's switches: those that ring the bell, plus the
    # pit targets and the drop target)
    SWITCH_TAGS = [ "tag_bell", "pit_resource" ]
    EXTRA_SWITCHES = [ "s_disqualifier" ]
    JACKPOT = 250000
    DRAIN_MS = 10000
    LIGHT_KEY = "red_line"

    def mode_start(self, **kwargs):
        self.gear = 1
        self.tach = 0
        self.final_hits = set()
        self.blinks = {}
        self.set_redline(False)
        for switch in self.switches():
            self.add_mode_event_handler(f"{switch}_active", self.hit,
                switch=switch)
        self.delay.add(self.DRAIN_MS, self.drain, "drain")
        self.update_lights()

    def mode_stop(self, **kwargs):
        self.set_redline(False)
        for name in list(self.blinks):
            self.stop_blink(name)
        for name in self.TACH + self.GEAR_LIGHTS + [self.SHIFT_LIGHT] \
                + list(self.FINAL.values()):
            self.machine.lights[name].remove_from_stack_by_key(
                self.LIGHT_KEY)

    def switches(self):
        names = set(self.EXTRA_SWITCHES)
        for switch in self.machine.switches.values():
            if any(tag in switch.tags for tag in self.SWITCH_TAGS):
                names.add(switch.name)
        return sorted(names)

    def set_redline(self, on):
        self.redline = on
        player = self.machine.game and self.machine.game.player
        if player:
            player.red_line_at_redline = 1 if on else 0

    def hit(self, switch, **kwargs):
        if self.gear >= self.TOP_GEAR:
            self.final_run(switch)
        elif self.redline:
            if switch == self.SHIFT:
                self.shift()
            else:
                self.machine.events.post("red_line_bell")
        else:
            self.tach = min(len(self.TACH), self.tach + 1)
            self.machine.events.post("red_line_rev", tach=self.tach)
            if self.tach >= len(self.TACH):
                self.set_redline(True)
                self.machine.events.post("red_line_redline",
                    gear=self.gear)
        self.update_lights()

    def drain(self):
        if not self.redline and self.gear < self.TOP_GEAR and self.tach:
            self.tach -= 1
            self.update_lights()
        self.delay.add(self.DRAIN_MS, self.drain, "drain")

    def shift(self):
        self.set_redline(False)
        self.machine.events.post("red_line_shift", gear=self.gear,
            value=self.JACKPOT * self.gear)
        self.gear += 1
        self.tach = 0
        if self.gear >= self.TOP_GEAR:
            self.final_hits = set()
            self.machine.events.post("red_line_final_run")

    def final_run(self, switch):
        self.machine.events.post("red_line_rev", tach=len(self.TACH))
        if switch not in self.FINAL or switch in self.final_hits:
            return
        self.final_hits.add(switch)
        if len(self.final_hits) == len(self.FINAL):
            self.machine.events.post("red_line_checkered_flag")
            self.gear = 1
            self.tach = 0
            self.final_hits = set()

    def update_lights(self):
        priority = self.priority + 10
        # the tach (full in 5th gear)
        lit = len(self.TACH) if self.gear >= self.TOP_GEAR else self.tach
        for i, name in enumerate(self.TACH):
            self.set_light(name, i < lit and not self.redline, priority)
            self.blink(name, self.redline)
        # the gear
        for i, name in enumerate(self.GEAR_LIGHTS):
            self.set_light(name, i < self.gear - 1, priority)
        # shift
        self.blink(self.SHIFT_LIGHT, self.redline)
        # the final run
        final = self.gear >= self.TOP_GEAR
        for switch, name in self.FINAL.items():
            done = switch in self.final_hits
            self.set_light(name, final and done, priority)
            self.blink(name, final and not done)

    def set_light(self, name, on, priority):
        light = self.machine.lights[name]
        light.remove_from_stack_by_key(self.LIGHT_KEY)
        if on:
            light.on(priority=priority, key=self.LIGHT_KEY)
        else:
            light.off(priority=priority, key=self.LIGHT_KEY)

    def blink(self, name, on):
        if on and name not in self.blinks:
            self.blinks[name] = self.machine.shows["lights_blink"].play(
                show_tokens={ "lights": name },
                priority=self.priority + 11, speed=6)
        elif not on and name in self.blinks:
            self.stop_blink(name)

    def stop_blink(self, name):
        self.blinks.pop(name).stop()
