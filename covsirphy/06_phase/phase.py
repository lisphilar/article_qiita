#!/usr/bin/env python
# -*- coding: utf-8 -*-

import covsirphy as cs


def md(scenario, filename, name=None):
    with open(filename, "w") as fh:
        fh.write(scenario.summary(name=name).to_markdown())


def main():
    print(cs.__version__)
    # Data loading
    data_loader = cs.DataLoader("input")
    jhu_data = data_loader.jhu(verbose=True)
    population_data = data_loader.population(verbose=True)
    # For Japan
    japan_data = data_loader.japan()
    jhu_data.replace(japan_data)
    print(japan_data.citation)
    # Records
    snl = cs.Scenario(jhu_data, population_data, country="Japan")
    snl.records(filename="records.jpg")
    # S-R trend analysis
    snl.trend(filename="trend.jpg")
    with open("trend.md", "w") as fh:
        fh.write(snl.summary().to_markdown())
    # Disable
    snl.clear(name="A")
    snl.disable(phases=["0th", "3rd"], name="A")
    md(snl, "A.md", "A")
    snl.enable(phases=["0th"], name="A")
    md(snl, "A2.md", "A")
    # Delete 0th phase
    snl.clear(name="B")
    snl.delete(phases=["0th"], name="B")
    md(snl, "B.md", "B")
    snl.enable(phases=["0th"], name="B")
    md(snl, "B2.md", "B2")
    # Delete 3rd phase
    snl.clear(name="C")
    snl.delete(phases=["3rd"], name="C")
    md(snl, "C.md", "C")
    # Delete last phase
    snl.clear(name="D")
    snl.delete(phases=["6th", "7th"], name="D")
    md(snl, "D.md", "D")
    # Add phase with end_date
    snl.add(end_date="31Aug2020", name="D")
    md(snl, "D2.md", "D")
    # Add phase with days
    snl.add(days=10, name="D")
    md(snl, "D3.md", "D")
    # Add phase with end_date=None and days=None
    snl.add(name="D")
    md(snl, "D4.md", "D")


if __name__ == "__main__":
    main()
