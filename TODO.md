TODO
====

Gameplan
--------

In order, each one tested before the next:

1. ~~Bugs and quick fixes~~ (done: Red Line's reset and ready lamp,
   Pure Evil kept out of Red Line, Grooveline's 10s ball save, pit
   sounds only when low, flashing the low pit inserts, the cleanup)
2. ~~Scoring~~ (done: the rebalance, Backfire's multiplier step, super
   jackpots stepping the multiplier, Grand Prix's leader bonus; its
   callout is in step 3)
3. ~~Synth callouts~~ (done: required lube, Smooth Sailing, "Red
   flag!" (the `red_flag` pool, for step 4), the leader bonus)
4. ~~Under Red (red flag) mode~~ (done)
5. ~~End of ball bonus~~ (done: the multiball lines, only the lines
   that were touched, skipping with both flippers, the results board)
6. ~~Chimes and shaker~~ (done: super jackpots roll the chimes 3 times
   then the callout, with the overlay up throughout; the Red Line
   heartbeat in the shaker)
7. ~~Match animation on the segment displays~~ (done)
8. ~~High score: Red Line shifts category~~ (done: Shift Champ)
9. ~~Sounds: Luxury cash and coins (with the pops paying more)~~ (done)
10. Hardware (you): the tilt / coin door / service bank, the outlane
    switches, the loop gate servo, the tach experiment, then design
    (plastics, backglass)

Design
------

- Plastics art / simple vinyl / checkered flags?
- Backbox plexi backglass

Scoring (variable player)
-------------------------

- Revisit the numbers after playtesting on the machine

Wear and Tear
-------------

- Smooth Sailing's callouts (the `smooth_sailing` pool) are synth for
  now; replace with Steve recordings

Pit
---

- Tune Up: the left inlane (`s_inlane1`) auto fills a random low pit
  resource, with a callout

Sounds
------

- Steve recordings for the synth stand-ins: required lube (`lube`),
  Smooth Sailing (`smooth_sailing`), Red flag (`red_flag`), Leader bonus
  (`leader_bonus`)

Segment Displays
----------------

(They show 0-9, blank and blink. Every game's assumed to be 4 players,
so every display is someone's score: these only take one over
briefly)

- Off the Line start tree: during "Get Ready", all four displays count
  down together (`3333333`, `2222222`, `1111111`), then the scores come
  back on green
- Award count-ups: the big awards (jackpots, super jackpots, the end of
  ball bonus) roll the score up to its new total over about half a
  second, like an EM's reels, instead of jumping
- Pure Evil: every display but the current player's alternates `    666`,
  `666 666` and `666    ` while it runs (check on the machine that a
  blank mid-text shows as a blank digit)
- The winning score blinks at the end of a multiplayer game

Mechs
-----

- Tachometer / Voltage Meter experiment
- Shaker Motor show(s) (the spinner, multiball starts, jackpots, super
  jackpots, skill shots, replays, the Under Red crash, Backfire Pops and Red
  Line's heartbeat shake it now)
- Top-left loop gate / servo
- Wire the service switches (the tilt and coin mech on that bank work
  now; `s_service_*` are commented out in `config/common/switches.yaml`)

Hardware
--------

- `s_trough1` (0-3-26, at the trough's eject end) never changes state:
  0 changes in any session since Nov 20, still after the screw fix,
  while `s_trough2` / `s_trough3` change dozens of times a session.
  It's type NC, so an open circuit reads as "ball here" all the time.
  That throws MPF's ball count off ("Received unexpected ball" in the
  trough): an extra ball fed and auto launched, a ball ending early,
  and a black screen for up to ~40s after a game while MPF searches
  for a ball it thinks is missing. Check its wire, connector / crimp
  and the switch (or opto). Test: lift the ball off that spot in
  attract and watch the log for `s_trough1`
- The left inlane / outlane (`s_inlane1` 0-2-26, `s_outlane1` 0-2-27)
  fire together (774 times, vs 104 / 196 alone) and often with no ball,
  right after a coil fires: bridged inputs or a shared common. Until
  fixed they're not `playfield_active` (they faked launches and shut
  the loop gate); add the tag back once they're fixed
- The shooter lane switch is sensitive: it opens for 0.3-0.7s with the
  ball still in the lane (the debounce covers short bounces only)
- Segment display 4 needs solder work
- The GRAND "A" lamp (`l_grand3`, 0-1-22) probably needs its connector
  checked
- Possible bug, needs more confirmation: a player-up lamp stayed on the
  previous player into the next player's ball (seen 2026-11-22: player
  2's lamp still lit while player 3 was up, until partway through the
  ball), so it looked like the wrong player was up. The game took the
  turns in order, and the lamp is set on `ball_starting`, before the
  ball's fed (`config/common/info_lights.yaml`; checked locally). Likely
  an LED update to the second OPP board (the player-up lamps are on its
  LED chain, 1-0-40 to 43) that was dropped or late. If it happens
  again, note the time and player; to catch it, turn `opp: debug: true`
  on for a session (`config/production/xubuntu.yaml`) to log every LED
  update, then back off
