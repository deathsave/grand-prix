Awareness Bonus (Extra Ball)
============================

    Updated 6/2/26 by unrared.

The bonus target doubles as an awareness bonus once "P R I X" is fully lit.

![Extra Ball](https://github.com/deathsave/grand-prix/raw/main/images/preload/extra-ball.png)

Activation
----------

### 1. P-R-I-X Lock

1. The **Advance Awareness Bonus** target `s_bonus_target` increments the 
   `prix_counter`.
1. With "P R I X" lit, additional hits to the same target reverse the sequence
   per the `awareness_counter` in `./modes/green_flag/config/counters.yaml`.
1. **Carefully** hitting the target 4 times without entering the `s_prix_hole`
   will light the Extra Ball per `./modes/pit/config/light_player.yaml`.
1. Claim the extra ball by entering the right-side inline via the
   `s_top_inlane2` switch.
