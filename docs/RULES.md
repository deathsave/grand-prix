Grand Prix '86
==============

[![Grand Prix '86 Pinball](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml/badge.svg)](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml)

Strap in for Grand Prix '86—the homebrew pinball thrill ride where speed meets
spaghetti code, and every multiball is a minor miracle!

**Your quest**: fuel up, fix up, and fly through laps in Green Flag Mode, where
orbit shots rack up points and sometimes even do other things yet to be
determined. Smash your way through Backfire Pops for a frenzy of bumpers and
"hurry ups" that may or may not hurry anything. Craving more chaos? Unlock
Grooveline, Lap of Luxury, or the gloriously glitchy Grand Prix multiballs—each
one lighting up inserts like a disco ball with a loose wire. Complete all three
to trigger the legendary Red Line Wizard Mode, a ball-slinging spectacle that
will leave you wondering what you're actually supposed to do here because we
haven't written that code yet, but imagine how amazing it will be when or if we
ever get around to doing so!

![Grand Prix Pinball Machine](https://github.com/deathsave/grand-prix/raw/main/misc/grand-prix-front.png)

How things are supposed to Work
-------------------------------

A day before the 2025 Pacific Northwest Pinball & Arcade Show, this game was
not even flipping. Many burned up components and a hell of a lot of elbow
grease later, well there's still much to do ...but she's flipping! If you've
got ideas, share them with Death Save Pinball Cult.

### General

Out of the gate, try to get into the Backfire Hole with a skillful plunge. This
will immediately drop the Green Flag. Otherwise, **your adventure begins in the
pit**. But don't fret, your ride is almost ready to roll. You only need to fill
up the tank (hit the Fuel target) to join the pack.

#### Skill Shots

**Backfire Skill Shot** (Ball 1 launch)

Plunge directly into the Backfire Hole on your first launch:
- Awards 25,000 points
- All pit resources (fuel, lube, tires) are maxed out
- Green Flag mode starts immediately

**Off the Line** (Under a Green Flag)

When a ball begins under a Green Flag, a chime countdown keeps you honest.
Launch the ball out of the shooter lane during the brief window at the end to
pocket an extra 5,000 points with a shit-eating grin.

#### Green-flag (Main Mode)

With a well-oiled vehicle, the race begins:

- Counter-clockwise orbit (the Grooveline switch) awards a lap and 100 points
- 10 pop bumper hits will also get you around the track
- A successful lap advances your Grooveline insert progress

Your car needs three things to "go": **fuel**, **lube**, and **tires**. Wear and tear is expected, so before long you'll find yourself back in the pit.

#### Backfire Pops

When returning to the pit, your engine may "backfire just right". After leaving
Green Flag:

- You have 10 seconds to hit the Spinner, then enter the Backfire Hole
- Once activated, work the pop bumpers — scoring starts at 1,000 points and increases by 1,000 per hit (1k, 2k, 3k... up to 10k)
- Collect 10 pop bumper hits to have a smooth pit and join the pack!

If you don't backfire, you'll need to ensure all three resources are filled
before getting back under green.

#### End of Ball Bonus

At the end of each ball, bonus is tallied and added to your score:

- **Spinner Bonus**: 10,000 points per Luxury counter step accumulated (see Lap of Luxury below)
- **Lap Bonus**: 1,000 points per lap completed during the ball
- Both bonuses are multiplied by your current multiplier

No bonus is awarded if nothing was earned that ball.

#### Multiplier

During any multiball, "Swerve" at apex of the loop to increment your
multiplier.

### Special Modes

Three special modes build up to the activation of a fourth, wizard mode.

#### Grooveline Multiball 1/3

![Grooveline Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grooveline.png)

The fastest way around the track (the North-West chain of 10 purple inserts).

- Making a lap during Green Flag lights an insert, in sequence from top to bottom
- Progress persists across balls and through pit stops within a ball
- Light all 10 inserts to qualify the multiball
- Hit the multiball target to activate Grooveline Multiball
  - Add a ball by completing 3 laps during multiball
- Activating the mode advances Red Line progress

There are no scoring bonuses here, yet. Sorry bro.

#### Lap of Luxury Multiball 2/3

![Lap of Luxury Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/luxury.png)

Crush the Spinner during Green Flag across multiple balls to max out the bonus, lighting all inserts in the North-East chain and qualifying the "Lap of Luxury".

- Every 10 Spinner hits during Green Flag advances one Luxury step
- Progress accumulates across all balls (it never resets)
- North-East bonus inserts show your progress
- Light all 10 Luxury inserts to qualify
- Hit the multiball target to begin Luxury Multiball
  - Collect the lit inserts to earn big points
  - Collecting all inserts awards an even bigger reward
- Completing the mode marks it done and advances Red Line progress

#### Grand Prix Multiball 3/3

![Grand Prix Multiball](https://github.com/deathsave/grand-prix/raw/main/images/preload/grand-prix.png)

It's the name of the game!

- Top-most 5 inserts in South-West chain spells out G-R-A-N-D
- Top-most 4 inserts in South-East chain spells out P-R-I-X
- Left standing target lights a GRAND insert (5 hits to complete)
- After lighting all of GRAND, entering the Grand Hole:
  - Locks a ball
  - Enables PRIX
- Right standing target lights a PRIX insert (4 hits to complete)
- After lighting all 4 of PRIX, entering the Prix Hole:
  - Locks a second ball
  - Lights the multiball
- Enter the **Backfire Hole** to release both locks and start Grand Prix Multiball
- Completing the mode marks it done and advances Red Line progress
- The mode can be qualified and played again after completion

There are no scoring bonuses here, yet. Sorry bro.

#### Red Line (Wizard Mode)

Complete all three special modes — Grooveline, Lap of Luxury, and Grand Prix — to qualify Red Line. Enter any hole (Grand, Prix, or Backfire) to start the mode and find out how deep the rabbit hole goes, which right now is nowhere, but you can pat yourself on the back for having come this far!

### Pure Evil

Beware the "Pure Evil" straight from James Cameron's nitemarish dreams:

- Every second costs you
- Hit the drop target to stop the bleeding
