import random
from mpf.core.mode import Mode
from mpf.modes.attract.code.attract import Attract

class GrandPrixAttract(Attract):

    def mode_start(self, **kwargs):
        self.machine.timers["segment_wiggle_timer"].reset()
        timer_event = "timer_segment_wiggle_timer_tick"
        self.add_mode_event_handler(timer_event,
            self.wiggle_segment)
        super().mode_start(**kwargs)

    def wiggle_segment(self, **kwargs):
        ticks = self.machine.timers["segment_wiggle_timer"].ticks
        self.machine.segment_displays["segment1"].add_text("")
        self.machine.segment_displays["segment2"].add_text("")
        self.machine.segment_displays["segment3"].add_text("")
        self.machine.segment_displays["segment4"].add_text("")

        if ticks > 58:
            segment_number = random.randint(1, 4)
            segment = self.machine. \
                segment_displays["segment" + str(segment_number)]
            segment.add_text(
                random.randint(0,99999)
            )
        elif ticks > 55:
            for i in range(1, 5):
                self.machine. \
                    segment_displays["segment" + str(i)]. \
                        add_text("")
        elif ticks > 45:
            self.machine.segment_displays["segment4"]. \
                add_text("1337")
        elif ticks > 32:
            self.machine.segment_displays["segment3"]. \
                add_text("50")
        elif ticks > 19:
            self.machine.segment_displays["segment2"]. \
                add_text("15")
        elif ticks > 5:
            self.machine.segment_displays["segment1"]. \
                add_text("1986")
