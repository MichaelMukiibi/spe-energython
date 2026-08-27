"""Return metrics: NPV, IRR, payback, simple LCOE."""

from __future__ import annotations

import numpy as np


def npv(cashflows, rate):
    """NPV of a cash-flow array where index 0 is year 0 (today)."""
    cf = np.asarray(cashflows, dtype=float)
    years = np.arange(len(cf))
    return float(np.sum(cf / (1.0 + rate) ** years))


def irr(cashflows, lo=0.0, hi=1.0, tol=1e-9):
    """IRR by bisection on NPV (cash flow is the classic -out, +in shape)."""
    cf = np.asarray(cashflows, dtype=float)

    def f(r):
        return npv(cf, r)

    if f(lo) < 0 or f(hi) > 0:
        return float("nan")  # no single root in [0, 100%]
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def payback_years(cumulative_cf):
    """Interpolated payback on a cumulative cash-flow array (index 0 = year 0)."""
    cum = np.asarray(cumulative_cf, dtype=float)
    if cum[-1] < 0:
        return None
    for yr in range(1, len(cum)):
        if cum[yr] >= 0:
            prev, nxt = cum[yr - 1], cum[yr]
            return (yr - 1) + (-prev) / (nxt - prev)
    return None


def cumulative_cashflow(cashflows):
    return np.cumsum(np.asarray(cashflows, dtype=float))


def lcoe(cfg, capex, revenue_df, opex_df, discount_rate):
    """Levelized cost of electricity over the horizon.

    Sum of discounted CAPEX+OPEX / discounted generated MWh (annual).
    """
    horizon = cfg["project"]["horizon_years"]
    years = np.arange(0, horizon + 1)
    disc = (1.0 + discount_rate) ** years
    npv_costs = -capex
    npv_energy = 0.0
    for yr in range(1, horizon + 1):
        opx = float(opex_df.loc[yr, "total_opex_usd"])
        mwh = float(revenue_df.loc[yr, "dc_mwh"]) + float(
            revenue_df.loc[yr, "export_mwh"]
        )
        npv_costs += opx / disc[yr]
        npv_energy += mwh / disc[yr]
    return npv_costs / npv_energy if npv_energy > 0 else float("nan")


def summary_metrics(cfg, cashflows, revenue_df, opex_df, capex, discount_rate):
    """One-stop metrics dict for a run."""
    project_acf = cumulative_cashflow(cashflows["project_cashflow_usd"])
    equity = cashflows["equity_cashflow_usd"]
    equity_acf = cumulative_cashflow(equity)
    project_npv = npv(cashflows["project_cashflow_usd"], discount_rate)
    equity_npv = npv(equity, discount_rate)
    dscr_array = cashflows["dscr"][1:]
    metrics = {
        "project_npv_usd": project_npv,
        "equity_npv_usd": equity_npv,
        "project_irr_pct": irr(cashflows["project_cashflow_usd"]) * 100.0,
        "equity_irr_pct": irr(equity) * 100.0,
        "project_payback_years": payback_years(project_acf),
        "equity_payback_years": payback_years(equity_acf),
        "min_dscr": float(np.min(dscr_array[dscr_array > 0]))
        if np.any(dscr_array > 0)
        else None,
        "equity_invested_usd": cashflows["equity_invested_usd"],
        "capex_usd": capex,
        "lcoe_usd_per_mwh": lcoe(cfg, capex, revenue_df, opex_df, discount_rate),
    }
    return metrics
