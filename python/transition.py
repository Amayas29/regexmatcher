# -*- coding: utf-8 -*-

class Transition:

    def __init__(self, src_state, tag, dest_state):
        self.src_state = src_state
        self.tag = tag
        self.dest_state = dest_state

    def __eq__(self, other):
        return type(self) == type(other) and self.tag == other.tag and self.dest_state == other.dest_state and self.src_state == other.src_state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.src_state} -{self.tag}-> {self.dest_state}"
