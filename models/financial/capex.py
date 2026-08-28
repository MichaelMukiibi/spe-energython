"""CAPEX build-up from the engineering register in scenarios/baselines.yaml."""

from __future__ import annotations

import pandas as pd


def capex_build_up(cfg, multiplier=1.0):
    """Itemized CAPEX register -> totals + DataFrame.

    Totals are always computed from items (never read back from YAML) so the
    register stays the single source of truth.
    """
    items = cfg["capex"]["items"]
    total = sum(v["cost_usd"] for v in items.values()) * multiplier

    df = pd.DataFrame(
        {
            "item": list(items.keys()),
            "description": [v["description"] for v in items.values()],
            "basis": [v["basis"] for v in items.values()],
            "cost_usd": [v["cost_usd"] * multiplier for v in items.values()],
        }
    )
    df["share_pct"] = df["cost_usd"] / total * 100.0

    gross_mw = cfg["plant"]["gross_capacity_mw"]
    net_mw = cfg["plant"]["net_capacity_mw"]
    return {
        "total_capex_usd": total,
        "specific_capex_usd_per_kw_gross": total / (gross_mw * 1e3),
        "specific_capex_usd_per_kw_net": total / (net_mw * 1e3),
        "gross_mw": gross_mw,
        "net_mw": net_mw,
        "register_df": df,
    }
