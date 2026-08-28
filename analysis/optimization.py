"""Optimization: PPA-tariff vs gas-price break-even frontier and NPV heatmap.

Shows where the project is bankable (project NPV >= 0) and where equity clears the
hurdle (equity IRR >= financing.equity_hurdle_pct) across a gas-price x PPA-price grid.

Usage: python -m analysis.optimization"""

from __future__ import annotations

import copy
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from models.financial.project import run_project
from models.loader import deep_merge, load_baseline

OUT = Path(__file__).resolve().parent.parent / "outputs"

GAS_GRID_USD_PER_MMBTU = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
PPA_GRID_USD_PER_KWH = [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22]


def sweep(cfg, gas_grid=GAS_GRID_USD_PER_MMBTU, ppa_grid=PPA_GRID_USD_PER_KWH):
    """Run the full grid. Returns matrix (project_npv) and records list."""
    base = copy.deepcopy(cfg)
    npv = np.zeros((len(gas_grid), len(ppa_grid)))
    irr_p = np.zeros_like(npv)
    irr_e = np.zeros_like(npv)
    records = []
    for i, g in enumerate(gas_grid):
        for j, p in enumerate(ppa_grid):
            c = deep_merge(
                base,
                {
                    "fuel": {"price_usd_per_mmbtu": g},
                    "ppa": {"energy_price_usd_per_kwh": p},
                },
            )
            r = run_project(c)
            m = r["metrics"]
            npv[i, j] = m["project_npv_usd"]
            irr_p[i, j] = m["project_irr_pct"]
            irr_e[i, j] = m["equity_irr_pct"]
            records.append(
                {
                    "gas_price_usd_mmbtu": g,
                    "ppa_price_usd_kwh": p,
                    "project_npv_usd": m["project_npv_usd"],
                    "project_irr_pct": m["project_irr_pct"],
                    "equity_irr_pct": m["equity_irr_pct"],
                    "min_dscr": m["min_dscr"],
                }
            )
    return {
        "npv": npv,
        "irr_project": irr_p,
        "irr_equity": irr_e,
        "gas_grid": gas_grid,
        "ppa_grid": ppa_grid,
        "records": pd.DataFrame(records),
    }


def break_even(gas_grid, ppa_grid, ipp_grid):
    """Minimum PPA price per gas price where ipp_grid (>=0.0 passes)."""
    out = []
    for i, g in enumerate(gas_grid):
        vals = [ppa_grid[j] for j, p in enumerate(ppa_grid) if ipp_grid[i, j] > 0.0]
        out.append(
            {
                "gas_price_usd_mmbtu": g,
                "breakeven_ppa_usd_kwh": min(vals) if vals else None,
            }
        )
    return pd.DataFrame(out)


def fig_heatmap(res, cfg):
    gas = np.array(res["gas_grid"])
    ppa = np.array(res["ppa_grid"])
    npv = res["npv"] / 1e6
    X, Y = np.meshgrid(gas, ppa, indexing="ij")

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    im = ax.pcolormesh(X, Y, npv, cmap="RdYlGn", shading="auto")
    ax.contour(X, Y, npv, levels=[0.0], colors="k", linewidths=2)

    # bankable frontier (equity IRR >= hurdle)
    hurdle = cfg["financing"]["equity_hurdle_pct"]
    be_npv = break_even(gas, ppa, res["npv"])
    ax.plot(
        be_npv["gas_price_usd_mmbtu"],
        be_npv["breakeven_ppa_usd_kwh"],
        marker="o",
        ls="--",
        color="k",
        lw=1.6,
        label="NPV = 0 frontier",
    )
    ax.scatter(
        [cfg["fuel"]["price_usd_per_mmbtu"]],
        [cfg["ppa"]["energy_price_usd_per_kwh"]],
        marker="*",
        s=280,
        color="blue",
        zorder=5,
        label="Baseline case",
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Project NPV (USD million @10% discount)")
    ax.set_xlabel("Delivered CNG price (USD/MMBtu)")
    ax.set_ylabel("PPA energy price (USD/kWh)")
    ax.set_title(
        f"Bankability map — CCGT + 10\u201320 MW DC (equity IRR \u2265 {hurdle:.0f}%)"
    )
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "ppa_gas_heatmap.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/ppa_gas_heatmap.png")


def fig_breakeven(res, cfg):
    gas = np.array(res["gas_grid"])
    ppa_grid = np.array(res["ppa_grid"])
    be_npv = break_even(gas, ppa_grid, res["npv"])
    hurdle = cfg["financing"]["equity_hurdle_pct"]
    # bankable marker: 1.0 where equity IRR >= hurdle, 0.0 otherwise
    equity_cover = (res["irr_equity"] >= hurdle).astype(float)
    be_equity = break_even(gas, ppa_grid, equity_cover)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(
        be_npv["gas_price_usd_mmbtu"],
        be_npv["breakeven_ppa_usd_kwh"],
        marker="o",
        label="Project NPV = 0 (project IRR = 10%)",
        lw=1.8,
    )
    ax.plot(
        be_equity["gas_price_usd_mmbtu"],
        be_equity["breakeven_ppa_usd_kwh"],
        marker="s",
        label=f"Equity IRR = {hurdle:.0f}% (bankable)",
        lw=1.8,
    )
    ax.axvline(
        cfg["fuel"]["price_usd_per_mmbtu"],
        color="tab:gray",
        ls=":",
        label="Baseline gas",
    )
    ax.set_xlabel("Delivered CNG price (USD/MMBtu)")
    ax.set_ylabel("Minimum PPA energy price (USD/kWh)")
    ax.set_title("Break-even tariffs vs gas price")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "breakeven_tariff.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/breakeven_tariff.png")
    return be_npv, be_equity


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default=None)
    args = ap.parse_args(argv)

    cfg = load_baseline(args.scenario)
    res = sweep(cfg)

    (OUT / "tables").mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    res["records"].to_csv(OUT / "tables" / "ppa_gas_grid.csv", index=False)

    fig_heatmap(res, cfg)
    be_npv, be_equity = fig_breakeven(res, cfg)
    be_npv.to_csv(OUT / "tables" / "breakeven_npv.csv", index=False)
    be_equity.to_csv(OUT / "tables" / "breakeven_equity_irr.csv", index=False)

    base_gas = cfg["fuel"]["price_usd_per_mmbtu"]
    r = be_equity[be_equity["gas_price_usd_mmbtu"] == base_gas]
    print(
        f"At baseline gas ${base_gas}/MMBtu: min PPA for equity-cover = "
        f"${r.iloc[0]['breakeven_ppa_usd_kwh']:.3f}/kWh (baseline {cfg['ppa']['energy_price_usd_per_kwh']})"
    )
    print("  wrote outputs/tables/ppa_gas_grid.csv, breakeven_*.csv")


if __name__ == "__main__":
    main()
