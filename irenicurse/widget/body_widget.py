import urwid
import logging

import factories
from base import BaseWidgetClass
from decorator import bind_to_key
from section_widget_data_structures import Section, SectionList, SectionChild


class ListWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, content, factory=factories.wrap_item_into_widget, index=0):
        logging.debug("[ListWidget] init with content: %s" % list(content))
        BaseWidgetClass.__init__(self)
        self.factory = factory
        self.content = map(self.factory, content)
        urwid.ListBox.__init__(self, self.content)
        self.set_focus(index)

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
        self.content.append(self.factory(new_item))

    def delete(self, position=None):
        if position is None:
            position = self.get_current_position()
        logging.debug("[%s] going to delete item at position: %s" %
                      (self.__class__, position))
        if position is not None:
            self.content.pop(position)

    def get_current_position(self):
        return self.get_focus()[1]

    def get_current_widget(self):
        return self.get_focus()[0]

    def get_current_item(self):
        return self.get_focus()[0]._original_widget.get_text()[0]

    def insert(self, new_item, position=None):
        if position is None:
            position = self.get_current_position()
            if position is None:
                position = 0
        logging.debug("[%s] going to insert item at position: %s" %
                      (self.__class__, position))
        self.content.insert(position, self.factory(new_item))


class FullListWidget(ListWidget):
    "poeut pouet"
    @bind_to_key("q")
    def quit(self):
        ListWidget.quit(self)

    @bind_to_key("down")
    @bind_to_key("j")
    def go_down(self):
        ListWidget.go_down(self)
        logging.debug("%s" % [self.get_focus()])

    @bind_to_key("up")
    @bind_to_key("k")
    def go_up(self):
        """foobar"""
        ListWidget.go_up(self)
        logging.debug("%s" % [self.get_focus()])

class ColumnWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, columns, factory=factories.wrap_line_into_column):
        logging.debug("[ColumnWidget] constructor received data: %s" % columns)
        self.factory = factory
        self.content = map(self.factory, columns)
        logging.debug("[ColumnWidget] init with content: %s" % self.content)
        urwid.ListBox.__init__(self, self.content)
        BaseWidgetClass.__init__(self)

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
        column = self.get_current_focus_column()
        if index is None:
            return
        index += 1
        if index >= len(self.content):
            index = len(self.content) - 1
        self.set_focus(index)
        self.set_current_row_focus_column(column) if column < self.get_current_column_len() else self.set_current_row_focus_column(self.get_current_column_len() - 1)

    def go_up(self):
        index = self.get_current_position()
        column = self.get_current_focus_column()
        if index is None:
            return
        index -= 1
        if index < 0:
            index = 0
        self.set_focus(index)
        self.set_current_row_focus_column(column) if column < self.get_current_column_len() else self.set_current_row_focus_column(self.get_current_column_len() - 1)

    def go_left(self):
        row = self.get_focus()[0]
        if row is None:
            return
        column = row.get_focus_column()
        if column is None or column == 0:
            return
        column -= 1
        row.set_focus_column(column)

    def go_right(self):
        row = self.get_focus()[0]
        if row is None:
            return
        column = row.get_focus_column()
        if column is None or column == len(row.widget_list) - 1:
            return
        column += 1
        row.set_focus_column(column)


class FullColumnWidget(ColumnWidget):
    @bind_to_key("q")
    def quit(self):
        ColumnWidget.quit(self)

    @bind_to_key("down")
    @bind_to_key("j")
    def go_down(self):
        ColumnWidget.go_down(self)
        logging.debug("%s" % [self.get_focus()])

    @bind_to_key("up")
    @bind_to_key("k")
    def go_up(self):
        ColumnWidget.go_up(self)
        logging.debug("%s" % [self.get_focus()])

    @bind_to_key("left")
    @bind_to_key("h")
    def go_left(self):
        ColumnWidget.go_left(self)
        logging.debug("%s" % [self.get_focus()])

    @bind_to_key("right")
    @bind_to_key("l")
    def go_right(self):
        ColumnWidget.go_right(self)
        logging.debug("%s" % [self.get_focus()])


class SectionListWidget(urwid.ListBox, BaseWidgetClass):
    def __init__(self, content, factory=factories.section_list_factory, index=1):
        logging.debug("[SectionListWidget] init with content: %s" % list(content))
        BaseWidgetClass.__init__(self)
        self.structured_data = SectionList(content)
        self.factory = factory
        self.content = self.factory(self.structured_data)
        urwid.ListBox.__init__(self, self.content)
        self.set_focus(index)

    def go_up(self):
        index = self.get_current_position()
        if index is None:
            return
        index -= 1
        if index < 1:
            index = 1
        self.set_focus(index)
        if not self.get_current_widget().walkable and index != 1:
            self.go_up()

    def go_down(self):
        index = self.get_current_position()
        if index is None:
            return
        index += 1
        if index >= len(self.content):
            index = len(self.content) - 1
        self.set_focus(index)
        if not self.get_current_widget().walkable and index != len(self.content) - 1:
            self.go_down()
