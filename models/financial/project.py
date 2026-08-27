"""End-to-end project run: profiles -> dispatch -> physical -> revenue -> opex
-> debt -> cash flows -> metrics, for a given config."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from models.loader import ROOT
from models.operational.dispatch import availability_mask
from models.physical.combined_cycle import run_hourly
from models.financial.capex import capex_build_up
from models.financial.revenue import annual_revenue
from models.financial.opex import annual_opex
from models.financial.financing import DebtSchedule
from models.financial.cashflow import build_cashflows
from models.financial.returns import summary_metrics


def load_profile_mw(cfg, phase_key, scenario, root=ROOT):
    """Load a phase+scenario hourly facility-load profile (MW)."""
    base = cfg["dc_ramp"][phase_key]["profile_base"]
    path = Path(root) / cfg["data_center"]["phase_profiles_dir"] / f"{base}_{scenario}.csv"
    df = pd.read_csv(path)
    return (df["facility_load_kw"].to_numpy(dtype=float) / 1000.0).astype(float)


def operating_years_by_phase(cfg):
    """Map operating year -> dc_ramp phase key. years: [start, end] inclusive."""
    out = {}
    for phase_key, spec in cfg["dc_ramp"].items():
        start, end = spec["years"]
        for yr in range(start, end + 1):
            out[yr] = phase_key
    return out


def run_project(cfg, load_scenario=None, dispatch_mode=None, capex_multiplier=1.0):
    """Run the full 20-yr model.

    Returns a dict holding metrics, cash-flow arrays, DataFrames, and the
    final-year hourly model for plotting.
    """
    horizon = cfg["project"]["horizon_years"]
    scenario = load_scenario or cfg["data_center"]["baseline_load_scenario"]
    mode = dispatch_mode or cfg["ppa"]["dispatch_mode"]

    years_by_phase = operating_years_by_phase(cfg)
    if set(years_by_phase) != set(range(1, horizon + 1)):
        raise ValueError("dc_ramp years must tile 1..horizon exactly")

    capex = capex_build_up(cfg, multiplier=capex_multiplier)

    rev_rows, opx_rows, energy_rows = [], [], []
    metrics_rows = []
    hourly_last = None
    hourly_year = None

    for yr in range(1, horizon + 1):
        phase = years_by_phase[yr]
        load_mw = load_profile_mw(cfg, phase, scenario)
        gt_on = availability_mask(cfg, yr)
        t = run_hourly(cfg, load_mw, gt_on, mode)

        annual = {
            "mwh": float(np.sum(t["mwh"])),
            "dc_mwh": float(np.sum(np.minimum(t["sched_mw"], t["load_mw"]))),
            "export_mwh": float(np.sum(t["export_mw"])),
            "import_mwh": float(np.sum(t["import_mw"])),
            "fuel_mmbtu": float(np.sum(t["fuel_mmbtu"])),
            "fuel_nm3": float(np.sum(t["fuel_nm3"])),
            "fuel_kg": float(np.sum(t["fuel_kg"])),
            "availability": float(np.mean(gt_on.sum(axis=1) > 0)),
            "phase": phase,
        }

        rev = annual_revenue(cfg, yr, annual, t, annual["availability"])
        opx = annual_opex(cfg, yr, annual["fuel_mmbtu"], annual["mwh"], capex["total_capex_usd"])

        rev_rows.append({"year": yr, **rev})
        opx_rows.append({"year": yr, **opx})
        energy_rows.append({"year": yr, "phase": phase, **annual})
        metrics_rows.append(
            {
                "year": yr,
                "ebitda_usd": rev["total_revenue_usd"] - opx["total_opex_usd"],
                "fuel_share_pct": opx["fuel_cost_usd"] / opx["total_opex_usd"] * 100.0,
            }
        )
        hourly_last, hourly_year = t, yr

    revenue_df = pd.DataFrame(rev_rows).set_index("year")
    opex_df = pd.DataFrame(opx_rows).set_index("year")
    energy_df = pd.DataFrame(energy_rows).set_index("year")
    margin_df = pd.DataFrame(metrics_rows).set_index("year")

    debt = DebtSchedule(cfg, capex["total_capex_usd"])
    discount = cfg["financing"]["discount_rate_pct"] / 100.0
    cf = build_cashflows(cfg, revenue_df, opex_df, capex["total_capex_usd"], debt, horizon)
    # build_cashflows reads total_revenue_usd/total_opex_usd by .loc[year]; indexes are year.
    metrics = summary_metrics(
        cfg, cf, revenue_df, opex_df, capex["total_capex_usd"], discount
    )

    return {
        "metrics": metrics,
        "cashflows": cf,
        "revenue_df": revenue_df,
        "opex_df": opex_df,
        "energy_df": energy_df,
        "margin_df": margin_df,
        "capex": capex,
        "debt": debt,
        "hourly_last": hourly_last,
        "hourly_year": hourly_year,
        "scenario": scenario,
        "dispatch_mode": mode,
        "horizon": horizon,
    }