import logging
from irenicurse.widget import FullListWidget, link_to_key
from irenicurse import run

class TestFullListWidget(FullListWidget):
    @link_to_key("a")
    def testeu(self):
        self.call(TestFullListWidget("ceci est du chocolat au lait".split()))

    @link_to_key("r")
    def testeu2(self):
        self.call(TestFullListWidget("taratata pouet pouet".split()))

    @link_to_key("d")
    def test_delete(self):
        self.delete(self.get_current_position())

    @link_to_key("z")
    def test_append(self):
        self.append("qsd qsd")

    @link_to_key("e")
    def show_focus(self):
        logging.debug("%s" % [self.get_focus()])

    @link_to_key("t")
    def test_insert(self):
        self.insert("caca pouet pouet")


class TestMenuWidget(FullListWidget):
    widgets_to_test = (
         ("FullListWidget", (TestFullListWidget, "ceci est une liste de test".split())),
    )

    def __init__(self):
        FullListWidget.__init__(self, zip(*self.widgets_to_test)[0])

    @link_to_key("enter")
    def test_widget(self):
        data = dict(self.widgets_to_test)[self.get_current_item()]
        class_to_spawn = data[0]
        self.call(class_to_spawn(data[1][1:]))


if __name__ == "__main__":
    logging.debug("[main] start")
    run(TestMenuWidget())
    logging.debug("[main] end\n------------------------------\n\n\n")
    logging.debug("\n" * 200)
