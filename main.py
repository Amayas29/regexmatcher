# -*- coding: utf-8 -*-

from regex import match
import re

text = "AZdslkn jzobc zejk cj evco bc oazebucodib z"
regex = "a?c?d?"


m = re.match(regex, text)
m = "None" if m is None else m.group(0)
print("." + m + ".", sep="")

if match(text, regex):
    print(f"{text} match the regex {regex}")

else:
    print(f"{text} doesn't match the regex {regex}")
