import urwid

from row_widget import RowTextWidget, RowSectionTextWidget


def wrap_item_into_widget(item):
    if not isinstance(item, (urwid.AttrWrap, RowTextWidget)):
        item = RowTextWidget(item)
    return item


def wrap_line_into_column(line, item_factory=wrap_item_into_widget):
    return urwid.Columns(map(item_factory, line))


def section_list_factory(items):
    result = []
    for item in items:
        result += [RowSectionTextWidget(item, colour="title", walkable=False)]
        result += [RowSectionTextWidget(x, prefix="    ") for x in item.childs] if item.childs else [RowTextWidget("empty", prefix=" ", colour="light blue")]
        result += [RowTextWidget("", walkable=False)]
    result.pop()
    return result
