from mpf.core.custom_code import CustomCode


class Replay(CustomCode):
    # A replay: when a player's score passes the replay score, they get
    # one (once a game): a free credit in credit play, or an extra ball
    # on free play, with a fanfare (see config/common/replay.yaml).
    #
    # The replay score adjusts itself after each game, so replays stay
    # within reach but earned: up when someone got one, down after a
    # few games without one. It's saved on the machine (the
    # replay_score machine var, see config/common/variables.yaml).
    START = 1500000
    STEP_UP = 250000
    STEP_DOWN = 100000
    GAMES_BEFORE_LOWERING = 3
    MIN = 500000
    MAX = 5000000

    def on_load(self):
        self.replayed_this_game = False
        self.machine.events.add_handler("game_started", self.game_started)
        self.machine.events.add_handler("player_score", self.score_changed)
        self.machine.events.add_handler("game_ending", self.adjust)

    def replay_score(self):
        return self.machine.variables.get_machine_var("replay_score") \
            or self.START

    def game_started(self, **kwargs):
        self.replayed_this_game = False

    def score_changed(self, value, player_num, **kwargs):
        game = self.machine.game
        if not game:
            return
        player = game.player_list[player_num - 1]
        if player.replay_awarded or value < self.replay_score():
            return
        player.replay_awarded = 1
        self.replayed_this_game = True
        free_play = self.machine.settings.get_setting_value("free_play")
        self.machine.events.post("replay_awarded",
            player_num=player_num, replay_score=self.replay_score())
        self.machine.events.post(
            "replay_extra_ball" if free_play else "replay_credit",
            player_num=player_num)

    # Up when someone got a replay, down after a few games without one
    def adjust(self, **kwargs):
        score = self.replay_score()
        without = self.machine.variables.get_machine_var(
            "replay_games_without") or 0
        if self.replayed_this_game:
            score += self.STEP_UP
            without = 0
        else:
            without += 1
            if without >= self.GAMES_BEFORE_LOWERING:
                score -= self.STEP_DOWN
                without = 0
        score = max(self.MIN, min(self.MAX, score))
        self.machine.variables.set_machine_var("replay_score", score)
        self.machine.variables.set_machine_var("replay_games_without",
            without)
