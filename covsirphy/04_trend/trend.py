#!/usr/bin/env python
# -*- coding: utf-8 -*-

import covsirphy as cs


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
    df = snl.records(show_figure=False)
    with open("records.md", "w") as fh:
        fh.write(df.tail().to_markdown())
    snl.records(filename="records.jpg")
    # S-R trend analysis
    snl.trend(filename="trend.jpg")
    # Summary
    with open("summary.md", "w") as fh:
        fh.write(snl.summary().to_markdown())
    # Phase-dependent Rt
    snl.estimate(cs.SIRF)
    snl.history(target="Rt", filename="rt.jpg")


if __name__ == "__main__":
    main()
