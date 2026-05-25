Pit Mode
========

    Updated 5/23/26 by unrared.

This is the base mode a game begins with on ball 1. Much of the default/global
config lives here.

![Pit Mode](https://github.com/deathsave/grand-prix/raw/main/misc/images/screens/pit.png)

Custom Pit Class
----------------

The file `./modes/pit/code/pit.py` contains some custom code.

When the `pit` mode starts:

1. All 4 segments are cleared.
1. The method `update_progress` is hooked into the event
   `player_pit_eternal_tick` handling the indication of state on playfield
   inserts for common patterns.
1. Sets the `name` player variable (Juan, Deuce, etc.) per the player `number`.
1. Randomly assigns the `evil_number` for the `pure_evil` mode.

Base Functionality
------------------

- Base scoring is here from `./modes/pit/config/variable_player.yaml`.
- The `ball_start` ball save lasts 10s with a2s grace period.
- Shows for the ball save, the pit arrow, swerve and fuel are from `./modes/pit/config/show_player.yaml`.

![Fuel](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/fuel.jpeg)
![Lube](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/lube.jpeg)
![Tires](https://github.com/deathsave/grand-prix/raw/main/misc/images/art/tires.jpeg)
