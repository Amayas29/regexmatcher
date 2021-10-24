# -*- coding: utf-8 -*-

class Transition:

    def __init__(self, src_state, tag, dest_state, if_transition=None):
        self.src_state = src_state
        self.tag = tag
        self.dest_state = dest_state
        self.if_transition = False if if_transition is None else if_transition

    def __eq__(self, other):
        return type(self) == type(other) and self.tag == other.tag and self.dest_state == other.dest_state and self.src_state == other.src_state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.src_state} -{self.tag}-> {self.dest_state}"
