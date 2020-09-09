#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import covsirphy as cs


def main():
    print(cs.__version__)
    pprint(cs.SIRF.EXAMPLE, compact=True)
    # Reproduction number
    eg_dict = cs.SIRF.EXAMPLE.copy()
    model_ins = cs.SIRF(
        population=eg_dict["population"],
        **eg_dict["param_dict"]
    )
    print(model_ins.calc_r0())
    # Set tau value and start date of records
    example_data = cs.ExampleData(tau=1440, start_date="01Jan2020")
    # Add records with SIR model
    model = cs.SIRF
    area = {"country": "Full", "province": model.NAME}
    example_data.add(model, **area)
    # Change parameter values if needed
    # example_data.add(model, param_dict={"kappa": 0.001, "kappa": 0.002, "rho": 0.4, "sigma": 0.0150}, **area)
    # Records with model variables
    df = example_data.specialized(model, **area)
    # Plotting
    cs.line_plot(
        df.set_index("Date"),
        title=f"Example data of {model.NAME} model",
        y_integer=True,
        filename="sirf.png"
    )


if __name__ == "__main__":
    main()
