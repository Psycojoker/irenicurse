from UserList import UserList


class SectionList(UserList):
    def __init__(self, the_list):
        self.data = []
        for item in the_list:
            self.data.append(Section(item))


class Section(object):
    def __init__(self, item):
        self.title = item[0]
        self.childs = [SectionChild(x, self) for x in item[1]]


class SectionChild(object):
    def __init__(self, title, father):
        self.title = title
        self.father = father
