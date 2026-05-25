Overview
========

Running the Game
----------------

- **Development** - `bin/dev` will run both `mpf` and `mpf-mc`
  without the console GUI. It will also run `mpf monitor` so you can
  interact with it.
- **Production** - `bin/run` will run for production using the real
  hardware devices and the console GUI.
- **Test** - Run a test with `bin/test tests/test_something.py` or
  simply `bin/test` to run all tests from the `./tests` folder.

Synthesis Call outs
-------------------

We used the built-in macOS `say` command to generate these and the
"Tritik Krush" VST plugin to bit-crush them.

`say -v "Vicki" "Let's race\!" -o sounds/preload/voice/synth/player-up4.ogg`

Flowchart
---------

This is a rough idea of how things work together.

```mermaid
graph TD
  ATTRACT[/"Attract Mode"/] == press start ==> PIT[/"PIT Mode"/]
  PIT == fuel up ==> GREEN_FLAG[/"Green Flag Mode"/]
  GREEN_FLAG == make 3 laps ==> RANDOM1{"Random<br>Event"}
  GREEN_FLAG ==> IS_LAP_EVIL{"Is Lap<br>the root of<br>all Evil?"}
  GREEN_FLAG == 10 laps on 1 ball,<br>multiball target ==> GL_MODE[/"Grooveline Mode"/]
  GREEN_FLAG == 100 spins,<br>multiball target ==> LUX_MODE[/"Lap of Luxury Mode"/]
  GREEN_FLAG == grand prix sequence ==> GP_MODE[/"Grand Prix Mode"/]
  RANDOM1 == fuel ==>
    IS_NEED_PIT{"Fuel, Lube or Tires need attention?"}
  RANDOM1 == tires ==> IS_NEED_PIT
  RANDOM1 == lube ==> IS_NEED_PIT
  RANDOM1 == bad luck ==> BALL_DRAINS((("Ball Drains")))
  IS_NEED_PIT == yes ==> IS_BACKFIRE_QUALIFIED{"Backfire Qualified?"}
  IS_BACKFIRE_QUALIFIED == yes ==> BACKFIRE_MODE[/"Backfire<br>Mode"/]
  IS_BACKFIRE_QUALIFIED == no ==> PIT
  IS_LAP_EVIL == yes ==> PURE_EVIL[/"Pure Evil<br>Shows its Face"/]
  IS_LAP_EVIL == no ==> GREEN_FLAG
  PURE_EVIL == makes driver unhappy ==> IS_DISQUALIFIER_HIT{"Disqualifier Hit?"}
  IS_DISQUALIFIER_HIT{"Disqualifier Hit?"} == yes ==> GREEN_FLAG
  IS_DISQUALIFIER_HIT{"Disqualifier Hit?"} == no ==> PURE_EVIL
  BACKFIRE_MODE ==> IS_BACKFIRE_COMPLETED{"Backfire Completed?"}
  IS_BACKFIRE_COMPLETED == yes ==> GREEN_FLAG
  IS_BACKFIRE_COMPLETED == no ==> PIT
  IS_NEED_PIT == no ==> GREEN_FLAG
  GL_MODE ==> GL_MULTI("Grooveline Multiball")
  LUX_MODE ==> LUX_MULTI("Lap of Luxury Multiball")
  GP_MODE ==> GP_MULTI("Grand Prix Multiball")
  GL_MULTI == make 3 laps ==> GL_MULTI_ADD_BALL("Add a Ball")
  GL_MULTI ==>
      IS_RF_MODE_READY{"Red Line Mode Ready?"}
  LUX_MULTI ==> IS_RF_MODE_READY
  GP_MULTI ==> IS_RF_MODE_READY
  IS_RF_MODE_READY == yes ==> RF_MODE[/"Red Line<br>(Wizard) Mode"/]
  IS_RF_MODE_READY == no ==> GREEN_FLAG
  RF_MODE ==> RF_MULTI("Red Line Multiball")
```
