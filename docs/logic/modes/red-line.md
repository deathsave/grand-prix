Red Line (Wizard) Mode
======================

    Updated 11/21/26 by unrared.

Red Line starts when any hole (`sw_tag_hole`) is entered with Grooveline, Lap
of Luxury and Grand Prix all completed. It's a 3 ball multiball (all the
balls) with 60s of ball save (`./modes/red_line/config/multiballs.yaml`) and
ends with the multiball.

Shots
-----

Handled by `./modes/red_line/code/red_line.py`, which posts the events the
config plays sounds and scores from:

1. **Rev up:** every playfield switch (those tagged `tag_bell` or
   `pit_resource`, plus `s_disqualifier`) lights one more of the 10 Rev Match
   lights (the tach, `l_backbox_match10` ... `l_backbox_match00`) and posts
   `red_line_rev` (the `rev` pool). Every 10s, the tach drains one light.
1. **Red line** (all 10 lit, `red_line_redline`): the tach stays full and
   blinks, the Backfire hole's light blinks, "SHIFT!" shows on the display and
   tribal drums loop (`red_line_drums`, made by `bin/drums`, reverbed) until
   the shift. The player variable `red_line_at_redline` is 1, so
   every switch but the Backfire hole scores like the pit: Green Flag's base
   scoring is multiplied by `(1 - red_line_at_redline)` and
   `./modes/red_line/config/variable_player.yaml` scores 10 (the pit targets
   keep the Pit's scoring), with just the bell (`red_line_bell`).
1. **Shift** (the Backfire hole at the red line, no time limit,
   `red_line_shift`): the max rev (`max_rev_end`), a backfire, and a **Jackpot** of 250,000 × the gear
   (with the jackpot callout and widget, like the other modes). Then up a gear
   and the tach empties. The gear is shown on `l_signal1` ... `l_signal4`
   (none in 1st, all 4 in 5th).
1. **5th gear** (`red_line_final_run`): the tach is full and the top
   Grooveline, Grand and Prix inserts blink. Hitting all three of
   `s_grooveline`, `s_hole_grand` and `s_hole_prix` is the super jackpot,
   the **Checkered Flag** (2,000,000, `red_line_checkered_flag`, "CHECKERED
   FLAG!" on the display), then it's back to 1st gear.

While revving, every switch is only a rev: `./modes/red_line/config/sound_player.yaml`
silences the other modes' switch sounds (blocking them with `nothing`).

Sound
-----

No music (`./modes/red_line/config/track_player.yaml`), just the breathing,
a heartbeat and the crowd, all reverbed and looped (see Reverb in
`../index.md`).
