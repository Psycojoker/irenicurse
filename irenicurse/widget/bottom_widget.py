import urwid

from base import BaseWidgetClass
from decorator import bind_to_key

class OneLineEdit(BaseWidgetClass, urwid.Edit):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs["callback"]
        del kwargs["callback"]
        urwid.Edit.__init__(self, *args, **kwargs)
        BaseWidgetClass.__init__(self)

    def keypress(self, size, key):
        if key == "enter":
            self.callback(self.edit_text)
            self.stack.end_footer_call()
        urwid.Edit.keypress(self, size, key)


class YesOrNoWidget(BaseWidgetClass, urwid.Text):
    def __init__(self, text, callback, *args, **kwargs):
        self.callback = callback
        urwid.Text.__init__(self, text, *args, **kwargs)
        BaseWidgetClass.__init__(self)

    @bind_to_key("y")
    @bind_to_key("Y")
    @bind_to_key("enter")
    def yes(self):
        self.callback(True)
        self.stack.end_footer_call()

    @bind_to_key("n")
    @bind_to_key("N")
    def no(self):
        self.callback(False)
        self.stack.end_footer_call()
