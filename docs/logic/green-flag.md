Green Flag Mode
===============

    Updated 5/23/26 by unrared.

This is the primary mode activated in several ways:

1. On ball launch, hitting the `skill_backfire` skill shot from `./modes/pit/config/shots.yaml`.
1. During the `pit` mode, hitting 1 of the 3 (`s_pit_fuel`, `s_pit_lube`,
   `s_pit_tires`) switches when the other 2 are already full.
1. During the `backfire` mode per the `logicblock_backfire_counter_complete`
   event.
1. Immediately on `ball_started` for ball 2 if not having activated, yet.

Making Laps
-----------

1. Hitting the `s_spinner` activates the `loop_gate` in `./config/common/diverters.yaml` which opens the gate for 2 seconds.
1. The ball continues its travel from the top of the playfield to the left lane where it will roll over the `s_grooveline`.
1. The `seq_lap` sequence in `./modes/green_flag/config/sequences.yaml` is completed.
1. `logicblock_seq_lap_complete` adds 1 to the `lap_count` player variable.
