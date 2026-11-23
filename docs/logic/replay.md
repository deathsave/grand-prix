Replay
======

    Updated 11/22/26 by unrared.

MPF has no replay mode, so it's `./code/replay.py` (custom code, see
`./config/common/custom_code.yaml`) with `./config/common/replay.yaml`.

When a player's score passes the replay score (once a game per player, the
`replay_awarded` player var) it posts `replay_awarded`, then:

- in credit play, `replay_credit`: a free credit (`events` in
  `./config/common/credits.yaml`)
- on free play, `replay_extra_ball`: an extra ball (the pit's `replay` extra
  ball, `./modes/pit/config/extra_balls.yaml`)

with a fanfare: the chimes knock (`./shows/replay_chimes.yaml`, rolling down
twice), the "Replay!" call out (synth for now) and a gold REPLAY! overlay with
FREE GAME or EXTRA BALL for 3s.

The replay score adjusts itself. It starts at 1,500,000 and after each game
(`game_ending`):

- someone got a replay: it's 1.5x their final score (the best of them, if
  more than one did)
- 50 games in a row without one: it's halved
- rounded to the nearest 10,000, and never below 500,000

It's saved on the machine (the `replay_score` and `replay_games_without`
machine vars, `./config/common/variables.yaml`).
