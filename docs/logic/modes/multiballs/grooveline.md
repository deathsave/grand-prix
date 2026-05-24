Grooveline Multiball
====================

    Updated 5/24/26 by unrared.

Grooveline is built up by making laps and hitting pop bumpers.

![Grooveline Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grooveline.png)

Activation
----------

There are two ways to increment the
`lap_counter` in `./modes/green_flag/config/counters.yaml`:

- Making a lap during `green_flag` per the `logicblock_seq_lap_complete` event.
- Hitting 20 pop bumpers per `logicblock_rubbing_is_racing_counter_complete`.

Doing either increments the `grooveline_counter`. After 10 hits, the
Grooveline inserts will trace indicating multiball is ready and hitting the
`s_multiball_target` begins the mode.

![Multiball Target](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/multiball.jpeg)

Shots
-----

No shots at this time.
