# -*- coding: utf-8 -*-

import os
from src.state import State


class Automaton:

    def __init__(self, list_transitions, list_states=None):

        self.list_transitions = list_transitions
        self.list_states = list_states

        if self.list_states is None:
            self.list_states = []
            self.list_states = self._get_list_states()

    def _get_list_states(self):
        states = set(self.list_states)

        for t in self.list_transitions:
            states = states | {t.src_state, t.dest_state}

        return list(states)

    def add_transition(self, transition):

        if transition not in self.list_transitions:
            self.list_transitions.append(transition)

            if transition.src_state not in self.list_states:
                self.list_states.append(transition.src_state)
            if transition.dest_state not in self.list_states:
                self.list_states.append(transition.dest_state)

            return True

        return False

    def remove_transition(self, transition):

        if transition in self.list_transitions:
            self.list_transitions.remove(transition)
            return True

        return False

    def add_state(self, state):

        if state not in self.list_states:
            self.list_states.append(state)
            return True

        return False

    def remove_state(self, state):

        if state in self.list_states:

            transitions = [t for t in self.list_transitions]

            for t in transitions:
                if t.src_state == state or t.dest_state == state:
                    self.remove_transition(t)

            self.list_states.remove(state)
            return True

        return False

    def get_list_initial_states(self):
        return list(filter(lambda s: s.init, self.list_states))

    def get_list_final_states(self):
        return list(filter(lambda s: s.fin, self.list_states))

    def get_list_transitions_from(self, state):

        list = []

        if state in self.list_states:
            list += filter(lambda t: t.src_state ==
                           state, self.list_transitions)

        return list

    def succ_elem(self, state, letter, matched):

        succs = []
        forward = True

        for t in self.get_list_transitions_from(state):

            if (t.tag == letter or t.tag == "" or t.if_transition) and t.dest_state not in succs:
                succs.append(t.dest_state)
                if t.tag != "" or (t.if_transition and t.tag == letter):
                    matched += 1

        return succs, matched

    def succ_list_state(self, list_states, letter, matched):

        succs_by_letter = set()

        for state in list_states:

            l, matched = self.succ_elem(state, letter, matched)
            succs_by_letter = succs_by_letter.union(l)

        return list(succs_by_letter), matched

    @ staticmethod
    def execute(auto, word):

        matched = 0
        list_states = auto.get_list_initial_states()

        for letter in word:
            list_states, matched = auto.succ_list_state(
                list_states, letter, matched)

        return State.contains_final(list_states), matched

    # DEBUG

    def __str__(self) -> str:
        return f"{self.list_states} : {self.list_transitions}"

    def toDot(self):
        """-> str
        rend une description de l'automate au format dot qui sera
        appelée par la fonction show
        """
        # ret : str
        ret = "digraph a { \n graph [rotate = 90];\n rankdir=LR\n"
        # state : State
        for state in self.list_states:
            ret += str(state.id) + "[ label =\"" + str(state.label) + "\","
            # Test pour savoir si l'etat est initial et/ou final
            if state.init:
                ret += " color=red "
            if state.fin:
                ret += "peripheries=2 "
            ret += "];\n"

            # Ecriture des transitions depuis l'etat
            # liste : list[Transition]
            liste = list(self.get_list_transitions_from(state))
            # trans : liste[Transition]
            for trans in liste:
                # etiq : str
                etiq = trans.tag
                # listToRemove : list[Transition]
                listToRemove = []
                # t : Transition
                for t in liste:
                    if t.dest_state.id == trans.dest_state.id and t.tag != trans.tag:
                        etiq = etiq + " , " + t.tag
                        listToRemove.append(t)
                for t in listToRemove:
                    liste.remove(t)
                ret += str(trans.src_state.id) + " -> " + \
                    str(trans.dest_state.id)
                ret += " [ label = \"" + etiq + "\" ];\n"
        # Fin de l'automate
        ret += "}\n"
        # print(ret)
        return ret

    def show(self, nomFichier):
        """ str ->
        Produit un fichier pdf donnant une représentation graphique de l'automate
        Erreur si l'impression s'est mal passée
        """
        try:
            # fichier : File
            fichier = open(nomFichier + ".dot", "w")
            fichier.write(self.toDot())
            fichier.close()
            # os.system("dot -Tps "+ nomFichier + ".dot -o " + nomFichier + ".ps" )
            # os.system("ps2pdf " + nomFichier + ".ps " + nomFichier + ".pdf")

            os.system("dot -Tpdf "+nomFichier +
                      ".dot -o " + nomFichier + ".pdf")
            # WINDOWS
            # os.system("start " + nomFichier + ".pdf")
            # MAC
            # os.system("open " + nomFichier + ".pdf")
            # LINUX
            os.system("evince " + nomFichier + ".pdf &")
            os.system("rm " + nomFichier + ".dot ")  # + nomFichier + ".ps")

        except IOError:
            print("Impossible de creer le fichier .dot")
