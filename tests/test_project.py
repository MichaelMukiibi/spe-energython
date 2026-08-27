"""Material-balance and scenario-invariance checks on the end-to-end run."""
import numpy as np
import pytest

from models.loader import load_baseline
from models.operational.dispatch import availability_mask
from models.physical.combined_cycle import run_hourly
from models.financial.project import run_project
from models.financial.capex import capex_build_up


def test_energy_balance_max_export():
    cfg = load_baseline()
    gt_on = availability_mask(cfg, year=1)
    load = np.full(8760, 10.0)
    t = run_hourly(cfg, load, gt_on, "max_export")

    dc = np.minimum(t["sched_mw"], t["load_mw"])
    assert np.isclose(np.sum(t["mwh"]), np.sum(dc) + np.sum(t["export_mw"]))
    assert np.isclose(np.sum(t["load_mw"]), np.sum(dc) + np.sum(t["import_mw"]))
    # no export during full outage; import only when generation short
    assert np.all(t["import_mw"] <= t["load_mw"] + 1e-9)


def test_energy_balance_load_following():
    cfg = load_baseline()
    gt_on = availability_mask(cfg, year=3)
    load = np.full(8760, 10.0)
    t = run_hourly(cfg, load, gt_on, "load_following")
    assert np.isclose(np.sum(t["export_mw"]), 0.0)
    dc = np.minimum(t["sched_mw"], t["load_mw"])
    assert np.isclose(np.sum(t["load_mw"]), np.sum(dc) + np.sum(t["import_mw"]))


def test_dc_ramp_phases_tile_horizon():
    cfg = load_baseline()
    r = run_project(cfg, load_scenario="mixed")
    phases = r["energy_df"]["phase"]
    assert set(r["energy_df"].index) == set(range(1, 21))
    assert set(phases.loc[[1, 2]]) == {"phase_1"}
    assert set(phases.loc[[3, 6]]) == {"phase_2"}
    assert set(phases.loc[[7, 20]]) == {"phase_3"}


def test_capex_register_consistency():
    cfg = load_baseline()
    cap = capex_build_up(cfg)
    expected = sum(v["cost_usd"] for v in cfg["capex"]["items"].values())
    assert cap["total_capex_usd"] == pytest.approx(expected)
    assert 1000 < cap["specific_capex_usd_per_kw_gross"] < 3000


def test_baseline_viability_smoke():
    r = run_project(load_baseline())
    m = r["metrics"]
    assert m["project_npv_usd"] > 0
    assert m["equity_npv_usd"] > 0
    assert 5 < m["project_irr_pct"] < 40
    assert 10 < m["equity_irr_pct"] < 80
    assert m["min_dscr"] is not None and m["min_dscr"] > 1.0


def test_negative_case_gas_above_headline():
    """High gas should degrade NPV but the sign should still be sane."""
    from models.loader import deep_merge
    import copy
    cfg = deep_merge(copy.deepcopy(load_baseline()), {"fuel": {"price_usd_per_mmbtu": 10.5}})
    low = run_project(cfg)["metrics"]["project_npv_usd"]
    base_npv = run_project(load_baseline())["metrics"]["project_npv_usd"]
    assert low < base_npv