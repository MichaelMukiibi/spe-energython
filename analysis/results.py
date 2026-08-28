"""Baseline run: produce summary tables, cash-flow figures and a narrative report
for the slide deck / video. Usage: python -m analysis.results [--scenario X]"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from models.financial.project import run_project
from models.loader import deep_merge, load_baseline

OUT = Path(__file__).resolve().parent.parent / "outputs"


def fmt_m(v):
    return f"${v / 1e6:,.1f}M"


def save_fig(fig, name):
    fig.savefig(OUT / "figures" / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote outputs/figures/{name}")


def cashflow_table(result):
    cf = result["cashflows"]
    rows = []
    for yr in range(0, result["horizon"] + 1):
        rows.append(
            {
                "year": yr,
                "revenue_usd": cf["revenue_usd"][yr],
                "opex_usd": cf["opex_usd"][yr],
                "ebitda_usd": cf["ebitda_usd"][yr],
                "tax_usd": cf["tax_usd"][yr],
                "project_cashflow_usd": cf["project_cashflow_usd"][yr],
                "equity_cashflow_usd": cf["equity_cashflow_usd"][yr],
                "debt_service_usd": cf["debt_service_usd"][yr],
                "cumulative_project_usd": np.cumsum(cf["project_cashflow_usd"])[yr],
                "cumulative_equity_usd": np.cumsum(cf["equity_cashflow_usd"])[yr],
            }
        )
    return pd.DataFrame(rows)


def fig_capex_pie(result):
    df = result["capex"]["register_df"]
    fixed = {
        "GT packages": df.loc[df.item == "gt_packages", "cost_usd"].sum(),
        "HRSG": df.loc[df.item == "hrsg", "cost_usd"].sum(),
        "Steam turbine system": df.loc[
            df.item == "steam_turbine_system", "cost_usd"
        ].sum(),
        "CNG station": df.loc[df.item == "cng_station", "cost_usd"].sum(),
        "Electrical": df.loc[df.item == "electrical", "cost_usd"].sum(),
        "Civil & BOP": df.loc[df.item == "civil_bop", "cost_usd"].sum(),
        "EPC & owners": df.loc[df.item == "epc_owners", "cost_usd"].sum(),
        "Contingency": df.loc[df.item == "contingency", "cost_usd"].sum(),
    }
    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, _, autotexts = ax.pie(
        list(fixed.values()),
        labels=list(fixed.keys()),
        autopct=lambda p: f"{p:.0f}%",
        startangle=90,
        counterclock=False,
    )
    for at in autotexts:
        at.set_fontsize(8)
    ax.set_title(
        f"CAPEX build-up — ${result['capex']['total_capex_usd'] / 1e6:,.1f}M total"
    )
    fig.savefig(OUT / "figures" / "capex_breakdown.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/capex_breakdown.png")


def fig_cashflows(result):
    cf = result["cashflows"]
    years = np.arange(0, result["horizon"] + 1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    ax.bar(years, cf["revenue_usd"] / 1e6, label="Revenue", color="#4C72B0")
    ax.bar(years, -cf["opex_usd"] / 1e6, label="OPEX", color="#DD8452")
    ax.bar(
        years,
        -(cf["opex_usd"] + cf["tax_usd"]) / 1e6,
        color="#C44E52",
        alpha=0.55,
        label="Tax",
    )
    ax.bar(0, -result["capex"]["total_capex_usd"] / 1e6, color="#55A868", label="CAPEX")
    ax.set_xlabel("Operating year")
    ax.set_ylabel("USD million")
    ax.set_title("Annual revenue / costs (project view)")
    ax.legend(fontsize=7, loc="lower right")

    ax = axes[1]
    cum_p = np.cumsum(cf["project_cashflow_usd"]) / 1e6
    cum_e = np.cumsum(cf["equity_cashflow_usd"]) / 1e6
    ax.plot(years, cum_p, marker="o", ms=3, label="Project cumulative")
    ax.plot(years, cum_e, marker="s", ms=3, label="Equity cumulative")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("Operating year")
    ax.set_ylabel("USD million")
    ax.set_title("Cumulative NPV trackers")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "annual_cashflows.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/annual_cashflows.png")


def fig_dispatch_profile(result):
    t = result["hourly_last"]
    if t is None:
        return
    # one representative summer week (e.g. hours 4000-4168)
    sl = slice(4000, 4168)
    h = np.arange(4000, 4168)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(h, t["load_mw"][sl], label="Facility demand (P3)", lw=1.2)
    ax.plot(h, t["sched_mw"][sl], label="CCGT net generation", lw=1.2, color="#55A868")
    ax.fill_between(
        h, t["export_mw"][sl], color="#DD8452", alpha=0.35, label="Export to grid"
    )
    ax.set_xlabel("Hour of year (year %d)" % result["hourly_year"])
    ax.set_ylabel("MW")
    ax.set_title("Dispatch sample — max-export operation")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "dispatch_sample.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  wrote outputs/figures/dispatch_sample.png")


def write_report(result):
    m = result["metrics"]
    e = result["energy_df"]
    rev = result["revenue_df"]
    opx = result["opex_df"]
    lines = []
    ap = lines.append
    ap("# Financial Model — Baseline Summary")
    ap("")
    ap(
        f"*Scenario: `{result['scenario']}` · dispatch: `{result['dispatch_mode']}` · horizon {result['horizon']} yrs*"
    )
    ap("")
    ap("## Headline returns (nominal USD)")
    ap("")
    ap("| Metric | Value |")
    ap("|---|---|")
    ap(
        f"| CAPEX | {fmt_m(m['capex_usd'])} ({m['capex_usd'] / result['capex']['net_mw'] / 1e3:,.0f} USD/kW net) |"
    )
    ap(f"| Equity invested | {fmt_m(m['equity_invested_usd'])} |")
    ap(f"| **Project NPV @10%** | **{fmt_m(m['project_npv_usd'])}** |")
    ap(f"| **Project IRR** | **{m['project_irr_pct']:.1f}%** |")
    ap(f"| **Equity IRR** | **{m['equity_irr_pct']:.1f}%** |")
    ap(f"| Project payback | {m['project_payback_years']:.1f} yr |")
    ap(f"| Equity payback | {m['equity_payback_years']:.1f} yr |")
    ap(f"| Min DSCR | {m['min_dscr']:.2f} |")
    ap(f"| LCOE | ${m['lcoe_usd_per_mwh']:,.2f}/MWh |")
    ap("")
    ap("## Annual operating picture")
    ap("")
    ap("| Metric | Year 1 (P1) | Year 6 (P2) | Year 15 (P3) |")
    ap("|---|---|---|---|")
    ap(
        f"| Facility load (avg, MW) | {e.loc[1, 'load_avg_mw']:.1f} | {e.loc[6, 'load_avg_mw']:.1f} | {e.loc[15, 'load_avg_mw']:.1f} |"
    )
    ap(
        f"| Generated MWh | {e.loc[1, 'mwh']:,.0f} | {e.loc[6, 'mwh']:,.0f} | {e.loc[15, 'mwh']:,.0f} |"
    )
    ap(
        f"| DC-served MWh | {e.loc[1, 'dc_mwh']:,.0f} | {e.loc[6, 'dc_mwh']:,.0f} | {e.loc[15, 'dc_mwh']:,.0f} |"
    )
    ap(
        f"| Exported MWh | {e.loc[1, 'export_mwh']:,.0f} | {e.loc[6, 'export_mwh']:,.0f} | {e.loc[15, 'export_mwh']:,.0f} |"
    )
    ap(
        f"| Imported MWh | {e.loc[1, 'import_mwh']:,.0f} | {e.loc[6, 'import_mwh']:,.0f} | {e.loc[15, 'import_mwh']:,.0f} |"
    )
    ap(
        f"| Fuel burn (MMBtu) | {e.loc[1, 'fuel_mmbtu']:,.0f} | {e.loc[6, 'fuel_mmbtu']:,.0f} | {e.loc[15, 'fuel_mmbtu']:,.0f} |"
    )
    ap(
        f"| EBITDA (USD) | {fmt_m(rev.loc[1, 'total_revenue_usd'] - opx.loc[1, 'total_opex_usd'])} | {fmt_m(rev.loc[6, 'total_revenue_usd'] - opx.loc[6, 'total_opex_usd'])} | {fmt_m(rev.loc[15, 'total_revenue_usd'] - opx.loc[15, 'total_opex_usd'])} |"
    )
    ap(
        f"| Plant availability | {e.loc[1, 'availability']:.3f} | {e.loc[6, 'availability']:.3f} | {e.loc[15, 'availability']:.3f} |"
    )
    ap("")
    ap("## Narrative")
    ap("")
    ap(
        "- Gross 20.06 MWe / net 19.6 MWe CCGT; fuel at delivered CNG; max-export dispatch."
    )
    ap(
        "- Early years (P1, 10 MW DC) operate at ~78% capacity factor and export ~80 GWh/yr to the TCN grid; revenue from exports is a core early stream."
    )
    ap(
        "- At P3 (20 MW DC, PUE 1.20) peak demand 21 MW exceeds net 19.6 MW capacity; outages and the tail of the load curve cause modest grid purchases (2-4% of demand)."
    )
    ap(
        "- 2x1 reliability: plant availability ≈ 97.8% (single-GT and full-plant outage windows covered by grid import, not customer outage)."
    )
    ap(
        "- Financial assumptions flagged WORKING (gas price, PPA/export tariffs, CAPEX, financing) — see sensitivity analysis for swings."
    )
    ap("")
    ap(
        "*Generated by `analysis/results.py`. All figures: `outputs/figures/`. All tables: `outputs/tables/`.*"
    )
    (OUT / "reports" / "financial_model_summary.md").write_text("\n".join(lines))
    print("  wrote outputs/reports/financial_model_summary.md")


def parse_overrides(items):
    """Turn ['fuel.price_usd_per_mmbtu=8.5','ppa.energy_price_usd_per_kwh=0.18']
    into a nested dict for deep_merge. Numeric values are auto-coerced."""
    import ast

    out = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--override expects key.path=value, got {item!r}")
        path, raw = item.split("=", 1)
        try:
            val = ast.literal_eval(raw)  # numbers, lists, True/False, strings
        except (ValueError, SyntaxError):
            val = raw
        node = out
        keys = path.split(".")
        for k in keys[:-1]:
            node = node.setdefault(k, {})
        node[keys[-1]] = val
    return out


def main(argv=None):
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--scenario", default=None)
    ap_.add_argument("--dispatch", default=None)
    ap_.add_argument("--capex-x", type=float, default=1.0, help="CAPEX multiplier")
    ap_.add_argument(
        "-o",
        "--override",
        action="append",
        default=[],
        help="Override a config value by dotted path, e.g. -o fuel.price_usd_per_mmbtu=8.5",
    )
    args = ap_.parse_args(argv)

    cfg = load_baseline(args.scenario)
    if args.override:
        cfg = deep_merge(cfg, parse_overrides(args.override))
    result = run_project(
        cfg, dispatch_mode=args.dispatch, capex_multiplier=args.capex_x
    )

    (OUT / "tables").mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    (OUT / "reports").mkdir(parents=True, exist_ok=True)

    cf = cashflow_table(result)
    cf.to_csv(OUT / "tables" / "cashflows.csv", index=False)
    result["energy_df"].reset_index().to_csv(
        OUT / "tables" / "annual_energy.csv", index=False
    )
    result["revenue_df"].reset_index().to_csv(
        OUT / "tables" / "annual_revenue.csv", index=False
    )
    result["opex_df"].reset_index().to_csv(
        OUT / "tables" / "annual_opex.csv", index=False
    )
    result["capex"]["register_df"].to_csv(
        OUT / "tables" / "capex_register.csv", index=False
    )
    pd.DataFrame([result["metrics"]]).to_csv(
        OUT / "tables" / "financial_summary.csv", index=False
    )
    print("  wrote outputs/tables/*.csv")

    fig_capex_pie(result)
    fig_cashflows(result)
    fig_dispatch_profile(result)
    write_report(result)

    m = result["metrics"]
    print(
        "Baseline OK: project NPV=%s IRR=%.1f%% equity IRR=%.1f%% LCOE=$%.2f/MWh"
        % (
            fmt_m(m["project_npv_usd"]),
            m["project_irr_pct"],
            m["equity_irr_pct"],
            m["lcoe_usd_per_mwh"],
        )
    )


if __name__ == "__main__":
    main()
