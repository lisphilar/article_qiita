#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IterClass(object):
    """
    Iterable class.

    Args:
        values (list[int]): list of values
    """

    def __init__(self, values):
        self._values = values

    def __iter__(self):
        yield from self._values


if __name__ == "__main__":
    iteration = IterClass(["a", "ab", "abc", "bb", "cc"])
    print([v for v in iteration if "a" in v])
