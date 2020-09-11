#!/usr/bin/env python
# -*- coding: utf-8 -*-

import covsirphy as cs


def main():
    print(cs.__version__)
    # DataLoader
    data_loader = cs.DataLoader("input")
    # JHU data
    jhu_data = data_loader.jhu(verbose=True)
    print(type(jhu_data))
    print(data_loader.covid19dh_citation)
    print(jhu_data.raw.tail())
    with open("jhu_data_cleaned.md", "w") as fh:
        s = jhu_data.cleaned().tail().to_markdown()
        fh.write(s)
    with open("jhu_data_subset.md", "w") as fh:
        subset_df = jhu_data.subset(country="JPN", province="Tokyo")
        s = subset_df.tail().to_markdown()
        fh.write(s)
    cs.line_plot(
        subset_df.set_index("Date").drop("Confirmed", axis=1),
        title="Japan/Tokyo: cases over time",
        filename="jhu_data_subset.jpg", y_integer=True)
    with open("jhu_data_total.md", "w") as fh:
        s = jhu_data.total().tail().to_markdown()
        fh.write(s)
    # Population
    population_data = data_loader.population(verbose=True)
    print(type(population_data))
    with open("population_data_cleaned.md", "w") as fh:
        s = population_data.cleaned().tail().to_markdown()
        fh.write(s)
    print(population_data.value(country="JPN", province="Tokyo"))
    # OxCGRT
    oxcgrt_data = data_loader.oxcgrt()
    print(type(oxcgrt_data))
    with open("oxcgrt_data_cleaned.md", "w") as fh:
        s = oxcgrt_data.cleaned().tail().to_markdown()
        fh.write(s)
    with open("oxcgrt_data_subset.md", "w") as fh:
        s = oxcgrt_data.subset(country="Japan").tail().to_markdown()
        fh.write(s)


if __name__ == "__main__":
    main()
