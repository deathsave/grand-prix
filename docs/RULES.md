Grand Prix ’86 RULES
====================

Main objective is to gas up, keep the car in good shape, and
either run up the score completing laps or qualify the Grand Prix.

Fundamental Modes
-----------------

### Pit Row (Base Mode)

Racers, on your mark...

- Top left gate is closed.
- Standard scoring described here

### Green-flag (Main Mode)

The race begins!

- Activated when fuel, oil, and tires reach max level
- Top left gate opens allowing a counter-clockwise orbit
- Each orbit increases the lap counter and adds to the bonus
- 3 successful orbits:
  - Causes a random event
  - Awards a bonus (TODO)

Special Modes
-------------

There are 3 special modes which build up to activation of the
4th, pseudo-wizard mode.

### Grooveline 1/4

The fastest way around the track (the North-West chain of 10
purple inserts).

- Making a lap during Green Flag lights an insert, in sequence
  from top to bottom
- Lighting all 10 inserts and then hitting the "disqualifer":
  - **Activates "Grooveline" Multiball!**
    - Spinner and Grooveline rollover awards 2x scoring
    - Add single ball by completing 3 laps within 15 seconds
  - Lights first of the 4 traffic signal inserts (Yellow)
- **This mode resets progress after each ball**

### Grand Prix 2/4

It's the name of the game!

- Top-most 5 inserts in South-West chain spells out G-R-A-N-D
- Top-most 4 inserts in South-East chain spells out P-R-I-X
- Left standing target lights a GRAND insert
- Right standing target un-lights a GRAND insert
- Lighting all 5 and entering the hole lights one letter of PRIX
- Hitting either the PRIX hole or standing target:
    - Resets GRAND inserts
    - Lights left side of podium insert
- Lighting all 4 of PRIX and entering hole:
  - Lights right side of podium insert
- With both sides lit, entering podium hole:
  - **Activates Grand Prix Multiball!**
    - Primary Multiball
    - Top-hole keeps ball locked. Autokicker will launch the others.
    - Add a ball up to 3 times by getting into any hole, exclusive
  - Lights THIRD of the 4 traffic signal inserts (Green)

### Rubbing is Racing "Hurry Up" 3/4

When exiting Grooveline or Grand Prix, the driver is given a
"hurry up" with a chance to reactivate the mode. This should
function more or less like "bats/rats" from "Dracula". Hit as many
switches as possible in a short amount of time...

- 30 second hurry-up with 2x scoring awarded for all switches
- If `n` (TBD) switches are hit:
  - Lights one of the 4 traffic signal inserts
  - Lights second of the 4 traffic signal inserts (Yellow)
  - When time expires, random event fires and kicks the
    player back to "Pit Row" (base mode)

#### Red-flag 4/4

Once 3/4 traffic signals are lit, the fourth will begin flashing
in red color. The player then only needs to lock a ball in ANY of
the 3 holes to activate Red-flag Multiball.

- "Music" is just a heart beat and heavy breathing
- Constant multi-ball for 30 seconds
- Mode continues for another 30 seconds where the player needs
  to hit every switch on the playfield to complete the mode
- Each shot should play a random "wrecking/crash" sound from
  the pool and sound the chimebox

Other Modes / Functionalities
-----------------------------

### End of Ball Bonus

- Pulses chimebox in time with music equal to lit
  letters, turning them off with each group (throwback)
  and is followed by "There's no time to discriminate
  Hate every motherfucker That's in your way"
- Bonus inserts lit by spinner
  - Every `n` spins lights 1/10 of the bonus inserts in sequence
    - (experiment with how many spins a typical ball gets)
  - Lighting the last insert locks in the first, second and so on
- Bonus calculated by:
  - Lit Bonus insert * (Number of lit traffic signals)

### Tilt

- Sound clip: "Hey, you, are you trying to be mean?"

### Disqualifier

- Hitting the central-right drop target will remove one unit
  of "progress" from each mode (or some modes - TBD)

### Music Thoughts:

- "No Particular Place to Go" by Chuck Berry (Green Flag)
- "The Distance" by Cake
- "Highway to the Danger Zone" by Kenny Loggins
- "Mach 5" by The Presidents of the United States of America
- "Shake your Groove Thing" by Peaches & Herb
- "302 Cubic Inch V8 Powered Blues" by Zeke
- "The Beautiful People" by Marilyn Manson (Chimebox)
