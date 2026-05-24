Grand Prix Multiball
====================

    Updated 5/24/26 by unrared.

Grand Prix is primarily controlled by the mid-playfield, left and right-side
targets and kick-out holes.

![Grand Prix Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grand-prix.png)

Activation
----------

### 1. G-R-A-N-D Lock

1. During `green_flag`, hit the **Apron Saves** target `s_save_target` to build up
   the `grand_counter`.
1. With "G R A N D" lit, the `grand_hole` multiball lock is enabled per the
   `logicblock_grand_counter_complete` event.
1. Entering the `grand_hole` locks the ball there.

### 2. P-R-I-X Lock

1. Mirroring "G-R-A-N-D", the **Advance Awareness Bonus** target `s_bonus_target`
increments the `prix_counter`.
1. With "P R I X" lit, the `prix_hole` multiball lock is enabled per the
   `logicblock_prix_counter_complete` event.
1. Entering the `prix_hole` locks the ball there.

### 3. Backfire Lock

![Backfire Hole](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/backfire.jpeg)

Unlike the other multiball modes, Grand Prix Multiball begins with the
`balldevice_bd_backfire_hole_ball_entered` event in
`modes/pit/config/event_player.yaml` conditionally firing
`grand_prix_multiball_ready` based on the state of both the counters and
locks described above.

Shots
-----

No shots at this time.
