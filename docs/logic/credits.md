Credits
=======

    Updated 11/22/26 by unrared.

MPF's built-in `credits` mode (in `./config/common/modes.yaml`), set up in
`./config/common/credits.yaml`:

- The coin mech (`s_credit`) takes quarters: 50 cents a game, 3 for a dollar,
  up to 30 credits.
- Free play is the default. Start + the left flipper (the switch tagged
  `left_flipper`), held 2s, toggles between free play and credit play
  (`free_play_toggle` in `./config/common/combo_switches.yaml`, which posts
  `toggle_credit_play`). MPF saves it (the `free_play` setting), so it survives
  a restart. (Start + the right flipper is still the shutdown combo.)
- The display says CREDIT PLAY or FREE PLAY when it toggles, and INSERT COINS
  when start is pressed without enough.
- A coin shows `credits_slide` (the credits over the dimmed splash, the
  pricing and PRESS START) until 5s after the last one.
- The attract splash shows FREE PLAY or CREDITS n, bottom right
  (`credits_splash`).
- `c` on the keyboard drops a quarter in (development).

`./modes/credits/code/credits.py` fixes MPF's mode: it only worked out the
credit units (quarters per game) and pricing tiers when it started in credit
play, so switching from free play left them unset (games started without
coins, and a coin divided by zero). They're worked out whenever credit play is
turned on.
