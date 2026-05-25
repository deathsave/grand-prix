Pure Evil Mode
==============

    Updated 5/25/26 by unrared.

This mode is a random problem the player needs to deal with.

![Pure Evil Mode](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/pure-evil.jpeg)

Activation
----------

The file `./modes/pit/code/pit.py` contains custom code which sets
`self.machine.game.player.evil_number` to a random number between the current
value of the player variable `lap_count` and the current `ball` times 10. So
on a player's second ball with 3 laps completed, this value will be between
3 and 20. On the `logicblock_seq_lap_complete` event, the `evil_number` is
compared to `lap_count` and on a match, the event `pure_evil_enters` is
emitted beginning the mode.

Function
--------

With the mode running, `./modes/pure_evil/config/mode.yaml` subscribes to
to the `timer_eternal_tick` event. Each second, 1% of the players current
score is removed.

Deactivation
------------

1. The `s_disqualifier` switch (drop target).
1. A ball ending via the `ball_will_end` event.
1. The `pure_evil_exits` event (currently only for dev use).
