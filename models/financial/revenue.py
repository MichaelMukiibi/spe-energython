"""Revenue model: data-center energy, exports, imports, capacity payments."""

from __future__ import annotations

import numpy as np


def annual_revenue(cfg, year, annual_energy, t_models, availability):
    """Compute a single operating year's revenue streams.

    Args:
        cfg: baseline config.
        year: 1-indexed operating year (drives escalation).
        annual_energy: dict with mwh (generated), served (to DC), export, import.
        t_models: dict of physical model arrays (for served/export/import MWh).
        availability: plant availability fraction for capacity performance.

    Returns dict of revenue lines (USD millions would be scaled by caller).
    """
    p = cfg["ppa"]
    esc = (1.0 + p["escalation_pct_per_yr"] / 100.0) ** (year - 1)

    dc_mwh = float(np.sum(np.minimum(t_models["sched_mw"], t_models["load_mw"])))
    export_mwh = float(np.sum(t_models["export_mw"]))
    import_mwh = float(np.sum(t_models["import_mw"]))

    energy_revenue = dc_mwh * p["energy_price_usd_per_kwh"] * 1000 * esc
    export_revenue = export_mwh * p["export_price_usd_per_kwh"] * 1000 * esc
    import_cost = import_mwh * p["import_price_usd_per_kwh"] * 1000 * esc
    capacity_revenue = p["capacity_payment_usd_per_month"] * 12.0 * availability * esc

    return {
        "year": year,
        "dc_mwh": dc_mwh,
        "export_mwh": export_mwh,
        "import_mwh": import_mwh,
        "energy_revenue_usd": energy_revenue,
        "export_revenue_usd": export_revenue,
        "import_cost_usd": import_cost,
        "capacity_revenue_usd": capacity_revenue,
        "total_revenue_usd": energy_revenue
        + export_revenue
        + capacity_revenue
        - import_cost,
    }


def revenue_series(cfg, annual_list, year_results):
    """Convenience: build a DataFrame of revenue lines over the horizon."""
    import pandas as pd

    rows = []
    for y in annual_list:
        rows.append(
            {
                "year": y,
                **year_results[y]["revenue"],
            }
        )
    return pd.DataFrame(rows)
