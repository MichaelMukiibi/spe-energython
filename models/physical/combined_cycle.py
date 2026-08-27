"""Physical 2x1 CCGT model: hourly generation, fuel consumption, grid balance."""
from __future__ import annotations

import numpy as np

MMBTU_PER_MWH = 3.412
MJ_PER_MMBTU = 1055.06


def part_load_efficiency_factor(sched_mw, rated_net_mw, floor_ratio=0.30, floor_factor=0.80):
    """Linear efficiency ramp from floor -> full between 30% and 70% of net rating."""
    pl = np.asarray(sched_mw, dtype=float) / rated_net_mw
    slope = (1.0 - floor_factor) / (0.70 - floor_ratio)
    factor = np.where(pl >= 0.70, 1.0, floor_factor + np.clip(pl - floor_ratio, 0, None) * slope)
    return np.where(pl <= floor_ratio, floor_factor, factor)


def cc_fuel_mmbtu(mwh, eta_cc, efficiency_factor=1.0):
    """Combined-cycle fuel burn: MWh_e / eta_eff, converted to MMBtu (HHV-free, LHV basis)."""
    return mwh * MMBTU_PER_MWH / (eta_cc * efficiency_factor)


def cc_fuel_nm3(mwh, eta_cc, lhv_mj_per_nm3, efficiency_factor=1.0):
    """Fuel burn in Nm3 of CNG from generated MWh."""
    mmbtu = cc_fuel_mmbtu(mwh, eta_cc, efficiency_factor)
    return mmbtu * MJ_PER_MMBTU / lhv_mj_per_nm3


def run_hourly(cfg, load_mw, gt_on, dispatch_mode="max_export"):
    """Hourly CCGT simulation.

    Args:
        cfg: baseline config dict.
        load_mw: (8760,) facility demand (MW).
        gt_on: (8760, 2) bool array, GT availability per unit.
        dispatch_mode: "max_export" (run at full net, export surplus) or
                       "load_following" (generate just to load, no export).

    Returns:
        dict of per-hour arrays + end-of-array state.
    """
    pl = cfg["plant"]
    fu = cfg["fuel"]
    gt_mw = pl["gas_turbine_capacity_mw"]
    st_mw = pl["steam_turbine_capacity_mw"]
    parasitic = pl["parasitic_load_mw"]
    eta_cc = pl["combined_cycle_efficiency"]
    lhv = fu["lhv_mj_per_nm3"]
    density = fu.get("density_kg_per_nm3", 0.717)
    floor_ratio = pl.get("part_load_floor_ratio", 0.30)
    floor_factor = pl.get("part_load_floor_efficiency_factor", 0.80)

    gt_on = np.asarray(gt_on, dtype=bool)
    n_gt_on = gt_on.sum(axis=1).astype(float)
    any_on = n_gt_on > 0

    # Steam turbine output scales with available exhaust (half with one GT running).
    st_output = np.where(any_on, st_mw * (n_gt_on / 2.0), 0.0)
    gross_mw = n_gt_on * gt_mw + st_output
    net_available_mw = np.where(any_on, gross_mw - parasitic, 0.0)

    if dispatch_mode == "max_export":
        sched_mw = net_available_mw
    elif dispatch_mode == "load_following":
        sched_mw = np.minimum(net_available_mw, np.maximum(load_mw, 0.0))
    else:
        raise ValueError(f"Unknown dispatch_mode: {dispatch_mode}")

    import_mw = np.maximum(load_mw - sched_mw, 0.0)
    if dispatch_mode == "max_export":
        export_mw = np.maximum(sched_mw - load_mw, 0.0)
    else:
        export_mw = np.zeros_like(sched_mw)

    eff_factor = part_load_efficiency_factor(
        sched_mw, pl["net_capacity_mw"], floor_ratio=floor_ratio, floor_factor=floor_factor
    )
    mwh = sched_mw / 1.0  # hourly = MWh
    fuel_mmbtu = cc_fuel_mmbtu(mwh, eta_cc, eff_factor)
    fuel_nm3 = fuel_mmbtu * MJ_PER_MMBTU / lhv
    fuel_kg = fuel_nm3 * density

    return {
        "load_mw": np.asarray(load_mw, dtype=float),
        "n_gt_on": n_gt_on,
        "sched_mw": sched_mw,
        "net_available_mw": net_available_mw,
        "import_mw": import_mw,
        "export_mw": export_mw,
        "mwh": mwh,
        "efficiency_factor": eff_factor,
        "fuel_mmbtu": fuel_mmbtu,
        "fuel_nm3": fuel_nm3,
        "fuel_kg": fuel_kg,
        "operating_hours": float(np.count_nonzero(sched_mw > 0)),
    }