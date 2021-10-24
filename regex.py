# -*- coding: utf-8 -*-

from automaton import Automaton
from state import State
from transition import Transition


def to_automaton(regex: str):

    auto = Automaton([])
    init = State(True, False)
    auto.add_state(init)

    end_word = False
    if regex[-1] == "$":
        end_word = True
        regex = regex[:-1]

    if regex[0] != "^":
        auto.add_transition(Transition(init, "", init))
    else:
        regex = regex[1:]

    regex = regex.split("|")

    for r in regex:
        to_automaton_unit(auto, init, r, end_word)

    return auto


def __create_stack(regex):

    stack = []
    number = 0
    number_min = 0
    comma = False
    max = False

    for i in range(len(regex)):

        c = regex[i]

        if c.isalpha():
            stack.append((c, ''))
            continue

        if c == "*":
            value = stack.pop()
            stack.append((value[0], '*'))
            continue

        if c == "+":
            value = stack.pop()
            stack.append((value[0], '+'))
            continue

        if c == "?":
            value = stack.pop()
            stack.append((value[0], '?'))
            continue

        if c.isdigit():
            number = number * 10 + int(c)
            continue

        if c == "}":
            value = stack.pop()

            if not comma:
                number_min = number
            if max:
                number = "*"

            stack.append((value[0], f"{number_min},{number}"))
            number = 0
            comma = False
            continue

        if c == ',':
            comma = True
            number_min = number
            number = 0
            if regex[i+1] == "}":
                max = True

    return stack


def get_literal(auto, letter, init):
    next = State(False, False)
    auto.add_transition(Transition(init, letter, next))

    return next


def get_star(auto, letter, init):
    auto.add_transition(Transition(init, letter, init))


def get_plus(auto, letter, init):
    next = State(False, False)
    auto.add_transition(Transition(init, letter, next))
    auto.add_transition(Transition(next, letter, next))

    return next


def get_once_or_none(auto, letter, init):
    inter = State(False, False)
    auto.add_transition(Transition(init, letter, inter, True))

    return inter


def get_numbers(auto, letter, init, min_value, max_value, i, stack, n, end_word):
    for _ in range(min_value):
        next = State(False, False)
        auto.add_transition(Transition(init, letter, next))
        init = next

    if max_value == "*":
        auto.add_transition(Transition(init, letter, init))
        i += 1
        return False, init

    rest = int(max_value) - min_value
    inc = False
    next = State(False, False)

    if (i != n - 1):
        auto.add_transition(Transition(init, stack[i+1][0], next))
        inc = True
        if stack[i+1][1] == "?":
            init.fin = True
            if not end_word:
                auto.add_transition(Transition(init, "", init))
    else:
        init.fin = True
        if not end_word:
            auto.add_transition(Transition(init, "", init))

    for j in range(rest):

        curr = init

        for _ in range(j+1):
            inter = State(False, False)
            auto.add_transition(Transition(curr, letter, inter))
            curr = inter

        if (i != n - 1):
            auto.add_transition(Transition(curr, stack[i+1][0], next))
            inc = True

        else:
            curr.fin = True
            if not end_word:
                auto.add_transition(Transition(curr, "", curr))

    return inc, next


def to_automaton_unit(auto, init, regex, end_word):

    stack = __create_stack(regex)
    n = len(stack)
    i = 0
    finals = []
    only_once = True

    while i < n:

        value = stack[i]

        if value[1] == '':
            init = get_literal(auto, value[0], init)
            only_once = False

        elif value[1] == '*':
            get_star(auto, value[0], init)
            only_once = False

        elif value[1] == '+':
            init = get_plus(auto, value[0], init)
            only_once = False

        elif value[1] == "?":
            init = get_once_or_none(auto, value[0], init)
            finals.append(init)
        else:
            only_once = False
            values = value[1].split(",")
            min_value = int(values[0])
            max_value = values[1]

            inc, init = get_numbers(auto, value[0], init,
                                    min_value, max_value, i, stack, n, end_word)
            if inc:
                i += 1

        i += 1

    if only_once:
        for f in finals:
            f.fin = True
            if not end_word:
                auto.add_transition(Transition(f, "", f))
    else:
        init.fin = True
        if not end_word:
            auto.add_transition(Transition(init, "", init))


def match(text, regex):
    auto = to_automaton(regex)
    auto.show("auto")
    return Automaton.execute(auto, text)


if __name__ == "__main__":

    to_automaton("^am*y{2,}k|JD+dd*as{2,3}|s?a?n?$").show("auto")
