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

    def enable(self):
        """
        Enable the unit.
        """
        self._enabled = True

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

    def _validate_index(self, num):
        """
        Validate the index number.

        Args:
            num (int): index number of a unit

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        if not isinstance(num, int):
            raise TypeError(
                f"@num must be integer, but {num} was applied.")
        try:
            self._units[num]
        except IndexError:
            raise IndexError(f"@num must be under {len(self._units)}")

    def enable(self, num):
        """
        Enable a unit.

        Args:
            num (int): index of the unit to be enabled

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        self._validate_index(num)
        self._units[num].enable()

    def disable(self, num):
        """
        Disable a unit.

        Args:
            num (int): index of the unit to be disabled

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        self._validate_index(num)
        self._units[num].disable()


def show_enabled(series):
    """
    Show the values of enabled units.
    """
    if not isinstance(series, Series):
        raise TypeError("@unit must be a instance of Series")
    print([unit.value for unit in series if unit])


if __name__ == "__main__":
    # Unit class
    unit1 = Unit(value=1.0)
    if unit1:
        print(unit1.value)
    unit1.disable()
    if unit1:
        print("Disabled")
        print(unit1.value)
    unit1.enable()
    if unit1:
        print("Enabled")
        print(unit1.value)
    # Create a series of units
    series = Series()
    [series.add(Unit(i)) for i in range(6)]
    show_enabled(series)
    # Disable two units
    series.disable(4)
    series.disable(5)
    show_enabled(series)
    # Enable one disabled unit
    series.enable(4)
    show_enabled(series)
