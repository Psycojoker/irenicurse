import urwid

from row_widget import RowTextWidget


def wrap_item_into_widget(item):
    if not isinstance(item, (urwid.AttrWrap, RowTextWidget)):
        item = RowTextWidget(item)
    return item


def wrap_line_into_column(line, item_factory=wrap_item_into_widget):
    return urwid.Columns(map(item_factory, line))


