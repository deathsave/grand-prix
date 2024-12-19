from mpf.core.mode import Mode
from objprint import op
import time

class Attract(Mode):

    # def mode_init(self):
    #     pass

    def mode_start(self, **kwargs):
        # self.machine.lights.l_backbox_match_00.color('white')
        # for each of the lights
        while True:
            for light in self.machine.lights.values():
                time.sleep(0.333333)
                op(light.get_color())
                # turn the light off
                # if light.color() == 'white':
                #     light.color('black')
                # else:
                #     light.color('white')

        # Set a delay to call self.my_callback() in 5 seconds
        # self.delay.add(5000, self.my_callback)

        # # turn LED "led01" red
        # op(self.machine.lights)
        # self.machine.leds.led01.color('red')

    # def mode_stop(self, **kwargs):
    #     pass
