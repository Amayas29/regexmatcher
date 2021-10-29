# -*- coding: utf-8 -*-

from src.regex import match

text = "AZdslkn jzobc zejk cj evco bc oazebucodib z"
regex = "a?c?d?"


if match(text, regex):
    print(f"{text} match the regex {regex}")

else:
    print(f"{text} doesn't match the regex {regex}")
