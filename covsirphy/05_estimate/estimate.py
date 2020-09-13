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
    snl.records(filename="records.jpg")
    # S-R trend analysis
    snl.trend(filename="trend.jpg")
    # Summary
    with open("summary.md", "w") as fh:
        fh.write(snl.summary().to_markdown())
    # Parameter estimation
    snl.estimate(cs.SIRF)
    with open("summary_estimated.md", "w") as fh:
        fh.write(snl.summary().to_markdown())
    # Parameters
    with open("summary_param.md", "w") as fh:
        cols = ["Start", "End", "ODE", "tau", *cs.SIRF.PARAMETERS]
        fh.write(snl.summary(columns=cols).to_markdown())
    snl.history(target="theta", filename="theta.jpg")
    snl.history(target="kappa", filename="kappa.jpg")
    snl.history(target="rho", filename="rho.jpg")
    snl.history(target="sigma", filename="sigma.jpg")
    # Day-parameters
    with open("summary_param_day.md", "w") as fh:
        cols = ["Start", "End", "ODE", "tau", *cs.SIRF.DAY_PARAMETERS]
        fh.write(snl.summary(columns=cols).to_markdown())
    snl.history(target="1/beta [day]", filename="beta.jpg")
    # Rt
    with open("summary_rt.md", "w") as fh:
        cols = ["Start", "End", "ODE", "Rt"]
        fh.write(snl.summary(columns=cols).to_markdown())
    snl.history(target="Rt", filename="rt.jpg")
    # Accuracy
    with open("summary_accuracy.md", "w") as fh:
        cols = ["Start", "End", "RMSLE", "Trials", "Runtime"]
        fh.write(snl.summary(columns=cols).to_markdown())
    snl.estimate_accuracy(phase="0th", filename="accuracy_0th.jpg")
    snl.estimate_accuracy(phase="6th", filename="accuracy_6th.jpg")


if __name__ == "__main__":
    main()
