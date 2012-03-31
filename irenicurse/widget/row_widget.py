import urwid


class RowTextWidget(urwid.AttrMap):
    def __init__(self, data, highligh_colour='reveal focus', prefix="", suffix=""):
        self.data = data
        self.highligh_colour = highligh_colour
        self.prefix = prefix
        self.suffix = suffix
        urwid.AttrMap.__init__(self, urwid.Text(self.format_data(self.data)), None, highligh_colour)

    def format_data(self, text):
        return self.prefix + text + self.suffix
