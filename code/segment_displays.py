from mpf.core.custom_code import CustomCode
from mpf.platforms.interfaces.segment_display_platform_interface import \
    FlashingType


class SegmentDisplays(CustomCode):
    # Fun with the score displays (they show 0-9, blank and blink). Each
    # only takes over the scores briefly, over them on the displays'
    # stacks (the scores are at ~110, see
    # modes/segment_display/config/segment_display_player.yaml) and
    # under the match's spin (2000, see modes/match/code/match.py):
    #
    # - Off the Line's start tree: all four count down 3-2-1 together
    #   with its countdown, then the scores come back on green
    # - Award count-ups: a big award (20k or more: skill shots,
    #   jackpots, super jackpots, a big bonus) rolls the score up to its
    #   new total, like an EM's reels, instead of jumping
    # - Pure Evil: every display but the current player's alternates
    #   "    666", "666 666" and "666    " while it runs
    # - The winning score blinks as a multiplayer game ends (the match
    #   then blinks its winners, or the game's winner with no match)
    DISPLAYS = [f"segment{n}" for n in range(1, 5)]
    PRIORITY = 1500

    COUNTDOWN = {"off_the_line_countdown3": 3, "off_the_line_countdown2": 2,
        "off_the_line_countdown1": 1}
    # (and gone after this anyway, if green never comes)
    COUNTDOWN_FOR = 1.5

    COUNT_UP_FROM = 20000
    COUNT_UP_STEPS = 8
    COUNT_UP_FOR = 0.6

    EVIL = ["    666", "666 666", "666    "]
    EVIL_EVERY = 0.4

    def on_load(self):
        events = self.machine.events
        for event in self.COUNTDOWN:
            events.add_handler(event, self.countdown, event_name=event)
        events.add_handler("green_flag_dropped", self.end_countdown)
        events.add_handler("mode_green_flag_stopped", self.end_countdown)
        self.counting = {}
        events.add_handler("player_score", self.score_changed)
        events.add_handler("mode_pure_evil_started", self.start_evil)
        events.add_handler("mode_pure_evil_stopped", self.stop_evil)
        events.add_handler("game_ending", self.blink_winner, priority=1000)
        events.add_handler("game_ended", self.clear)
        events.add_handler("game_started", self.clear)

    def _display(self, name):
        return self.machine.segment_displays.get(name)

    def _write(self, name, key, text, flashing=FlashingType.NO_FLASH):
        display = self._display(name)
        if display:
            display.add_text_entry(text, None, flashing, "", None, None,
                self.PRIORITY, key)

    def _remove(self, name, key):
        display = self._display(name)
        if display:
            display.remove_text_by_key(key)

    # -- Off the Line's start tree --

    def countdown(self, event_name, **kwargs):
        digit = str(self.COUNTDOWN[event_name])
        for name in self.DISPLAYS:
            self._write(name, "countdown", digit * 7)
        self.delay.reset(self.COUNTDOWN_FOR * 1000, self.end_countdown,
            "countdown")

    def end_countdown(self, **kwargs):
        self.delay.remove("countdown")
        for name in self.DISPLAYS:
            self._remove(name, "countdown")

    # -- Award count-ups --

    def score_changed(self, value, change, player_num, **kwargs):
        name = f"segment{player_num}"
        if change < self.COUNT_UP_FROM or not self.machine.game:
            # (a small one during a count-up: count to the new total)
            if name in self.counting:
                self.counting[name]["to"] = value
            return
        # from wherever it's showing (another count-up's partway)
        start = self.counting.get(name, {}).get("now", value - change)
        self.counting[name] = {"from": start, "to": value, "now": start,
            "step": 0}
        self._count_up(display=name)

    def _count_up(self, display):
        count = self.counting.get(display)
        if not count:
            return
        count["step"] += 1
        if count["step"] >= self.COUNT_UP_STEPS:
            del self.counting[display]
            self._remove(display, "count_up")
            return
        done = count["step"] / self.COUNT_UP_STEPS
        # (easing out: quick, then settling onto the total)
        done = 1 - (1 - done) ** 2
        now = int(count["from"] + (count["to"] - count["from"]) * done)
        # (scores end in 0)
        count["now"] = now - now % 10
        self._write(display, "count_up", str(count["now"]))
        self.delay.reset(self.COUNT_UP_FOR * 1000 / self.COUNT_UP_STEPS,
            self._count_up, f"count_up_{display}", display=display)

    def _stop_count_ups(self):
        for name in list(self.counting):
            self.delay.remove(f"count_up_{name}")
            self._remove(name, "count_up")
        self.counting = {}

    # -- Pure Evil --

    def start_evil(self, **kwargs):
        game = self.machine.game
        current = game.player.number if game and game.player else 0
        self.evil_displays = [name for n, name in
            enumerate(self.DISPLAYS, start=1) if n != current]
        self.evil_step = 0
        self._evil()

    def _evil(self):
        text = self.EVIL[self.evil_step % len(self.EVIL)]
        for name in self.evil_displays:
            self._write(name, "pure_evil", text)
        self.evil_step += 1
        self.delay.reset(self.EVIL_EVERY * 1000, self._evil, "pure_evil")

    def stop_evil(self, **kwargs):
        self.delay.remove("pure_evil")
        for name in self.DISPLAYS:
            self._remove(name, "pure_evil")

    # -- The winner --

    @staticmethod
    def winners(game):
        """The players (numbers) with the top score, in a multiplayer
        game."""
        if not game or len(game.player_list) < 2:
            return []
        top = max(player.score for player in game.player_list)
        return [player.number for player in game.player_list
            if player.score == top]

    def blink_winner(self, **kwargs):
        self._stop_count_ups()
        game = self.machine.game
        for number in self.winners(game):
            self._write(f"segment{number}", "winner",
                str(game.player_list[number - 1].score),
                FlashingType.FLASH_ALL)

    # A new game, or the end of one: all of it off the displays
    def clear(self, **kwargs):
        self.end_countdown()
        self._stop_count_ups()
        self.stop_evil()
        for name in self.DISPLAYS:
            self._remove(name, "winner")
