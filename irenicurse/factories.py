import urwid

def wrap_item_into_widget(item):
    if not isinstance(item, (urwid.Text, urwid.AttrWrap)):
        item = urwid.Text(item)
    if not isinstance(item, urwid.AttrWrap):
        item = urwid.AttrWrap(item, None, 'reveal focus')
    return item
