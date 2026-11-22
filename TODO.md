TODO
====

Gameplan
--------

In order, each one tested before the next:

1. Bugs and quick fixes: Red Line's reset (and its ready lamp), Pure
   Evil kept out of Red Line, Grooveline's 10s ball save, pit sounds
   only when low, flashing the low pit inserts, the cleanup items
2. Scoring: the rebalance, Backfire's multiplier step, super jackpots
   stepping the multiplier, Grand Prix's leader bonus
3. Synth callouts: required lube, Smooth Sailing, "Red flag!", the
   leader bonus
4. Under Red (red flag) mode
5. End of ball bonus: the multiball entries, only lines that were
   touched, skipping with both flippers, the results board slides
6. Chimes and shaker: super jackpot chime rolls (callout after),
   shaker pulses (multiball starts, Off the Line, Red Line heartbeat)
7. Match animation on the segment displays
8. High score: Red Line shifts category
9. Sounds: Luxury cash and coins (with the pops paying more), then the
   engine start up, idle loop and wreck once you've provided them
10. Hardware (you): the tilt / coin door / service bank, the outlane
    switches, the loop gate servo, the tach experiment, then design
    (plastics, backglass, apron card)

Design
------

- Plastics art / simple vinyl / checkered flags?
- Backbox plexi backglass
- Apron card - the rules have enough depth now that new players
  need it

Red Line
--------

- Leaving Red Line resets `is_grooveline_completed` and
  `is_grand_prix_completed` (and their signal lights). Right now they
  never reset, so once the wizard has been reached any hole entry
  restarts it for the rest of the game
  - Plan: set both to 0 on `mode_red_line_stopped`; `l_signal4`
    (`is_red_line_completed`) stays lit; test that a hole after Red
    Line doesn't restart it, and that Grooveline + Grand Prix get
    back to it
  - Luxury stays completed for the rest of the game: its chain is the
    end of ball bonus, which stays maxed (100k every ball) once
    earned. So the second run at Red Line is just the other 2
    multiballs. (Luxury is once per game already, `luxury_counter`
    never resets)
  - `red_line_counter` (lights the multiball lamp when the wizard is
    ready) counts to 3 and resets to 0 after Red Line, so with
    Luxury not counting again it would stop at 2. Drop the counter
    and light the lamp off the completed flags instead, same as the
    start condition
- Pure Evil can start during Red Line (it only checks the lap count),
  and when it ends it brings the music back to 0.3, which Red Line
  had silenced
  - Plan: keep Pure Evil out of Red Line only (add
    `not mode.red_line.active` to its start event). If the evil lap
    lands during the wizard it's skipped for that ball. It can still
    crash the other multiballs

Scoring (variable player)
-------------------------

- Backfire Mode - completing Backfire Pops steps the multiplier up
  (1x -> 2x -> 5x) and it carries into the resumed Green Flag on the
  normal 30s multiplier timer
- Grand Prix Mode - every lap during the multiball (the shot is hard)
  pays a "leader bonus" that grows linearly: 20k, 40k, 60k...
  capped at 100k from the 5th lap (with a callout and slide)
- Any super jackpot steps the multiplier up on the normal 30s timer:
  Grand Prix's super jackpot, Luxury's completion and Red Line's
  checkered flag. (Grooveline's already does, but holds it until the
  mode ends)
- Dropped: the first-time multiball multiplier bump, and the ball end
  decrement (the multiplier is always back to 1x by ball end)
- Rebalance (the ladder: pit 10 a switch < Green Flag 50-2,500 + 5k
  laps < skill shots 25k < jackpots 30k-100k < supers 250k-500k, each
  4-5x its own jackpots < Red Line):
  - Green Flag switches x5: pops / slings / spinner / targets /
    swerves 50, inlanes 150, outlanes 250, Grooveline lane and the
    Grand / Prix holes 500, Backfire hole 2,500 (still x multiplier)
  - Laps in Green Flag pay 5k x multiplier
  - Grooveline: jackpots 30k growing 5k a hit (30k-70k), super 250k
    (full run 1.31M -> 700k; it's the easiest multiball)
  - Luxury: jackpot 75k, super 300k (full run 375k -> 675k)
  - Grand Prix: keep 100k / 500k (repeatable and hardest)
  - Red Line: keep 250k x gear / 2M checkered flag
  - Off the Line 5k -> 25k (same as the ball start skill shot)
  - The multiplier applies to regular jackpots too (Grooveline,
    Luxury, Grand Prix, Red Line shifts); supers stay flat
  - High score defaults 10k / 5k / 1k / 100 -> 3M / 2M / 1M / 500k
- Revisit this list after playtesting on the machine

Multiballs
----------

- Grooveline has no ball save (`shoot_again: 0s`), while Luxury has
  10s and Grand Prix 20s
  - Plan: give it 10s, like Luxury

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

- Under Red handling (`green_flag_under_red`, 5% chance every 3rd lap) -
  a multi-car wreck; the event is posted but nothing listens for it yet
  - Plan: a red flag, as its own mode. It stops Green Flag like a pit
    stop, and the switches score like the pit, but getting the
    resources doesn't get you out
  - To get out, the driver has to get into the Grand hole (which
    resumes Green Flag) or drain. It doesn't carry over to the next
    ball; they're back in the pit then
  - Lights: the 5 pit inserts chase red from `l_pit_arrow2` north up
    to `l_pit_tires` (arrow2, arrow1, fuel, lube, tires), pointing at
    the Grand hole, and `l_grand1` / `l_grand2` alternate on and off
  - Probably a wreck sound and a "Red flag!" callout (synth for now)
  - Watch out for the Grand hole lock: if Grand Prix's `grand_hole`
    lock is enabled, a Grand hole entry during Under Red would lock
    the ball as well
- Smooth Sailing (`green_flag_smooth_sailing`, 20%) is meant to be a
  nothing burger, but should get a callout or two: "Looking good",
  "Things are going smooth out there", etc.
  - Plan: 2-3 synth lines (bin/voice-callout) played at random, to be
    replaced by Steve recordings later

Sounds
------

- Engine start up sound (you provide, I trim / level / wire up)
- Idling engine loop -> sitting in shooter lane (you provide, I make
  it loop seamlessly)
- For Luxury Mode - cash and coin sounds (I synthesize)
  - a cash register "cha-ching" under the jackpot callout on each of
    the 6 shots
  - coin sounds on the pops, and the pops pay more during Luxury to
    match: 500 x multiplier (under Backfire Pops' 1k-10k climb)
- Under Red wreck sound (you provide)
- Required lube callout (`pit_required_lube`) - generate a synth voice
  for now, until there's a Steve callout
- Pit resource sounds should only play when that resource is actually
  low (`level_* < 2`), with the bell otherwise. They play on every
  pit hit now. The conditional version in
  `modes/pit/config/sound_player.yaml` never fires because the pit's
  variable_player fills the level to 2 on the same switch event, and
  MC checks the condition after that update arrives. Fix: post a
  `pit_*_filled` event from MPF when the level is low, and have both
  the fill and the sound hang off that
  - Decided: only when low, the bell otherwise

Pit
---

- After Green Flag ends for a pit stop, the needed resource's pit
  insert doesn't flash (it only does at ball start, see the TODO in
  `modes/pit/config/show_player.yaml`)
  - Plan: every resource below full flashes its pit insert until it's
    filled, at ball start too (which today only does fuel)

High Score
----------

- A Red Line category to reward the wizard: the most shifts in a game

Cleanup
-------

- `print("lights cleared")` in `modes/attract/code/attract.py` floods
  the test output
- Stale TODO comments in `modes/green_flag/config/random_event_player.yaml`
  (bad luck is done)

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
- Shaker Motor show(s)
  - Pulse when any multiball starts
  - Pulse when a lap is made (already does, on `logicblock_seq_lap_complete`
    in `modes/green_flag/config/coil_player.yaml`, along with revs and
    swerves; maybe a longer pulse)
  - Pulse on the last tick of Off the Line if the skill shot is made
  - Grooveline - pulse shaker to the music (shake your groove thing)
  - Red Line - tiny pulses in time with the heartbeat loop
- Chimebox show(s)
  - Super jackpots roll the chimes 3 times, then the voice callout
    plays after the rolls, and the super jackpot slide stays up for
    all of it (rolls + callout)
- Top-left loop gate / servo
- Wire the tilt / coin door / service switch bank
  (`config/common/switches.yaml`)
- Outlane switches - left is dead, right is intermittent
