#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IterClass(object):
    """
    Iterable class.

    Args:
        values (list[object] or tuple(object)): list of values

    Raises:
        TypeError: @values is not a list/tuple
    """

    def __init__(self, values):
        if not isinstance(values, (list, tuple)):
            raise TypeError("@values must be a list or tuple.")
        self._values = values

    def __iter__(self):
        yield from self._values


if __name__ == "__main__":
    iteration = IterClass(["a", "ab", "abc", "bb", "cc"])
    print([v for v in iteration if "a" in v])
