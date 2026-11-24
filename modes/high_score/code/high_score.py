from mpf.modes.high_score.code.high_score import HighScore


class GrandPrixHighScore(HighScore):
    # A category added since the machine's scores were saved (like
    # shift_count, the Shift Champ) starts from its defaults, instead of
    # empty (MPF leaves it empty, so attract would show its machine
    # vars unfilled)
    def _create_machine_vars(self):
        defaults = self.config["high_score"]["defaults"]
        missing = [category for category in defaults
            if category not in self.high_scores]
        for category in missing:
            self.high_scores[category] = [
                [next(iter(entry.keys())), next(iter(entry.values()))]
                for entry in defaults[category]]
        super()._create_machine_vars()
        if missing:
            self._write_scores_to_disk()
