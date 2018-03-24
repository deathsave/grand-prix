William’s Grand Prix
====================

Code for solid-state conversion / re-theme of the 1976 [EM Pinball Machine](http://www.ipdb.org/machine.cgi?id=1072) by William’s.


Proposed OPP Build
------------------

OPP boards can each have up to 4 wings attached as shown:

![OPP Processor Board](http://pinballmakers.com/wiki/images/f/f1/Opp-processor.png)

### Board Configs for Playfield

* **North Playfield (a):** 1 Switch, 3 Incandescent
  * 24 lamps: 20 spinner state, 2 spinner lit, 2 lane select
  * 4 switches: l/r lane selects, l/r spinners
* **North Playfield (b):** 1 Switch, 2 Solenoid, 1 Incandescent
  * 7 coils: Pop (direct fire), 2 Drops, (Top Hole on 1)
  * 7 swtiches: 1:1 with coils
  * 0 lamps: none (room to wire pop lamps or else???)
* **Central Playfield:** 2 Incandescent, 1 Solenoid, 1 Switch
  * 2 coils: Left Kicker, Left Slingshot (direct fire)
  * 14 lamps: 10 Left Bonus, 4 Stars
  * 5 swtiches: left kicker, advance, lanes (2), and sling
* **South Playfield (a):** 2 Switch, 1 Solenoid, 1 Incandescent
  * 2 coils: Left Flipper (direct fire?), trough
  * 5 switches: start button, tilt, left flips (eos+hold), trough
  * 8 lamps:
    * lane arrow lights (4), same player shoots again,
    * left special, left extra ball, credit in (apron)?
* **South Playfield (b):** 1 Switch, 1 Solenoid, 2 Incandescent
  * 3 coils: Right Kicker, Right Slingshot (direct fire), Right Flipper
  * 7 swtiches: right kicker, advance, lanes (2), sling, and flips (eos+hold)
  * 12 lamps: 10 Right Bonus, right extra ball, right special

### Board Configs for Backbox

We might be able to do communicate some/all of the gamestate stuff with the
7-segments, but it seems correct we'd only have lamps/coils in the backbox.

* **Backbox:** 3 Incandescents, 1 Solenoid
  * `n` lamps:
    * player up (4), game over (1/2), current ball (3/5),
    * match lights (10), extra ball lights (1/2)
  * 1-4 coils: knocker... (and maybe sneak the chime box in here?)

### 6 Total OPP Boards

**I/O Wings:** 6  
**Switch Wings:** 6  
**Solenoid Wings:** 6  
**Incandescent Wings:** 9 or 12 
