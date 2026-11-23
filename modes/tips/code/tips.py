import os
import re
from ruamel.yaml import YAML
from mpf.core.mode import Mode

class Tips(Mode):
    # The tip_slide text widgets display these machine vars,
    # so "typing" is just growing each string a word at a
    # time (each display update costs a redraw, so words
    # rather than characters). See config/common/widgets.yaml
    # (tip_*).
    TITLE_VAR = "tip_title"
    LINE_VARS = [ "tip_line1", "tip_line2", "tip_line3", "tip_line4" ]

    # fast enough to type the longest tip in ~7.5s of
    # its 10s (see shows/attract_rotation.yaml)
    WORD_MS = 150       # delay between words
    LINE_PAUSE_MS = 300 # pause after finishing a line
    CURSOR = "_"

    # The rotation show: splash, then one step per tip
    # (see shows/attract_rotation.yaml)
    SHOW = "attract_rotation"
    FIRST_TIP_STEP = 2

    def mode_init(self):
        self.tips = self.load_tips()

    # The side each slide slides in from (see config/slide_player.yaml):
    # the side of the flipper button pressed, or the right when the
    # rotation moves on by itself. (The flipper tags are swapped
    # relative to the buttons: right_flipper, which advances, is the
    # physically left button)
    AUTO_SIDE = "right"
    ADVANCE_SIDE = "left"
    REWIND_SIDE = "right"
    SPLASH = "splash_slide"

    def mode_start(self, **kwargs):
        self.show = None
        self.side = self.AUTO_SIDE
        self.clear()
        self.add_mode_event_handler("attract_tip", self.show_tip)
        self.add_mode_event_handler("attract_splash", self.show_splash)
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
        self.side = self.ADVANCE_SIDE
        if self.show:
            self.show.advance()
        else:
            self.start_rotation(start_step=self.FIRST_TIP_STEP)

    # Left flipper: previous step (from the intro: last tip)
    def rewind(self, **kwargs):
        self.side = self.REWIND_SIDE
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
        self.play_slide(self.slide_for(tip))
        lines = (tip.get("lines") or [])[:len(self.LINE_VARS)]
        values = self.values()
        self.queue = [ (var, text.format_map(values)) for var, text in
            [ (self.TITLE_VAR, tip["title"]) ] +
            list(zip(self.LINE_VARS, lines)) ]
        self.words = 0
        self.delay.add(self.WORD_MS, self.type_next_word, "typing")

    # Live values a tip's text can show, as {name} (see
    # content/tips.yaml), worked out when the tip comes up
    def values(self):
        replay_score = self.machine.variables.get_machine_var(
            "replay_score") or 0
        free_play = self.machine.settings.get_setting_value("free_play")
        return {
            "replay_score": f"{replay_score:,}",
            "replay_award": "an extra ball" if free_play
                else "a free game",
        }

    def show_splash(self, **kwargs):
        self.play_slide(self.SPLASH)

    # Plays a slide, sliding in from the side for how we got here (then
    # back to the automatic side)
    def play_slide(self, slide):
        self.machine.events.post(f"{slide}_from_{self.side}")
        self.side = self.AUTO_SIDE

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

    # Reveals one more word of the current line (with any
    # spaces before it, so indents stay), then schedules
    # itself until every line has been typed
    def type_next_word(self):
        var, text = self.queue[0]
        words = re.findall(r"\s*\S+", text)
        self.words += 1
        line_done = self.words >= len(words)
        cursor = "" if line_done else self.CURSOR
        self.set_var(var, "".join(words[:self.words]) + cursor)

        if not line_done:
            self.delay.add(self.WORD_MS, self.type_next_word, "typing")
            return
        self.queue.pop(0)
        self.words = 0
        if self.queue:
            self.delay.add(self.LINE_PAUSE_MS,
                self.type_next_word, "typing")

    def clear(self, **kwargs):
        self.delay.remove("typing")
        self.queue = []
        for var in [ self.TITLE_VAR ] + self.LINE_VARS:
            self.set_var(var, "")

    def set_var(self, name, value):
        self.machine.variables.set_machine_var(name, value)
