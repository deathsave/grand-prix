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

- Activated when fuel, lube, and tires reach max level
- Top left gate opens allowing a counter-clockwise orbit
- Each orbit increases the lap counter and adds to the bonus
- 3 successful orbits:
  - Causes a random event
  - Awards a bonus (TODO)

### Backfire Pops

When exiting green flag mode to pit, the drivers
engine may "backfire". Hit the spinner, then enter
the backfire hole to activate a hurry up. Hit the
pop bumpers to collect points while the engine "pops".

TODO:

- Each consecutive pop bumper hit increases
  linearly increasing the current bumpers
  value by 10% up to a maximum TBD
- If max is reached in time, immediately return player
  to green flag (fuel, lube and tires are max)

Special Modes
-------------

There are 3 special modes which build up to activation of the
4th, pseudo-wizard mode.

### Grooveline 1/3 (CYAN)

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

### Lap of Luxury 2/3 (MAGENTA)

"Spinning" a (very high - TBD) number of times during Green Flag
across multiple balls will eventually max out the bonus, lighting all inserts in the North-East chain and qualifying the "Lap of Luxury". Hit the multiball target to being Luxury Multiball. 6 shots award higher scoring and a bonus if completed.

### Grand Prix 3/3 (HOT PINK)

It's the name of the game!

- Top-most 5 inserts in South-West chain spells out G-R-A-N-D
- Top-most 4 inserts in South-East chain spells out P-R-I-X
- Left standing target lights a GRAND insert
- After lighting all of GRAND, entering the hole locks a ball,
  completes GRAND and enables PRIX
- Right standing target lights a PRIX insert
- Afer lighting all 4 of PRIX, entering the hole locks a ball,
  completes PRIX and lights the multiball insert
- Hit the multiball target to start grand prix multiball
  - Add a ball up to 3 times by getting into any hole, exclusive
  - Lights THIRD of the 4 traffic signal inserts

#### Red Line (Wizard Mode)

Once 3/4 traffic signals are lit, the fourth will begin flashing
in red color. The player then only needs to lock a ball in ANY of
the 3 holes to activate Red Line Multiball.

- Constant multi-ball for 60 seconds - all balls returned
- Player needs to hit every switch on the playfield to
  complete the mode
- Mode continues until all the extra balls drain or up to
  another 50 seconds when the song completes
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

### Music

#### Shipped

- "The Distance" by Cake (Attract Mode)
- "Shake your Groove Thing" by Peaches & Herb (Grooveline Mode)
- "302 Cubic Inch V8 Powered Blues" by Zeke (Red Line Mode)

#### TODO

- Blinding Lights - The Weeknd (Green Flag Mode)
- Glamorous - Fergie (Luxury Mode)
- "The Beautiful People" by Marilyn Manson (Chimebox / End of Ball Bonus)

#### Undecided

- GAME OVER
- Backfire Mode (Back Street's Back)

#### Other/Miscellaneous

- Rev Match (rev sfx)
- PIT (automotive repair sounds)
