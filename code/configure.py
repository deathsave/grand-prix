import os
from mpf.core.custom_code import CustomCode


class Configure(CustomCode):
    def on_load(self):
        self._handle_mode_availability("pure_evil")

    # For being able to test modes in isolation and/or preventing
    # edge cases where mode logic might affect other mode tests
    #
    # Use in the on_load hook with:
    #   self._handle_mode_availability("your_mode_name")
    #
    # Then ensure modes/your_mode_name/config/mode.yaml has:
    #   start_events: some_event{machine.is_your_mode_name_available}
    def _handle_mode_availability(self, mode):
        env_var = mode.upper()
        env_val = os.environ.get(env_var)
        available = 1 if env_val is None or env_val == "1" else 0
        self.machine.variables.set_machine_var(f"is_{mode}_available", available)
