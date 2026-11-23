from mpf.modes.bonus.code.bonus import Bonus


class GrandPrixBonus(Bonus):
    # MPF's bonus mode, with each line it pays put up on a results
    # board (see config/bonus.yaml): the next row's label and value
    # (machine vars), its points counting up, then the total
    LABELS = {
        "bonus_main": "Luxury",
        "bonus_lap": "Laps",
        "bonus_multiballs": "Multiballs",
        "bonus_supers": "Super Jackpots",
    }
    ROWS = 4
    COUNT_STEPS = 12
    COUNT_STEP_MS = 40

    def mode_start(self, **kwargs):
        self.rows = 0
        for row in range(1, self.ROWS + 1):
            self.machine.variables.set_machine_var(
                f"bonus_row{row}_label", "")
            self.machine.variables.set_machine_var(
                f"bonus_row{row}_value", "")
        self.machine.variables.set_machine_var("bonus_total_value", "")
        for event in self.LABELS:
            self.add_mode_event_handler(event, self.add_row,
                event_name=event)
        self.add_mode_event_handler("bonus_total", self.show_total)
        super().mode_start(**kwargs)

    def add_row(self, event_name, score=0, hits=0, **kwargs):
        if self.rows >= self.ROWS:
            return
        self.rows += 1
        row = self.rows
        self.machine.variables.set_machine_var(f"bonus_row{row}_label",
            f"{self.LABELS[event_name]}  x{hits}")
        self.count_up(f"bonus_row{row}_value", score)
        self.machine.events.post(f"bonus_row_{row}_shown")

    def show_total(self, score=0, **kwargs):
        self.count_up("bonus_total_value", score)
        self.machine.events.post("bonus_total_shown")

    # Counts a machine var up to the score, in a few quick steps
    def count_up(self, var, score, step=1):
        value = int(score * step / self.COUNT_STEPS)
        self.machine.variables.set_machine_var(var, f"{value:,}")
        if step < self.COUNT_STEPS:
            self.delay.add(self.COUNT_STEP_MS, self.count_up,
                f"count_{var}", var=var, score=score, step=step + 1)
