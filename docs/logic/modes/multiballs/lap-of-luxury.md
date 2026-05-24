Lap of Luxury Multiball
=======================

    Updated 5/24/26 by unrared.

Activation
----------

1. Hitting the spinner during `green_flag` increments the `spin_counter` in 
   `./modes/green_flag/config/counters.yaml` which
   is **completed at 10 spinner hits** and triggers the 
   `logicblock_spin_counter_complete` event.
1. The `luxury_counter` also in `./modes/green_flag/config/counters.yaml` 
   is incremented at this time.
1. The `luxury_qualifier` sequence shot in
    `./modes/green_flag/config/sequence_shots.yaml` comes into play after
   another 9 of these (100 total hits of `s_spinner`) when the 
   `logicblock_luxury_counter_complete` event is triggered.
1. The multiball insert will now flash and hitting the `s_multiball_target`
  begins the mode.


Shots
-----

Once activated, six areas of the playfield will blink inserts at:

- The bottom and top of the "P R I X" chain for `s_bonus_target` and `s_prix_hole`.
- The bottom of the "Bonus" chain (10,000) for `s_spinner`.
- The top of the "Grooveline" chain (top-left of playfield) for `s_grooveline`.
- The bottom and top of the "G R A N D" chain for `s_save_target` and `s_grand_hole`.

Hitting any of the individual switches awards 25,000 points per `./modes/luxury/config/variable_player.yaml`. Activating all the switches completes the mode
**awarding 250,000 points**.
