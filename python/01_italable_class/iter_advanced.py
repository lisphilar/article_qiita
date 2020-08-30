#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Unit(object):
    """
    The smallest unit.
    """

    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"@value must be integer or float value, but {value} was applied.")
        self._value = value
        self._enabled = True

    def __bool__(self):
        return self._enabled

    @property
    def value(self):
        """
        float: value of the unit
        """
        return self._value

    def disable(self):
        """
        Disable the unit.
        """
        self._enabled = False


class Series(object):
    """
    A series of units.
    """

    def __init__(self):
        self._units = []

    def __iter__(self):
        yield from self._units

    def add(self, unit):
        """
        Append a unit.

        Args:
            unit (Unit]): the smallest unit

        Raises:
            TypeError: unit is not an instance of Unit
        """
        if not isinstance(unit, Unit):
            raise TypeError("@unit must be a instance of Unit")
        self._units.append(unit)

    def disable(self, num):
        """
        Disable a unit.

        Args:
            num (int): index of the unit to be disabled

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        if not isinstance(num, int):
            raise TypeError(
                f"@num must be integer, but {num} was applied.")
        try:
            self._units[num].disable()
        except IndexError:
            raise IndexError(f"@num must be under {len(self._units)}")


if __name__ == "__main__":
    # Create a series of units
    series = Series()
    [series.add(Unit(i)) for i in range(10)]
    print([unit.value for unit in series if unit])
    # Disable two units
    series.disable(3)
    series.disable(5)
    print([unit.value for unit in series if unit])
