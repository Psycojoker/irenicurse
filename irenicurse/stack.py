import urwid
import logging
from os.path import expanduser

from widget import OneLineEdit

logging.basicConfig(filename=expanduser("~/.irenicurse.log"))
logging.root.setLevel(logging.DEBUG)

class ApplicationStack(urwid.Frame):
    def __init__(self, widget):
        urwid.Frame.__init__(self, widget)
        logging.debug("[Stack] init with widget: %s" % widget)
        self.stack = []
        self.push(widget)

    def push(self, widget):
        logging.debug("[Stack] push on stack the widget: %s" % widget)
        widget.attach_to_stack(self)
        self.set_body(widget)
        self.stack.append(widget)
        self.update_title_and_footer(widget)

    def manage_input(self, input):
        logging.debug("[Stack] reicive input: %s" % [input])
        logging.debug("[Stack] deleguate input to top widget: %s" % self.stack[-1])
        if self.get_focus() == "body":
            self.stack[-1].manage_input(input)
        elif self.get_focus() == "footer":
            self.footer.manage_input(input)

    def pop(self):
        logging.debug("[Stack] pop top widget")
        self.stack = self.stack[:-1]
        if not self.stack:
            logging.debug("[Stack] stack empty, exit main loop, bye bye")
            raise urwid.ExitMainLoop()
        else:
            self.set_body(self.stack[-1])
            self.update_title_and_footer(self.stack[-1])

    def set_frame_title(self, widget):
        if widget.get_title() is None:
            return

        self.set_header(urwid.AttrWrap(urwid.Text(widget.get_title()), 'title'))

    def set_frame_footer(self, widget):
        if widget.get_footer() is None:
            return

        self.set_footer(urwid.AttrWrap(urwid.Text(widget.get_footer()), 'title'))

    def update_title_and_footer(self, widget):
        self.set_frame_title(widget)
        self.set_frame_footer(widget)

    def ask(self, text, callback):
        self.call_on_footer(OneLineEdit(text + (" " if text != "" else ""), callback=callback))

    def call_on_footer(self, widget):
        self.old_footer = self.get_footer()
        self.set_footer(widget)
        self.footer.attach_to_stack(self)
        self.set_focus('footer')

    def end_footer_call(self):
        self.set_focus('body')
        self.set_footer(self.old_footer)
