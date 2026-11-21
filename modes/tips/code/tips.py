import os
from ruamel.yaml import YAML
from mpf.core.mode import Mode

class Tips(Mode):
    # The tip_slide text widgets display these machine vars,
    # so "typing" is just growing each string a character
    # at a time. See config/common/widgets.yaml (tip_*).
    TITLE_VAR = "tip_title"
    LINE_VARS = [ "tip_line1", "tip_line2", "tip_line3", "tip_line4" ]

    CHAR_MS = 45        # delay between characters
    LINE_PAUSE_MS = 400 # pause after finishing a line
    CURSOR = "_"

    def mode_init(self):
        self.tips = self.load_tips()
        self.tip_index = 0

    def mode_start(self, **kwargs):
        self.rotating = False
        self.clear()
        self.add_mode_event_handler("attract_tip", self.next_tip)
        self.add_mode_event_handler("attract_tip_clear", self.clear)
        self.add_mode_event_handler("attract_intro_done",
            self.start_rotation)
        self.add_mode_event_handler("sw_left_flipper", self.skip)
        self.add_mode_event_handler("sw_right_flipper", self.skip)

    # The Death Save intro finished. Start the splash/tip
    # rotation unless a flipper already started it.
    def start_rotation(self, **kwargs):
        if not self.rotating:
            self.rotating = True
            self.machine.events.post("tips_rotation_start")

    # Flipper pressed: jump to the next tip
    def skip(self, **kwargs):
        self.rotating = True
        self.machine.events.post("tips_skip")

    def mode_stop(self, **kwargs):
        self.clear()

    # Reads the tip content from modes/tips/content/tips.yaml
    def load_tips(self):
        path = os.path.join(self.path, "content", "tips.yaml")
        with open(path) as f:
            return YAML(typ="safe").load(f) or []

    # Types out the next tip, wrapping back to the first
    def next_tip(self, **kwargs):
        if not self.tips:
            return
        tip = self.tips[self.tip_index % len(self.tips)]
        self.tip_index += 1

        self.clear()
        lines = (tip.get("lines") or [])[:len(self.LINE_VARS)]
        self.queue = [ (self.TITLE_VAR, tip["title"]) ] + \
            list(zip(self.LINE_VARS, lines))
        self.chars = 0
        self.delay.add(self.CHAR_MS, self.type_next_char, "typing")

    # Reveals one more character of the current line, then
    # schedules itself until every line has been typed
    def type_next_char(self):
        var, text = self.queue[0]
        self.chars += 1
        line_done = self.chars >= len(text)
        cursor = "" if line_done else self.CURSOR
        self.set_var(var, text[:self.chars] + cursor)

        if not line_done:
            self.delay.add(self.CHAR_MS, self.type_next_char, "typing")
            return
        self.queue.pop(0)
        self.chars = 0
        if self.queue:
            self.delay.add(self.LINE_PAUSE_MS,
                self.type_next_char, "typing")

    def clear(self, **kwargs):
        self.delay.remove("typing")
        self.queue = []
        for var in [ self.TITLE_VAR ] + self.LINE_VARS:
            self.set_var(var, "")

    def set_var(self, name, value):
        self.machine.variables.set_machine_var(name, value)
