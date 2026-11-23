from mpf.modes.credits.code.credits import Credits


class GrandPrixCredits(Credits):
    # After toggling free play (start + a flipper held 2s, see
    # config/common/combo_switches.yaml), the start button doesn't start
    # a game (or add a player) for a few seconds: attract starts a game
    # when start is let go, so letting go of the combo would start one
    TOGGLE_BLOCK_SECS = 5

    def mode_start(self, **kwargs):
        self.toggled_at = None
        super().mode_start(**kwargs)
        self.add_mode_event_handler("request_to_start_game",
            self._blocked_after_toggle)
        self.add_mode_event_handler("player_add_request",
            self._blocked_after_toggle)

    def toggle_credit_play(self, **kwargs):
        self.toggled_at = self.machine.clock.get_time()
        super().toggle_credit_play(**kwargs)

    def _blocked_after_toggle(self, **kwargs):
        if self.toggled_at is not None and \
                self.machine.clock.get_time() - self.toggled_at < \
                self.TOGGLE_BLOCK_SECS:
            self.info_log("Start blocked: free play was just toggled.")
            return False
        return True

    # MPF's credits mode only works out the credit units (how many
    # quarters make a game) and the pricing tiers when it starts in
    # credit play. Switching from free play to credit play later
    # left them unset: games started without coins and a coin
    # divided by zero. So they're worked out every time credit play
    # is turned on.
    def enable_credit_play(self, post_event=True, **kwargs):
        self._calculate_credit_units()
        self._calculate_pricing_tiers()
        super().enable_credit_play(post_event=post_event, **kwargs)
