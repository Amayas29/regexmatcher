# -*- coding: utf-8 -*-

class State:

    cpt = 0

    def __init__(self, init, fin):
        self.id = State.cpt
        State.cpt += 1
        self.init = init
        self.fin = fin
        self.label = str(self.id)

    def __repr__(self):
        rep = self.label

        if self.init:
            rep = f"{rep}(initial)"

        if self.fin:
            rep = f"{rep}(final)"

        return rep

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if type(self.id) == int:
            return self.id

        s = str(self.id)

        res = ''.join(str(ord(c)) for c in s)
        return int(res)

    @staticmethod
    def contains_initial(list):
        for s in list:
            if s.init:
                return True

        return False

    @staticmethod
    def contains_final(list):
        for s in list:
            if s.fin:
                return True

        return False
