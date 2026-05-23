Multiplier
==========

    Updated 5/23/26 by unrared.

Machine Variable: multiplier  
Insert state: `./modes/pit/code/pit.py`

Activation
----------

### During Green Flag

1. Lap made. 
1. 5s `lap_to_lap` timer in `./modes/green_flag/config/timers.yaml` begins.
1. Another lap made (before timer expires).
1. `multiplier` set to `2` from `./modes/pit/config/variable_player.yaml`
   on `logicblock_seq_lap_complete`.

### During Multiball(s)

1. Multiball begins.
1. `tag_swerve` switches increment `swerve_counter` in `./modes/green_flag/config/counters.yaml`.
1. 5 `tag_swerve` switches hit.
1. `multiplier` set to `2` from `./modes/green_flag/config/variable_player.yaml` on `logicblock_swerve_counter_complete`.
