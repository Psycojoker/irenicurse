import urwid

from stack import ApplicationStack

def run(widget, palette=None):
    if palette is None:
        palette = [
            ('reveal focus', 'black', 'white', 'standout'),
        ]
    stack = ApplicationStack(widget)
    urwid.MainLoop(stack, unhandled_input=stack.manage_input, palette=palette).run()
