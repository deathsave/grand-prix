from mpf.core.custom_code import CustomCode


class Flippers(CustomCode):
    # The OPP boards remember switch -> coil mappings until they
    # lose power. If MPF restarts mid-game (ctrl+x, a crash, or
    # systemctl restart) the new MPF doesn't know those mappings
    # exist, so the flippers keep working in attract.
    #
    # Turning each flipper on and straight back off when the
    # machine resets (at boot and after each game) makes MPF send
    # the "remove mapping" command, clearing anything left over.
    def on_load(self):
        self.machine.events.add_handler("machine_reset_phase_3",
            self.clear_stale_rules)

    def clear_stale_rules(self, **kwargs):
        for flipper in self.machine.flippers:
            flipper.enable()
            flipper.disable()
