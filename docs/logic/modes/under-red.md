Under Red (Red Flag) Mode
=========================

    Updated 11/22/26 by unrared.

A multi-car wreck: Wear and Tear's `green_flag_under_red` (5% of the random
events every 3rd lap, `./modes/green_flag/config/random_event_player.yaml`)
puts the race under a red flag. Not during a multiball (Grooveline, Lap of
Luxury, Grand Prix or Red Line), when nothing happens. `green_flag` stops on
`mode_under_red_started` (`./modes/green_flag/config/mode.yaml`), however it
started (`debug_under_red` too).

Config is all in `./modes/under_red/config/mode.yaml`.

- Green Flag stops like a pit stop, so the switches score like the pit (10)
  and the engine's back at pace.
- Topping up the resources doesn't get you out: the pit targets' `green_flag`
  (`./modes/pit/config/event_player.yaml`) checks `not mode.under_red.active`.
  Nor does Backfire: its hurry up timer doesn't start (and is stopped on
  `mode_under_red_started`, `./modes/pit/config/timers.yaml`), its sequence is
  disabled and the mode won't start under a red flag.
- The Pot Hole (the Grand hole) gets you out: `s_hole_grand_active` posts `under_red_cleared`,
  which stops the mode and starts Green Flag (with its Off the Line countdown).
- So does a drain: it stops on `ball_will_end` and doesn't restart on the next
  ball, which begins in the pit.

Display, lights and sound:

- `under_red_slide` (`./config/common/slides.yaml`): the red flag image
  (`red-flag`) with the mode name, "Red Flag", like the other mode slides.
- `./shows/under_red_chase.yaml`: the 5 pit inserts chase red north (arrow 2,
  arrow 1, fuel, lube, tires), pointing at the Pot Hole.
- `./shows/under_red_grand.yaml`: GRAND 1 and 2 alternate.
- No pit ambience (the pit plays it when Green Flag stops): Under Red blocks
  and stops it.
- A wreck (the `crash` pool: `crash1` or `crash2`, from
  `./misc/sound-originals`, with their music taken out), then the `red_flag`
  call out (synth for now) 3s into it. Then, every 20s while it's on, a
  reminder: "Pull over near the pot hole to get back to green!"
  (`red_flag_reminder`, the `under_red_reminder` timer).

Watch out: if Grand Prix's `grand_hole` lock is enabled, a Pot Hole entry
also locks the ball (a new one is fed to the shooter lane).
