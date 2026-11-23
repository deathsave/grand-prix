import random

from mpf.modes.match.code.match import Match


class GrandPrixMatch(Match):
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
