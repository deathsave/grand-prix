from mpf.core.custom_code import CustomCode


class Replay(CustomCode):
    # A replay: when a player's score passes the replay score, they get
    # one (once a game): a free credit in credit play, or an extra ball
    # on free play, with a fanfare (see config/common/replay.yaml).
    #
    # The replay score adjusts itself after each game: when someone got
    # a replay, it's 1.5x their final score (the best of them), and
    # after 50 games in a row without one, it's halved. It's saved on
    # the machine (the replay_score machine var, see
    # config/common/variables.yaml).
    START = 1500000
    RAISE = 1.5
    GAMES_BEFORE_HALVING = 50
    # (never below this, and rounded to the nearest 10k)
    MIN = 500000
    ROUND_TO = 10000

    def on_load(self):
        self.machine.events.add_handler("player_score", self.score_changed)
        self.machine.events.add_handler("game_ending", self.adjust)

    def replay_score(self):
        return self.machine.variables.get_machine_var("replay_score") \
            or self.START

    def score_changed(self, value, player_num, **kwargs):
        game = self.machine.game
        if not game:
            return
        player = game.player_list[player_num - 1]
        if player.replay_awarded or value < self.replay_score():
            return
        player.replay_awarded = 1
        free_play = self.machine.settings.get_setting_value("free_play")
        self.machine.events.post("replay_awarded",
            player_num=player_num, replay_score=self.replay_score())
        self.machine.events.post(
            "replay_extra_ball" if free_play else "replay_credit",
            player_num=player_num)

    # 1.5x the best final score of those who got a replay, or halved
    # after 50 games in a row without one
    def adjust(self, **kwargs):
        score = self.replay_score()
        without = self.machine.variables.get_machine_var(
            "replay_games_without") or 0
        game = self.machine.game
        replayed = [ player.score for player in
            (game.player_list if game else []) if player.replay_awarded ]
        if replayed:
            score = max(replayed) * self.RAISE
            without = 0
        else:
            without += 1
            if without >= self.GAMES_BEFORE_HALVING:
                score /= 2
                without = 0
        score = int(max(self.MIN,
            round(score / self.ROUND_TO) * self.ROUND_TO))
        self.machine.variables.set_machine_var("replay_score", score)
        self.machine.variables.set_machine_var("replay_games_without",
            without)
