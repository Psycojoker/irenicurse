import urwid


class RowTextWidget(urwid.AttrMap):
    def __init__(self, data, highligh_colour='reveal focus', prefix="", suffix="", walkable=True, colour=None):
        self.data = data
        self.highligh_colour = highligh_colour
        self.walkable = walkable
        self.prefix = prefix
        self.suffix = suffix
        urwid.AttrMap.__init__(self, urwid.Text(self.format_data(self.data)), colour, highligh_colour)

    def format_data(self, text):
        return self.prefix + text + self.suffix if self.prefix or self.suffix else text

    def update(self):
        self.original_widget.set_text(self.format_data(self.data))

class RowSectionTextWidget(RowTextWidget):
    def __init__(self, wrapped_data, *args, **kwargs):
        self.ref_to_object = wrapped_data
        RowTextWidget.__init__(self, wrapped_data.title, *args, **kwargs)
