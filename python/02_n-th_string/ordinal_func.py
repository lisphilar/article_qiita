#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict


def int2ordinal(num):
    """
    Convert a natural number to a ordinal number.

    Args:
        num (int): natural number

    Returns:
        str: ordinal number, like 0th, 1st, 2nd,...

    Notes:
        Zero can be used as @num argument.
    """
    if not isinstance(num, int):
        raise TypeError(
            f"@num must be integer, but {num} was applied.")
    if num < 0:
        raise ValueError(
            f"@num must be over 0, but {num} was applied.")
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    q, mod = divmod(num, 10)
    suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
    """
    if num % 100 == 11:
        suffix = "th"
    else:
        suffix = ordinal_dict[num % 10]
    """
    return f"{num}{suffix}"


if __name__ == "__main__":
    print(int2ordinal(0))
    print(int2ordinal(1))
    print(int2ordinal(2))
    print(int2ordinal(3))
    print(int2ordinal(4))
    print(int2ordinal(11))
    print(int2ordinal(21))
    print(int2ordinal(111))
    print(int2ordinal(121))
