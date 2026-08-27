"""Project and equity cash-flow waterfall."""

from __future__ import annotations

import numpy as np


def build_cashflows(cfg, revenue_df, opex_df, capex, debt, horizon):
    """Assemble year-0..horizon cash-flow arrays.

    Timeline: CAPEX drawn at year 0, operations years 1..horizon.
    project_cf  = revenue - opex - tax  (pre-financing, levered-before-debt view)
    equity_cf   = project_cf - debt_service  (post-financing)
    Depreciation: straight line over depreciation_years on the full CAPEX.
    """
    tax_rate = cfg["tax"]["corporate_rate"]
    dep_years = cfg["tax"]["depreciation_years"]
    salvage = cfg["tax"]["salvage_value_ratio"] * capex

    dep_per_year = (capex - salvage) / dep_years
    revenue = np.zeros(horizon + 1)
    opex = np.zeros(horizon + 1)
    ebitda = np.zeros(horizon + 1)
    depreciation = np.zeros(horizon + 1)
    ebt = np.zeros(horizon + 1)
    tax = np.zeros(horizon + 1)
    project_cf = np.zeros(horizon + 1)
    equity_cf = np.zeros(horizon + 1)

    project_cf[0] = -capex
    equity_cf[0] = -(capex - debt.principal)

    schedule = debt.schedule(horizon)
    debt_service = schedule["total_debt_service_usd"]
    dscr = np.zeros(horizon + 1)

    for yr in range(1, horizon + 1):
        rev = float(revenue_df.loc[yr, "total_revenue_usd"])
        opx = float(opex_df.loc[yr, "total_opex_usd"])
        revenue[yr] = rev
        opex[yr] = opx
        ebitda[yr] = rev - opx
        depreciation[yr] = dep_per_year if yr <= dep_years else 0.0
        ebt[yr] = max(
            ebitda[yr] - depreciation[yr] - schedule["interest_payment_usd"][yr], 0.0
        )
        tax[yr] = ebt[yr] * tax_rate
        project_cf[yr] = ebitda[yr] - tax[yr]
        equity_cf[yr] = project_cf[yr] - debt_service[yr]
        if debt_service[yr] > 0:
            dscr[yr] = ebitda[yr] / debt_service[yr]

    return {
        "capex_usd": capex,
        "revenue_usd": revenue,
        "opex_usd": opex,
        "ebitda_usd": ebitda,
        "depreciation_usd": depreciation,
        "tax_usd": tax,
        "project_cashflow_usd": project_cf,
        "equity_cashflow_usd": equity_cf,
        "debt_service_usd": debt_service,
        "interest_usd": schedule["interest_payment_usd"],
        "principal_usd": schedule["principal_payment_usd"],
        "outstanding_usd": schedule["outstanding_usd"],
        "dscr": dscr,
        "equity_invested_usd": -(equity_cf[0]),
    }
