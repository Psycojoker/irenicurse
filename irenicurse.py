import logging
import urwid
from os.path import expanduser

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

    def manage_input(self, input):
        logging.debug("[Stack] reicive input: %s" % [input])
        logging.debug("[Stack] deleguate input to top widget: %s" % self.stack[-1])
        self.stack[-1].manage_input(input)

    def pop(self):
        logging.debug("[Stack] pop top widget")
        self.stack = self.stack[:-1]
        if not self.stack:
            logging.debug("[Stack] stack empty, exit main loop, bye bye")
            raise urwid.ExitMainLoop()
        else:
            self.set_body(self.stack[-1])


class BaseWidgetClass(object):
    # I think this will create bugs
    keys = {}

    @classmethod
    def link_to_key(klass, key):
        def decorate(func):
            logging.debug("[link_to_key] link key %s on method %s of %s" % ([key], func, klass))
            klass.keys[key] = func
            return func
        return decorate

    def manage_input(self, input):
        logging.debug("[%s] receive input: %s" % (self.__class__, input))
        if self.keys.get(input):
            logging.debug("[%s] execute corresponding function: %s" % (self.__class__, self.keys[input]))
            self.keys[input](self)
        else:
            logging.debug("[%s] drop input" % self.__class__)

    def attach_to_stack(self, stack):
        logging.debug("[%s] attach self to stack: %s" % (self.__class__, stack))
        self.stack = stack

    def quit(self):
        self.stack.pop()

    def call(self, widget):
        self.stack.push(widget)


class ListWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, content, index=0):
        self.content = map(self.convert_new_item, content)
        urwid.ListBox.__init__(self, self.content)
        self.set_focus(index)

    def convert_new_item(self, item):
        if not isinstance(item, (urwid.Text, urwid.AttrWrap)):
            item = urwid.Text(item)
        if not isinstance(item, urwid.AttrWrap):
            item = urwid.AttrWrap(item, None, 'reveal focus')
        return item

    def go_down(self):
        index = self.get_current_position()
        index += 1
        if index >= len(self.content):
            index = len(self.content) - 1
        self.set_focus(index)

    def go_up(self):
        index = self.get_current_position()
        index -= 1
        if index < 0:
            index = 0
        self.set_focus(index)

    def append(self, new_item):
        self.content.append(self.convert_new_item(new_item))

    def delete(self, position=None):
        if position is None:
            position = self.get_current_position()
        logging.debug("[%s] going to delete item at position: %s" % (self.__class__, position))
        if position is not None:
            self.content.pop(position)

    def get_current_position(self):
        return self.get_focus()[1]

    def get_current_item(self):
        return self.get_focus()[0]._original_widget.get_text()[0]

    def insert(self, new_item, position=None):
        if position is None:
            position = self.get_current_position()
            if position is None:
                position = 0
        logging.debug("[%s] going to insert item at position: %s" % (self.__class__, position))
        self.content.insert(position, self.convert_new_item(new_item))


class FullListWidget(ListWidget):
    @BaseWidgetClass.link_to_key("q")
    def quit(self):
        ListWidget.quit(self)

    @BaseWidgetClass.link_to_key("down")
    @BaseWidgetClass.link_to_key("j")
    def go_down(self):
        ListWidget.go_down(self)
        logging.debug("%s" % [self.get_focus()])

    @BaseWidgetClass.link_to_key("up")
    @BaseWidgetClass.link_to_key("k")
    def go_up(self):
        ListWidget.go_up(self)
        logging.debug("%s" % [self.get_focus()])


class TestFullListWidget(FullListWidget):
    @FullListWidget.link_to_key("a")
    def testeu(self):
        self.call(TestFullListWidget("ceci est du chocolat au lait".split()))

    @FullListWidget.link_to_key("r")
    def testeu2(self):
        self.call(TestFullListWidget("taratata pouet pouet".split()))

    @FullListWidget.link_to_key("d")
    def test_delete(self):
        self.delete(self.get_current_position())

    @FullListWidget.link_to_key("z")
    def test_append(self):
        self.append("qsd qsd")

    @FullListWidget.link_to_key("e")
    def show_focus(self):
        logging.debug("%s" % [self.get_focus()])

    @FullListWidget.link_to_key("t")
    def test_insert(self):
        self.insert("caca pouet pouet")


def run(widget, palette=None):
    if palette is None:
        palette = [
            ('reveal focus', 'black', 'white', 'standout'),
        ]
    stack = ApplicationStack(widget)
    urwid.MainLoop(stack, unhandled_input=stack.manage_input, palette=palette).run()


if __name__ == "__main__":
    logging.debug("[main] start")
    run(TestFullListWidget(map(unicode, range(10))))
    logging.debug("[main] end")
    logging.debug("\n" * 200)
