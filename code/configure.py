import os
from mpf.core.custom_code import CustomCode


class Configure(CustomCode):
    def on_load(self):
        self._handle_feature_availability("pure_evil")
        self._handle_feature_availability("wear_and_tear")

    # For being able to test features in isolation and/or preventing
    # edge cases where feature logic might affect other tests
    #
    # Use in the on_load hook with:
    #   self._handle_feature_availability("your_mode_name")
    #
    # Then ensure modes/your_mode_name/config/mode.yaml has:
    #   start_events: some_event{machine.is_your_feature_name_available}
    # or something similar per the env variable used.
    #
    # GOTCHA: unset env variables will be enabled (1), so they do not
    # need to be passed in normal operation.
    def _handle_feature_availability(self, identifier):
        env_var = identifier.upper()
        env_val = os.environ.get(env_var)
        available = 1 if env_val is None or env_val == "1" else 0
        self.machine.variables.set_machine_var(f"is_{identifier}_available", available)
