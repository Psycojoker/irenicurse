import logging


class BaseWidgetClass(object):
    """
    The base class of every Irenicurse's widgets. Every widgets should inherit
    from it to work has expected.

    It manages all interactions with the stack.

    Except if you create a new widget there should be no reasons for you to
    interact with it.
    """

    def __init__(self):
        _keybindings = {}
        for x in dir(self):
            i = getattr(self, x)
            if hasattr(i, "__keys__"):
                for j in i.__keys__:
                    _keybindings[j] = i
        if _keybindings:
            logging.debug("%s has _keybindings: %s" % (self, _keybindings))
        self._keybindings = _keybindings

    def manage_input(self, input):
        """
        Method responsible to handle inputs and dispatch it to the current
        focused widget.
        """
        logging.debug("[%s] receive input: %s" % (self.__class__, input))
        if self._keybindings.get(input) and hasattr(self, self._keybindings[input].func_name):
            logging.debug("[%s] execute corresponding function: %s" %
                          (self.__class__, self._keybindings[input]))
            self._keybindings[input]()
        else:
            logging.debug("[%s] drop input" % self.__class__)

    def attach_to_stack(self, stack):
        """
        Uses by the stack to attach itself to the widget.
        """
        logging.debug("[%s] attach self to stack: %s" % (self.__class__, stack))
        self.stack = stack

    def quit(self):
        """
        Remove itself from the stack.

        By default if the stack is empty the process will end.
        """
        self.stack.pop()

    def call(self, widget, callback=None):
        """
        Push a new widget on the stack on top of itself.

        Expect an Irenicurse widget (raw Urwid widget shouldn't work as expected).
        """
        self.stack.stack[-1].__callback__ = callback
        self.stack.push(widget)

    def answer(self, *args, **kwargs):
        self.stack.pop()
        self.stack.stack[-1].__callback__(*args, **kwargs)

    def replace(self, widget):
        """
        Replace self on stack with a new widget.

        Expect an Irenicurse widget (raw Urwid widget shouldn't work as expected).
        """
        self.stack.replace(widget)

    def get_title(self):
        """
        Hook to overwrite to set the title of the page.

        Should return either text, an attrmap urwid widget or a text urwid widget.
        """
        return None

    def get_footer(self):
        """
        Hook to overwrite to set the footer of the page.

        Should return either text, an attrmap urwid widget or a text urwid widget.
        """
        return None

    def ask(self, text, callback):
        """
        Ask a question to the user and send its answer to the callback.

        The user input ends once "enter" is pressed.
        """
        self.stack.ask(text, callback=callback)

    def yes_or_no(self, text, callback):
        """
        Ask a binary question to the user and send the answer to the callback.

        The user must press either the key "y" (yes) or the key "n" 
        """
        self.stack.yes_or_no(text, callback)
