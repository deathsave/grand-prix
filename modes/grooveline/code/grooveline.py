from mpf.core.mode import Mode

class Grooveline(Mode):
    # Shots: the left side of the playfield. The top
    # Grooveline insert, the multiball lamp and the top Grand
    # insert blink, marking the shots:
    #
    # - s_grooveline (the Grooveline lane)
    # - s_target_multiball
    # - s_hole_grand or s_target_save (the Grand area)
    #
    # Every hit on any of them pays a jackpot that grows with
    # each hit, and lights the next Grooveline insert from the
    # bottom (l_grooveline10) up. The 10th hit lights the top
    # one and pays only the super jackpot, which completes the shots
    # and bumps the multiplier (1X -> 2X -> 5X) for the rest of
    # the multiball: the 30s multiplier timer is stopped (see
    # is_grooveline_boosted in the Pit mode's timers.yaml and
    # variable_player.yaml) and it goes back to 1X when the
    # mode ends.
    SWITCHES = [
        "s_grooveline",
        "s_target_multiball",
        "s_hole_grand",
        "s_target_save",
    ]
    BLINKING = [ "l_grooveline01", "l_multiball", "l_grand1" ]
    INSERTS = [ f"l_grooveline{i:02}" for i in range(1, 11) ]
    HITS = len(INSERTS)
    JACKPOT = 30000
    JACKPOT_GROWTH = 5000
    LIGHT_KEY = "grooveline_shots"
    MULTIPLIER_BUMPS = { 1: 2, 2: 5 }

    def mode_start(self, **kwargs):
        self.hits = 0
        self.blinks = []
        for switch in self.SWITCHES:
            self.add_mode_event_handler(
                f"{switch}_active", self.shot_hit)
        self.update_lights()

    def mode_stop(self, **kwargs):
        player = self.machine.game and self.machine.game.player
        if player and player.is_grooveline_boosted:
            player.is_grooveline_boosted = 0
            player.multiplier = 1
        self.stop_blinking()
        for name in self.INSERTS + self.BLINKING:
            self.machine.lights[name].remove_from_stack_by_key(
                self.LIGHT_KEY)

    def shot_hit(self, **kwargs):
        if self.hits >= self.HITS:
            return
        self.hits += 1
        # (the last hit is only the super jackpot)
        if self.hits == self.HITS:
            self.machine.events.post("grooveline_super_jackpot")
            self.bump_multiplier()
        else:
            self.machine.events.post("grooveline_jackpot",
                hits=self.hits,
                value=self.JACKPOT + self.JACKPOT_GROWTH * (self.hits - 1))
        self.update_lights()

    # The inserts lit so far (from the bottom), over the
    # Grooveline progress lit by the Pit mode
    def update_lights(self):
        priority = self.priority + 10
        for i, name in enumerate(reversed(self.INSERTS)):
            light = self.machine.lights[name]
            light.remove_from_stack_by_key(self.LIGHT_KEY)
            if i < self.hits:
                light.on(priority=priority, key=self.LIGHT_KEY)
            elif name not in self.BLINKING:
                light.off(priority=priority, key=self.LIGHT_KEY)
        if self.hits >= self.HITS:
            self.stop_blinking()
        elif not self.blinks:
            self.blinks = [
                self.machine.shows["lights_blink"].play(
                    show_tokens={ "lights": name },
                    priority=priority + 1, speed=4)
                for name in self.BLINKING ]

    def bump_multiplier(self):
        player = self.machine.game.player
        player.is_grooveline_boosted = 1
        player.multiplier = self.MULTIPLIER_BUMPS.get(
            player.multiplier, player.multiplier)
        self.machine.events.post("grooveline_multiplier_bumped")

    def stop_blinking(self):
        for show in self.blinks:
            show.stop()
        self.blinks = []
