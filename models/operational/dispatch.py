"""Operational dispatch and availability simulation."""

from __future__ import annotations

import numpy as np


def availability_mask(cfg, year, hours=8760):
    """Deterministic per-GT availability mask for a given operating year.

    Each GT has an independent Bernoulli(1 - forced_outage_rate) availability
    (seeded RNG, reproducible, varies across years). A contiguous planned-
    maintenance window shuts the whole plant down for the configured number of
    hours (default one week / 168 h) at a year-varying offset in the year.
    """
    e = cfg["engine"]
    n_gts = cfg["plant"]["gas_turbine_count"]
    fo = e["forced_outage_rate"]
    seed = e.get("outage_seed", 2026) + 1000 * year
    rng = np.random.default_rng(seed)
    up = rng.uniform(size=(n_gts, hours))
    gt_on = (up >= fo).T  # (hours, n_gts) bool

    planned = int(e.get("planned_outage_hours", 168))
    if planned > 0:
        offset = (seed * 7) % (hours - planned)
        gt_on[offset : offset + planned, :] = False
    return gt_on


def plant_metrics(cfg, gt_on):
    """Availability/perf indicators from a GT mask."""
    any_on = gt_on.sum(axis=1) > 0
    return {
        "plant_availability": float(any_on.mean()),
        "gt_average_availability": float(gt_on.mean()),
        "operating_hours": int(np.count_nonzero(any_on)),
        "outage_hours": int(np.count_nonzero(~any_on)),
    }
