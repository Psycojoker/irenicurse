import logging
import urwid

def link_to_key(key):
    def decorate(func):
        func.__keys__ = func.__keys__ + [key] if hasattr(func, "__keys__") else [key]
        return func
    return decorate

class BaseWidgetClass(object):
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
        logging.debug("[%s] receive input: %s" % (self.__class__, input))
        if self._keybindings.get(input) and hasattr(self, self._keybindings[input].func_name):
            logging.debug("[%s] execute corresponding function: %s" %
                          (self.__class__, self._keybindings[input]))
            self._keybindings[input]()
        else:
            logging.debug("[%s] drop input" % self.__class__)

    def attach_to_stack(self, stack):
        logging.debug("[%s] attach self to stack: %s" % (self.__class__, stack))
        self.stack = stack

    def quit(self):
        self.stack.pop()

    def call(self, widget):
        self.stack.push(widget)

    def get_title(self):
        return None

    def get_footer(self):
        return None


class ListWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, content, index=0):
        logging.debug("[ListWidget] init with content: %s" % list(content))
        BaseWidgetClass.__init__(self)
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
        if index is None:
            return
        index += 1
        if index >= len(self.content):
            index = len(self.content) - 1
        self.set_focus(index)

    def go_up(self):
        index = self.get_current_position()
        if index is None:
            return
        index -= 1
        if index < 0:
            index = 0
        self.set_focus(index)

    def append(self, new_item):
        self.content.append(self.convert_new_item(new_item))

    def delete(self, position=None):
        if position is None:
            position = self.get_current_position()
        logging.debug("[%s] going to delete item at position: %s" %
                      (self.__class__, position))
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
        logging.debug("[%s] going to insert item at position: %s" %
                      (self.__class__, position))
        self.content.insert(position, self.convert_new_item(new_item))


class FullListWidget(ListWidget):
    @link_to_key("q")
    def quit(self):
        ListWidget.quit(self)

    @link_to_key("down")
    @link_to_key("j")
    def go_down(self):
        ListWidget.go_down(self)
        logging.debug("%s" % [self.get_focus()])

    @link_to_key("up")
    @link_to_key("k")
    def go_up(self):
        ListWidget.go_up(self)
        logging.debug("%s" % [self.get_focus()])

class ColumnWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, columns):
        logging.debug("[ColumnWidget] constructor received data: %s" % columns)
        #content = [('flow', x) for x in map(self.convert_new_item, columns)]
        self.content = [urwid.Columns([self.convert_new_item(y) for y in x]) for x in columns]
        logging.debug("[ColumnWidget] init with content: %s" % self.content)
        urwid.ListBox.__init__(self, self.content)
        BaseWidgetClass.__init__(self)

    def convert_new_item(self, item):
        if not isinstance(item, (urwid.Text, urwid.AttrWrap)):
            item = urwid.Text("%s" % item)
        if not isinstance(item, urwid.AttrWrap):
            item = urwid.AttrWrap(item, None, 'reveal focus')
        return item

    def get_current_position(self):
        return self.get_focus()[1]

    def get_current_focus_column(self):
        return self.get_focus()[0].get_focus_column()

    def set_current_row_focus_column(self, column):
        self.get_focus()[0].set_focus_column(column)

    def get_current_column_len(self):
        return len(self.get_focus()[0].widget_list)

    def go_down(self):
        index = self.get_current_position()
        if index is None:
            return
        index += 1
        if index >= len(self.content):
            index = len(self.content) - 1
        self.set_focus(index)

    def go_up(self):
        index = self.get_current_position()
        if index is None:
            return
        index -= 1
        if index < 0:
            index = 0
        self.set_focus(index)
