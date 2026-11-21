import os
from ruamel.yaml import YAML
from mpf.core.mode import Mode

class Tips(Mode):
    # The tip_slide text widgets display these machine vars,
    # so "typing" is just growing each string a character
    # at a time. See config/common/widgets.yaml (tip_*).
    TITLE_VAR = "tip_title"
    LINE_VARS = [ "tip_line1", "tip_line2", "tip_line3", "tip_line4" ]

    # fast enough to type the longest tip in ~7s of
    # its 10s (see shows/attract_rotation.yaml)
    CHAR_MS = 30        # delay between characters
    LINE_PAUSE_MS = 300 # pause after finishing a line
    CURSOR = "_"

    # The rotation show: splash, then one step per tip
    # (see shows/attract_rotation.yaml)
    SHOW = "attract_rotation"
    FIRST_TIP_STEP = 2

    def mode_init(self):
        self.tips = self.load_tips()

    def mode_start(self, **kwargs):
        self.show = None
        self.clear()
        self.add_mode_event_handler("attract_tip", self.show_tip)
        self.add_mode_event_handler("attract_tip_clear", self.clear)
        self.add_mode_event_handler("attract_intro_done",
            self.start_rotation)
        self.add_mode_event_handler("sw_right_flipper", self.advance)
        self.add_mode_event_handler("sw_left_flipper", self.rewind)

    # Plays the rotation show (looping forever). This mode
    # holds on to it so the flippers can step through it.
    def start_rotation(self, start_step=1, **kwargs):
        if self.show:
            return
        self.show = self.machine.shows[self.SHOW].play(
            priority=self.priority, loops=-1, start_step=start_step)

    # Right flipper: next step (from the intro: first tip)
    def advance(self, **kwargs):
        if self.show:
            self.show.advance()
        else:
            self.start_rotation(start_step=self.FIRST_TIP_STEP)

    # Left flipper: previous step (from the intro: last tip)
    def rewind(self, **kwargs):
        if self.show:
            self.show.step_back()
        else:
            self.start_rotation(start_step=-1)

    def mode_stop(self, **kwargs):
        if self.show:
            self.show.stop()
            self.show = None
        self.clear()

    # Reads the tip content from modes/tips/content/tips.yaml
    def load_tips(self):
        path = os.path.join(self.path, "content", "tips.yaml")
        with open(path) as f:
            return YAML(typ="safe").load(f) or []

    # Types out the tip for the show's current step
    def show_tip(self, **kwargs):
        if not self.tips:
            return
        tip = self.tips[self.tip_number() % len(self.tips)]

        self.clear()
        self.machine.events.post(self.slide_for(tip))
        lines = (tip.get("lines") or [])[:len(self.LINE_VARS)]
        self.queue = [ (self.TITLE_VAR, tip["title"]) ] + \
            list(zip(self.LINE_VARS, lines))
        self.chars = 0
        self.delay.add(self.CHAR_MS, self.type_next_char, "typing")

    # Which tip the rotation show is on (the first
    # tip when posted without the show, e.g. in tests)
    def tip_number(self):
        if not self.show or self.show.current_step_index is None:
            return 0
        return self.show.current_step_index - (self.FIRST_TIP_STEP - 1)

    # Tips with a mode use that mode's look
    # (tip_<mode>_slide), otherwise the plain tip_slide.
    # The event and slide share a name (see slide_player).
    def slide_for(self, tip):
        mode = tip.get("mode")
        return f"tip_{mode}_slide" if mode else "tip_slide"

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
