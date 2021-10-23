# -*- coding: utf-8 -*-

from regex import match

text = "ama"
regex = "a?x?d?"

if match(text, regex):
    print(f"{text} match the regex {regex}")

else:
    print(f"{text} doesn't match the regex {regex}")
