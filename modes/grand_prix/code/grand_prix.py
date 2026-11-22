from mpf.core.mode import Mode

class GrandPrix(Mode):
    # Shots: get back into the 3 holes used to start the
    # multiball (Grand, Prix and Backfire), all held by the
    # grand_prix_holes ball_hold (see config/ball_holds.yaml).
    #
    # - Each held ball (re)starts a 30s hurry up to get into
    #   another hole. If it runs out, the most recently held
    #   ball is ejected and the hurry up restarts for any
    #   still held.
    # - A jackpot is awarded each time the number of held
    #   balls reaches a new high for the sequence (so 2 -> 1
    #   -> 2 does not pay the 2nd jackpot again), up to 2.
    # - All 3 held awards only the super jackpot, ejects them all
    #   and restarts the sequence.
    # - A drain ejects all held balls (the sequence's
    #   jackpots stay awarded).
    # - While a hole holds a ball, the lights for its area
    #   stay on (over the light shows) until it is ejected.
    # - Every lap is a leader bonus, 20k more each time up to 100k
    #   (the shot is hard).
    HOLD = "grand_prix_holes"
    HOLES = 3
    HURRY_UP_MS = 30000

    AREA_LIGHTS = {
        "bd_hole_grand": [ f"l_grand{i}" for i in range(1, 6) ],
        "bd_hole_prix": [ f"l_prix{i}" for i in range(1, 5) ],
        "bd_hole_backfire": [ "l_swerve1", "l_swerve2" ],
    }
    LIGHT_KEY = "grand_prix_held"
    LEADER_BONUS = 20000
    LEADER_BONUS_MAX = 100000

    def mode_start(self, **kwargs):
        self.jackpots = 0
        self.laps = 0
        self.add_mode_event_handler("logicblock_seq_lap_complete",
            self.lap)
        self.add_mode_event_handler(
            f"ball_hold_{self.HOLD}_held_ball", self.ball_held)
        self.add_mode_event_handler("ball_drain", self.ball_drained)

    def mode_stop(self, **kwargs):
        self.delay.remove("hurry_up")
        self.release(all=True)

    def lap(self, **kwargs):
        self.laps += 1
        self.machine.events.post("grand_prix_leader_bonus",
            laps=self.laps, value=min(self.LEADER_BONUS * self.laps,
                self.LEADER_BONUS_MAX))

    def hold(self):
        return self.machine.ball_holds[self.HOLD]

    def ball_held(self, total_balls_held, **kwargs):
        self.update_lights()
        # (all 3 is only the super jackpot)
        if self.jackpots < total_balls_held < self.HOLES:
            self.jackpots = total_balls_held
            self.machine.events.post("grand_prix_jackpot",
                holes=total_balls_held)

        if total_balls_held >= self.HOLES:
            self.delay.remove("hurry_up")
            self.jackpots = 0
            self.machine.events.post("grand_prix_super_jackpot")
            self.release(all=True)
        else:
            self.start_hurry_up()

    def start_hurry_up(self):
        self.delay.reset(self.HURRY_UP_MS, self.hurry_up_expired,
            "hurry_up")

    def hurry_up_expired(self):
        self.release()
        self.machine.events.post("grand_prix_hole_lost")
        if self.hold().balls_held > 0:
            self.start_hurry_up()

    def ball_drained(self, balls=0, **kwargs):
        if balls > 0:
            self.delay.remove("hurry_up")
            self.release(all=True)

    # Ejects the most recently held ball (or all of them)
    def release(self, all=False):
        if all:
            self.hold().release_all()
        else:
            self.hold().release_one()
        self.update_lights()

    # Lights each area whose hole is holding a ball
    # (above the mode's light shows)
    def update_lights(self):
        held = { device.name for device, balls
            in self.hold().hold_queue if balls > 0 }
        for device, lights in self.AREA_LIGHTS.items():
            for name in lights:
                light = self.machine.lights[name]
                if device in held:
                    light.on(priority=self.priority + 10,
                        key=self.LIGHT_KEY)
                else:
                    light.remove_from_stack_by_key(self.LIGHT_KEY)
