Grand Prix ’86
==============

[![Grand Prix '86 Pinball](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml/badge.svg)](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml)

Strap in for Grand Prix ’86—the homebrew pinball thrill ride where speed meets spaghetti code, and every multiball is a minor miracle!

**Your quest**: fuel up, fix up, and fly through laps in Green Flag Mode, where orbit shots rack up points and sometimes even do other things yet to be determined. Smash your way through Backfire Pops for a frenzy of bumpers and “hurry ups” that may or may not hurry anything. Craving more chaos? Unlock Grooveline, Lap of Luxury, or the gloriously glitchy Grand Prix multiballs—each one lighting up inserts like a disco ball with a loose wire. Nab three traffic signals to trigger the legendary Red Line Wizard Mode, a 60-second ball-slinging spectacle that will leave you wondering what you're actually supposed to do here because we haven't written that code yet, but imagine how amazing it will be when or if we ever get around to doing so!

![Grand Prix Pinball Machine](https://github.com/deathsave/grand-prix/raw/main/misc/grand-prix-front.png)

How things are supposed to Work
-------------------------------

A day before the Pacific Northwest Pinball & Arcade Show, this game was not even flipping. Many burned up components and a hell of a lot of elbow grease later, well... there's still much to do. But she's flipping! If you've got ideas, share them with Death Save Pinball Cult.

### General Modes

#### Pit Row

> Every driver's got to pit Cole...

- Fuel up, lube up, and change the treads

#### Green-flag (Main Mode)

With a well-oiled vehicle, the race begins:

- Counter-clockwise orbit awards a lap
- A successful lap awards a Grooveline insert
- 3 laps simulates wear and tear on the vehicle

#### Backfire Pops

When exiting green flag mode for a needed pit stop, a drivers engine may "backfire just right". Hit the spinner, then enter the backfire hole within 10 seconds to activate the hurry up. Once activated, work the pop bumpers to collect big points and possibly even delay your pit stop.

### Special Modes

Three special modes build up to activation of a fourth, pseudo-wizard mode.

#### Grooveline Multiball 1/3

![Grooveline Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grooveline.png)

The fastest way around the track (the North-West chain of 10 purple inserts).

- Making a lap during Green Flag lights an insert, in sequence
  from top to bottom
- Light all 10 inserts to qualify the multiball
- Hit the multiball target to activate Grooveline Multiball
  - Add a ball by completing 3 laps within 15 seconds
  - **Mode resets progress with the conclusion of each ball**

There are no scoring bonuses here, yet. Sorry bro.

#### Lap of Luxury Multiball 2/3

![Lap of Luxury Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/luxury.png)

Crushing the Spinner during Green Flag across multiple balls will eventually max out the bonus, lighting all inserts in the North-East chain and qualifying the "Lap of Luxury". Hit the multiball target to begin Luxury Multiball.

- Collect the lit inserts earn big points
- Collecting all awards an even bigger reward

#### Grand Prix Multiball 3/3

![Grand Prix Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grand-prix.png)

It's the name of the game!

- Top-most 5 inserts in South-West chain spells out G-R-A-N-D
- Top-most 4 inserts in South-East chain spells out P-R-I-X
- Left standing target lights a GRAND insert
- After lighting all of GRAND, entering the hole:
  - Locks a ball
  - Completes GRAND
  - Enables PRIX
- Right standing target lights a PRIX insert
- Afer lighting all 4 of PRIX, entering the hole:
  - Locks a ball
  - Completes PRIX
  - Lights the multiball
- Hit the multiball target to start Grand Prix Multiball

There are no scoring bonuses here, yet. Sorry bro.

#### Red Line (Wizard Mode)

You red line and find out how deep the rabbit hole goes which right now is nowhere, but you can pat yourself on the back for having come this far!
