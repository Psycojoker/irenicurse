# -*- encoding: utf-8 -*-

import logging
from irenicurse.widget import FullListWidget, bind_to_key, FullColumnWidget
from irenicurse import run

class TestFullListWidget(FullListWidget):
    @bind_to_key("a")
    def testeu(self):
        self.call(TestFullListWidget("ceci est du chocolat au lait".split()))

    @bind_to_key("r")
    def testeu2(self):
        self.call(TestFullListWidget("taratata pouet pouet".split()))

    @bind_to_key("d")
    def test_delete(self):
        self.delete(self.get_current_position())

    @bind_to_key("z")
    def test_append(self):
        self.append("qsd qsd")

    @bind_to_key("e")
    def show_focus(self):
        logging.debug("%s" % [self.get_focus()])

    @bind_to_key("t")
    def test_insert(self):
        self.insert("caca pouet pouet")

    @bind_to_key("y")
    def test_ask(self):
        self.ask(u"Nom du nouvel élément:", callback=self.test_ask_input)

    def test_ask_input(self, text):
        self.append(text)

    @bind_to_key("u")
    def test_yes_or_no(self):
        self.yes_or_no(u"Rajouter un élément ? [y/n]", self.test_yes_or_no_answer)

    def test_yes_or_no_answer(self, answer):
        if answer:
            self.append("un nouvel élément !")


class TestMenuWidget(FullListWidget):
    widgets_to_test = (
         ("FullListWidget", (TestFullListWidget, "ceci est une liste de test".split())),
         ("FullColumnWidget", (FullColumnWidget, ["a b c d".split(), "1 2 3 4".split(), "a z e r t y".split()])),
    )

    def __init__(self):
        FullListWidget.__init__(self, zip(*self.widgets_to_test)[0])

    @bind_to_key("enter")
    def test_widget(self):
        data = dict(self.widgets_to_test)[self.get_current_item()]
        class_to_spawn = data[0]
        self.call(class_to_spawn(data[1]))


if __name__ == "__main__":
    logging.debug("[main] start")
    run(TestMenuWidget())
    logging.debug("[main] end\n------------------------------\n\n\n")
    logging.debug("\n" * 200)
