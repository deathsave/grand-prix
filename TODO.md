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
5. End of ball bonus: the multiball entries, only lines that were
   touched, skipping with both flippers, the results board slides
6. Chimes and shaker: super jackpot chime rolls (callout after),
   shaker pulses (multiball starts, Off the Line, Red Line heartbeat)
7. Match animation on the segment displays
8. High score: Red Line shifts category
9. Sounds: Luxury cash and coins (with the pops paying more)
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

End of Ball Bonus
-----------------

- Extend the bonus (it only counts Luxury progress and laps now):
  - 10k for each multiball started (its completed flag)
  - 30k for each multiball actually completed (its super jackpot);
    needs new player vars, as nothing records a super jackpot yet
  - paid every ball while the flags hold, so it builds up like the
    Luxury chain (Red Line's reset clears Grooveline's and Grand
    Prix's)
  - see the commented-out `bonus_*` vars in
    `config/common/variables.yaml`
- Make the bonus slides more appealing (they're plain text on
  black now): a race results board, each line sliding in with a
  count-up of points and a big total at the end, over the jackpots'
  pattern (mode color at 60% over a background image)
  - keep the countdown of the (up to 10) lit bonus inserts with the
    physical chime in sync with it
- Skip the bonus by pressing both flippers. Right now it's just made
  long enough for the insert countdown to finish. MPF's bonus mode
  has `hurry_up_event` / `hurry_up_delay_ms` for this; it needs a
  left + right flipper combo switch (the existing `both_flippers`
  combo is actually right flipper + start, for shutdown), and the
  insert countdown show has to jump to the end with it
- Only show bonus lines for things the player actually touched: no
  Luxury inserts lit means no main bonus line, never reaching Grand
  Prix means no Grand Prix lines, etc. (`skip_if_zero` is off for the
  current entries)

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

- For Luxury Mode - cash and coin sounds (I synthesize)
  - a cash register "cha-ching" under the jackpot callout on each of
    the 6 shots
  - coin sounds on the pops, and the pops pay more during Luxury to
    match: 500 x multiplier (under Backfire Pops' 1k-10k climb)
- Steve recordings for the synth stand-ins: required lube (`lube`),
  Smooth Sailing (`smooth_sailing`), Red flag (`red_flag`), Leader bonus
  (`leader_bonus`)

High Score
----------

- A Red Line category to reward the wizard: the most shifts in a game

Match
-----

- Animate the match on the segment displays: every digit of every
  player's score shows the rev/match number, all moving together in
  more or less the same animation (spin up and down a couple of times
  with a rev sound, then settle on `winner_number`)
- If there's a match, when the sequence finishes blink that player's
  score segments and leave the other scores on steady

Mechs
-----

- Tachometer / Voltage Meter experiment
- Shaker Motor show(s) (the spinner, multiball starts, jackpots, super
  jackpots, skill shots, replays, the Under Red crash and Backfire Pops
  shake it now)
  - Grooveline - pulse shaker to the music (shake your groove thing)
  - Red Line - tiny pulses in time with the heartbeat loop
- Chimebox show(s)
  - Super jackpots roll the chimes 3 times, then the voice callout
    plays after the rolls, and the super jackpot slide stays up for
    all of it (rolls + callout)
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
