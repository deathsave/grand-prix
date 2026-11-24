import asyncio
import random

from mpf.modes.match.code.match import Match
from mpf.platforms.interfaces.segment_display_platform_interface import \
    FlashingType

from code.segment_displays import SegmentDisplays


class GrandPrixMatch(Match):
    # The segment displays spin with the match: every digit of every
    # player's display shows the same number (the match number's tens:
    # scores end in 0), running 0-9 and back down twice with the revs,
    # then counting up to the match number as the lamps settle. When the
    # result's in, the scores come back, with a winner's blinking
    SPIN = [n for n in range(10)] + [n for n in range(8, 0, -1)]
    # (the first spin with the first rev, the second faster, with the
    # second rev at 1.8s, then settling from the third at 3s, like the
    # backbox lamps, see config/match.yaml)
    FIRST_SPIN = 0.1
    SECOND_SPIN = 1.2 / 18
    SETTLE_AT = 3.0
    SETTLE_FOR = 2.0
    # how long a winner's score blinks, with the chimes and the callout
    # (or the game's winner's, with no match), or how long the scores are
    # back before the game ends (a 1 player game with no match)
    BLINK_FOR = 2.0
    SHOW_FOR = 1.0
    KEY = "match"
    PRIORITY = 2000

    # (set up in _run: MPF starts it before mode_start, which can come
    # later, e.g. when high score entry holds the mode's start queue)
    def _start_spin(self):
        self._blinking = False
        self._displays = []
        if self.machine.game:
            for number in range(len(self.machine.game.player_list)):
                display = self.machine.segment_displays.get(
                    f"segment{number + 1}")
                if display:
                    self._displays.append(display)
        at = 0
        for step, digit in enumerate(self.SPIN * 2):
            self.delay.add(at * 1000, self._show_digit, digit=digit)
            at += self.FIRST_SPIN if step < len(self.SPIN) \
                else self.SECOND_SPIN
        self.delay.add(self.SETTLE_AT * 1000, self._settle)
        # (just under the queue relays in config/match.yaml, so after
        # they've held the result for the spin)
        for event in ["match_has_match", "match_no_match"]:
            self.add_mode_event_handler(event, self._show_result,
                priority=-1)

    def _write(self, display, text, flashing=FlashingType.NO_FLASH):
        display.add_text_entry(text, None, flashing, "", None, None,
            self.PRIORITY, self.KEY)

    def _show_digit(self, digit, **kwargs):
        for display in self._displays:
            self._write(display, str(digit) * display.size)

    # count up to the match number, slowing as it gets there
    def _settle(self, **kwargs):
        target = (self.machine.variables.get_machine_var("match_number")
            or 0) // 10
        steps = list(range(0, target + 1))
        weights = [1 + i for i in range(len(steps))]
        at = 0
        for digit, weight in zip(steps, weights):
            self.delay.add(at * 1000, self._show_digit, digit=digit)
            at += self.SETTLE_FOR * weight / sum(weights)

    # the scores again, a match winner's blinking (or with no match, the
    # game's winner, in a multiplayer game)
    def _show_result(self, winner_number=None, **kwargs):
        self.delay.clear()
        game = self.machine.game
        players = game.player_list if game else []
        matched = [number for number in range(len(players))
            if kwargs.get(f"match_number{number}") == winner_number]
        blinking = matched or [number - 1 for number in
            SegmentDisplays.winners(game)]
        self._blinking = bool(blinking)
        for number, display in enumerate(self._displays):
            if number >= len(players):
                continue
            self._write(display, str(players[number].score),
                FlashingType.FLASH_ALL if number in blinking
                else FlashingType.NO_FLASH)

    async def _run(self) -> None:
        self._start_spin()
        await super()._run()
        await asyncio.sleep(self.BLINK_FOR if self._blinking
            else self.SHOW_FOR)

    def mode_stop(self, **kwargs):
        for display in self._displays:
            display.remove_text_by_key(self.KEY)
        super().mode_stop(**kwargs)

    # MPF's match chance is match_percentage to the power of how many
    # different match numbers the players have: 10% for one, but 10^2
    # (100) for two and 10^3 for three, so a 2 or 3 player game nearly
    # always matched. Here each different number gets its own chance
    # (match_percentage, 10% by default), like an EM where each number
    # is 1 in 10: about 10% with one player, 19% with two, 27% with 3.
    def _get_winner_number(self, match_numbers, match_percentage) -> int:
        numbers = sorted(set(match_numbers))
        chance = match_percentage / 100
        if random.random() < 1 - (1 - chance) ** len(numbers):
            return random.choice(numbers)

        step = self.config.get("mode_settings", {}).get(
            "non_match_number_step", 1)
        return random.choice(
            sorted(set(range(0, 100, step)) - set(match_numbers)))
