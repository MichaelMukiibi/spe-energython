"""Sensitivity analysis: NPV tornado + scenario comparison.
Usage: python -m analysis.sensitivity"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from models.loader import load_baseline, deep_merge
from models.financial.project import run_project

OUT = Path(__file__).resolve().parent.parent / "outputs"

# Each leg: label, dotted path into cfg (or "capex"), low/high override values.
TORNADO_LEGS = [
    {"label": "Gas price ($/MMBtu)", "path": ["fuel", "price_usd_per_mmbtu"], "low": 6.0, "high": 10.5},
    {"label": "PPA energy price ($/kWh)", "path": ["ppa", "energy_price_usd_per_kwh"], "low": 0.12, "high": 0.18},
    {"label": "Export price ($/kWh)", "path": ["ppa", "export_price_usd_per_kwh"], "low": 0.05, "high": 0.09},
    {"label": "Capacity payment ($/mo)", "path": ["ppa", "capacity_payment_usd_per_month"], "low": 15000, "high": 25000},
    {"label": "CAPEX", "path": ["capex"], "low": 0.80, "high": 1.20},
    {"label": "Forced-outage rate/GT", "path": ["engine", "forced_outage_rate"], "low": 0.03, "high": 0.08},
    {"label": "Planned outage (h/yr)", "path": ["engine", "planned_outage_hours"], "low": 334, "high": 84},
    {"label": "Discount rate (%)", "path": ["financing", "discount_rate_pct"], "low": 8.0, "high": 12.0},
    {"label": "Debt interest (%)", "path": ["financing", "debt_interest_pct"], "low": 7.0, "high": 9.0},
    {"label": "Corporate tax (%)", "path": ["tax", "corporate_rate"], "low": 0.25, "high": 0.35},
]


def override_path(cfg, path, value):
    cfg = copy.deepcopy(cfg)
    node = cfg
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    return cfg


def run_npv(cfg, leg):
    """Run project NPV for low/high values of a leg. CAPEX uses the run multiplier."""
    if leg["path"] == ["capex"]:
        r_low = run_project(copy.deepcopy(cfg), capex_multiplier=leg["low"])
        r_high = run_project(copy.deepcopy(cfg), capex_multiplier=leg["high"])
        return r_low, r_high
    r_low = run_project(override_path(cfg, leg["path"], leg["low"]))
    r_high = run_project(override_path(cfg, leg["path"], leg["high"]))
    return r_low, r_high


def tornado(cfg):
    base_npv = run_project(copy.deepcopy(cfg))["metrics"]["project_npv_usd"]
    rows = []
    for leg in TORNADO_LEGS:
        r_low, r_high = run_npv(cfg, leg)
        rows.append(
            {
                "parameter": leg["label"],
                "low": leg["low"],
                "high": leg["high"],
                "npv_low_usd": r_low["metrics"]["project_npv_usd"],
                "npv_high_usd": r_high["metrics"]["project_npv_usd"],
                "low_irr_pct": r_low["metrics"]["project_irr_pct"],
                "high_irr_pct": r_high["metrics"]["project_irr_pct"],
            }
        )
    df = pd.DataFrame(rows)
    df["spread"] = (df["npv_high_usd"] - df["npv_low_usd"]).abs()
    df = df.sort_values("spread", ascending=True)
    return base_npv, df


def fig_tornado(base_npv, df):
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    y = np.arange(len(df))
    low = (df["npv_low_usd"] - base_npv) / 1e6
    high = (df["npv_high_usd"] - base_npv) / 1e6
    ax.barh(y, high, color="#55A868", label="High value")
    ax.barh(y, low, color="#C44E52", label="Low value")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(df["parameter"])
    ax.set_xlabel("Project NPV swing vs baseline (USD million)")
    ax.set_title(f"Tornado — sensitivity of project NPV (baseline ${base_npv/1e6:,.1f}M @10%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "sensitivity_tornado.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/sensitivity_tornado.png")


def scenario_comparison(cfg):
    cases = [
        {"name": "Baseline (mixed)", "cfg": copy.deepcopy(cfg)},
        {"name": "Gas $6.0 (low)", "cfg": deep_merge(copy.deepcopy(cfg), {"fuel": {"price_usd_per_mmbtu": 6.0}})},
        {"name": "Gas $10.5 (high)", "cfg": deep_merge(copy.deepcopy(cfg), {"fuel": {"price_usd_per_mmbtu": 10.5}})},
        {"name": "AI-heavy load", "cfg": deep_merge(copy.deepcopy(cfg), {"data_center": {"baseline_load_scenario": "ai_heavy"}})},
        {"name": "Cloud-heavy load", "cfg": deep_merge(copy.deepcopy(cfg), {"data_center": {"baseline_load_scenario": "cloud_heavy"}})},
        {"name": "Load-following", "cfg": deep_merge(copy.deepcopy(cfg), {"ppa": {"dispatch_mode": "load_following"}})},
    ]
    rows = []
    for case in cases:
        r = run_project(case["cfg"])
        m = r["metrics"]
        rows.append(
            {
                "scenario": case["name"],
                "project_npv_usd": m["project_npv_usd"],
                "project_irr_pct": m["project_irr_pct"],
                "equity_irr_pct": m["equity_irr_pct"],
                "min_dscr": m["min_dscr"],
                "lcoe_usd_per_mwh": m["lcoe_usd_per_mwh"],
                "equity_invested_usd": m["equity_invested_usd"],
            }
        )
    return pd.DataFrame(rows)


def fig_scenarios(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(df["scenario"], df["project_npv_usd"] / 1e6, color="#4C72B0")
    axes[0].set_ylabel("Project NPV (USD million)")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].set_title("NPV by scenario")
    axes[1].bar(df["scenario"], df["project_irr_pct"], color="#55A868")
    axes[1].set_ylabel("Project IRR (%)")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].set_title("IRR by scenario")
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "scenario_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/scenario_comparison.png")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=None)
    ap.add_argument("--quiet", action="store_true", help="print one-line summary only")
    args = ap.parse_args(argv)

    cfg = load_baseline(args.scenario)
    (OUT / "tables").mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(parents=True, exist_ok=True)

    base_npv, tor = tornado(cfg)
    tor.to_csv(OUT / "tables" / "sensitivity_tornado.csv", index=False)
    comp = scenario_comparison(cfg)
    comp.to_csv(OUT / "tables" / "sensitivity_scenarios.csv", index=False)

    if not args.quiet:
        fig_tornado(base_npv, tor)
        fig_scenarios(comp)
    rows = list(tor.itertuples())[-4:]
    print("Tornado NPV spread: " + ", ".join(
        f"{r.parameter} ${(r.npv_high_usd - r.npv_low_usd)/1e6:+.1f}M" for r in rows))
    print("Scenario NPV: " + "; ".join(
        f"{row.scenario}={row.project_npv_usd/1e6:.1f}M" for row in comp.itertuples()))
    print("  wrote outputs/tables/sensitivity_tornado.csv, sensitivity_scenarios.csv")


if __name__ == "__main__":
    main()