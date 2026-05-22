import os
from mpf.core.custom_code import CustomCode

class Configure(CustomCode):
    def on_load(self):
        self._handle_mode_availability("pure_evil")

    def _handle_mode_availability(self, mode):
        env_var = mode.upper()
        env_val = os.environ.get(env_var)
        available = 1 if env_val is None or env_val == "1" else 0
        self.machine.variables.set_machine_var(f"is_{mode}_available", available)
