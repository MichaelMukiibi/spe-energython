"""OPEX model: fuel, fixed/variable O&M, insurance."""
from __future__ import annotations


def annual_opex(cfg, year, fuel_mmbtu, net_generation_mwh, total_capex_usd):
    """Operating-year OPEX.

    Fuel price is DELIVERED (includes CNG compression/trucking). Escalation on
    fuel and O&M; insurance is % of original CAPEX per year.
    """
    fu = cfg["fuel"]
    op = cfg["opex"]
    inf = cfg["financing"]["inflation_pct"] / 100.0  # escalation on cost lines
    fu_esc = (1.0 + fu["price_escalation_pct_per_yr"] / 100.0) ** (year - 1)
    om_esc = (1.0 + op["om_escalation_pct_per_yr"] / 100.0) ** (year - 1)

    fuel_cost = fuel_mmbtu * fu["price_usd_per_mmbtu"] * fu_esc
    fixed_om = cfg["plant"]["net_capacity_mw"] * 1000.0 * op["fixed_om_usd_per_kw_yr"] * om_esc
    variable_om = net_generation_mwh * op["variable_om_usd_per_mwh"] * om_esc
    insurance = total_capex_usd * op["insurance_pct_of_capex_per_yr"] / 100.0

    return {
        "year": year,
        "fuel_cost_usd": fuel_cost,
        "fixed_om_usd": fixed_om,
        "variable_om_usd": variable_om,
        "insurance_usd": insurance,
        "total_opex_usd": fuel_cost + fixed_om + variable_om + insurance,
    }