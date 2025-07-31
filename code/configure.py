import os
from mpf.core.custom_code import CustomCode

class Configure(CustomCode):
    def on_load(self):
        # To allow this mode to be loaded
        # based on Environment variable
        if "PURE_EVIL" not in os.environ:
            self.machine.variables. \
                set_machine_var("is_pure_evil_available", 1)

        elif os.environ["PURE_EVIL"] == "1":
            self.machine.variables. \
                set_machine_var("is_pure_evil_available", 1)
        else:
            self.machine.variables. \
                set_machine_var("is_pure_evil_available", 0)
