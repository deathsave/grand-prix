Multiplier
==========

    Updated 5/23/26 by unrared.

The multiplier is NOT a mode, but a player variable called `multiplier`.

Activation
----------

### During Green Flag

1. Lap made. 
1. 15s `lap_to_lap` timer in `./modes/green_flag/config/timers.yaml` begins.
1. Another lap made (before timer expires).
1. `multiplier` set to `2` from `./modes/pit/config/variable_player.yaml`
   on `logicblock_seq_lap_complete`.

### During Multiball(s)

1. Multiball begins.
1. `tag_swerve` switches increment `swerve_counter` in `./modes/green_flag/config/counters.yaml`.
1. 5 `tag_swerve` switches hit.
1. `multiplier` set to `2` from `./modes/green_flag/config/variable_player.yaml` on `logicblock_swerve_counter_complete`.

The multiplier will reset back to 1 after 30s per the `multiplier` timer in `./modes/pit/config/timers.yaml`.

### Stepping Up

`multiplier_step` steps it up (1 to 2, 2 to 5, no higher) per
`step_multiplier` in `./modes/pit/code/pit.py` (set as the pit, for the 2X
callout). `./modes/pit/config/event_player.yaml` posts it for completing
Backfire Pops (`logicblock_backfire_counter_complete`, carried into the Green
Flag it resumes) and the super jackpots: `grand_prix_super_jackpot`,
`luxury_complete` (only when its shots are `claimed`: the shot group also posts
it as it starts) and `red_line_checkered_flag`. Each step restarts the 30s
timer.

### Grooveline Super Jackpot

Completing the Grooveline Multiball shots bumps the multiplier (1 to 2, or 2 to
5) per `./modes/grooveline/code/grooveline.py`. It sets `is_grooveline_boosted`,
which stops the 30s timer and keeps Green Flag stopping from resetting it, so
it lasts until the Grooveline mode ends (back to 1).

Application
-----------

- Inserts are lit per `handle_multiplier` in `./modes/pit/code/pit.py`.
- Most/all switch hit scoring and laps are multiplied per `./modes/green_flag/config/variable_player.yaml`.
- The regular jackpots are multiplied (Grooveline, Lap of Luxury, Grand Prix and
  Red Line's shifts, in their `variable_player.yaml`), the super jackpots aren't.
- The `grooveline_counter` in `./modes/green_flag/config/counters.yaml/` is incremented once more per the `multiplier_lap` event.
- The `lap_count` player variable is incremented once more per the `multiplier_lap` event in `./modes/green_flag/config/variable_player.yaml`.
