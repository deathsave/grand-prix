from mpf.modes.credits.code.credits import Credits


class GrandPrixCredits(Credits):
    # MPF's credits mode only works out the credit units (how many
    # quarters make a game) and the pricing tiers when it starts in
    # credit play. Switching from free play to credit play later
    # (start + left flipper, see config/common/combo_switches.yaml)
    # left them unset: games started without coins and a coin
    # divided by zero. So they're worked out every time credit play
    # is turned on.
    def enable_credit_play(self, post_event=True, **kwargs):
        self._calculate_credit_units()
        self._calculate_pricing_tiers()
        super().enable_credit_play(post_event=post_event, **kwargs)
