#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import covsirphy as cs


def md(scenario, filename, columns=None, name=None):
    with open(filename, "w") as fh:
        fh.write(scenario.summary(columns=columns, name=name).to_markdown())


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
    # Separate 0th phase
    snl.separate("01Apr2020")
    md(snl, "trend.md", name="Main")
    # Parameter estimation
    snl.estimate(cs.SIRF)
    est_cols = ["Start", "End", "Rt", *cs.SIRF.PARAMETERS, "RMSLE"]
    md(snl, "estimate.md", columns=est_cols, name="Main")
    # New
    snl.clear(name="New", template="Main")
    cols = ["Start", "End", "Rt", *cs.SIRF.PARAMETERS]
    md(snl, "new1.md", columns=cols)
    snl.delete(name="New")
    md(snl, "new2.md", columns=cols)
    # Main
    snl.add(end_date="31Dec2020", name="Main")
    md(snl, "main1.md", columns=cols)
    snl.add(days=100, name="Main")
    md(snl, "main2.md", columns=cols)
    # Medicine
    snl.clear(name="Medicine", template="Main")
    snl.add(end_date="31Dec2020", name="Medicine")
    sigma_last = snl.get("sigma", phase="last", name="Main")
    sigma_med = sigma_last * 2
    print(round(sigma_last, 3), round(sigma_med, 3))
    snl.add(sigma=sigma_med, days=100, name="Medicine")
    md(snl, "med1.md", columns=cols, name="Medicine")
    snl.add(days=30, name="Medicine")
    snl.delete(phases=["last"], name="Medicine")
    md(snl, "med2.md", columns=cols, name="Medicine")
    # History
    snl.history("sigma", filename="sigma.jpg")
    snl.history("Rt", filename="rt.jpg")
    snl.history("Infected", filename="infected.jpg")
    with open("describe.md", "w") as fh:
        fh.write(snl.describe().to_markdown())
    with open("simulate.md", "w") as fh:
        fh.write(snl.track().tail().to_markdown())


if __name__ == "__main__":
    main()
