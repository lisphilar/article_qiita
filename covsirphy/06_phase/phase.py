#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
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
    md(snl, "trend.md", "Main")
    # Disable
    snl.clear(name="A")
    snl.disable(phases=["0th", "3rd"], name="A")
    md(snl, "A.md", "A")
    snl.enable(phases=["0th"], name="A")
    md(snl, "A2.md", "A")
    # Combine
    snl.clear(name="B")
    snl.combine(phases=["1st", "5th"], name="B")
    md(snl, "B.md", "B")
    # Delete 0th phase
    snl.clear(name="C")
    snl.delete(phases=["0th"], name="C")
    md(snl, "C.md", "C")
    snl.enable(phases=["0th"], name="C")
    md(snl, "C2.md", "C2")
    # Delete 3rd phase
    snl.clear(name="D")
    snl.delete(phases=["3rd"], name="D")
    md(snl, "D.md", "D")
    # Delete last phase
    snl.clear(name="E")
    snl.delete(phases=["6th", "7th"], name="E")
    md(snl, "E.md", "E")
    # Add phase with end_date
    snl.add(end_date="31Aug2020", name="E")
    md(snl, "E2.md", "E")
    # Add phase with days
    snl.add(days=10, name="E")
    md(snl, "E3.md", "E")
    # Add phase with end_date=None and days=None
    snl.add(name="E")
    md(snl, "E4.md", "E")
    # Separate
    snl.clear(name="F", template="E")
    snl.separate(date="01Apr2020", name="F")
    md(snl, "F.md", "F")
    # Change
    snl.clear(name="G", template="F")
    snl.combine(phases=["0th", "1st"], name="G")
    snl.separate(date="12Apr2020", name="G")
    md(snl, "G.md", "G")
    # Optimize change point
    candidates = ["01Mar2020", "12Apr2020"]
    opt_dict = {date: {} for date in candidates}
    snl_opt = cs.Scenario(jhu_data, population_data, country="Japan", tau=720)
    snl_opt.trend(show_figure=False)
    for date in candidates:
        snl_opt.clear(name=date)
        snl_opt.combine(phases=["0th", "1st"], name=date)
        snl_opt.separate(date=date, name=date)
        snl_opt.estimate(cs.SIRF, phases=["0th", "1st"], name=date)
        opt_dict[date]["0th"] = snl_opt.get("RMSLE", phase="0th", name=date)
        opt_dict[date]["1st"] = snl_opt.get("RMSLE", phase="1st", name=date)
    with open("opt.md", "w") as fh:
        df = pd.DataFrame.from_dict(opt_dict, orient="index")
        fh.write(df.to_markdown())


if __name__ == "__main__":
    main()
