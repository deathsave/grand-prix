from mpf.core.custom_code import CustomCode

class ClassName(CustomCode):
    def on_load(self):
        pass
        # self.machine.events.add_handler('machine_reset_phase_1',
        #     self.do_something)

    def do_something(self, **kwargs):
        pass
