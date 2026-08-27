"""Fuel-conversion identity tests and design-point cross-checks."""
import pytest

from models.physical.combined_cycle import (
    MMBTU_PER_MWH,
    MJ_PER_MMBTU,
    part_load_efficiency_factor,
    cc_fuel_mmbtu,
    cc_fuel_nm3,
)
from models.loader import load_baseline


def test_full_load_fuel_matches_research_design():
    """At full net load the model must reproduce the locked design fuel figures
    (~157.3 MMBtu/h gross basis, ~4,623 Nm3/h, ~3,315 kg/h)."""
    cfg = load_baseline()
    fu = cfg["fuel"]
    mwh_h = cfg["plant"]["gross_capacity_mw"]  # per hour at gross
    mwh_h_net = cfg["plant"]["net_capacity_mw"]
    eta = cfg["plant"]["combined_cycle_efficiency"]

    mmbtu_gross = cc_fuel_mmbtu(mwh_h, eta)
    assert mmbtu_gross == pytest.approx(157.3, rel=0.02)

    nm3 = cc_fuel_nm3(mwh_h_net, eta, fu["lhv_mj_per_nm3"])
    # net basis (19.6 MW) at 44% -> ~152 MMBtu/h -> ~4,470 Nm3/h
    assert nm3 == pytest.approx(fu["flow_nm3_per_h"], rel=0.05)

    kg = nm3 * fu["density_kg_per_nm3"]
    assert kg == pytest.approx(fu["flow_kg_per_h"], rel=0.05)


def test_unit_identity():
    mmbtu = cc_fuel_mmbtu(1.0, 0.44)
    assert mmbtu == pytest.approx(MMBTU_PER_MWH / 0.44)
    nm3 = cc_fuel_nm3(1.0, 0.44, 35.9)
    assert nm3 == pytest.approx(mmbtu * MJ_PER_MMBTU / 35.9)


def test_part_load_factor_ramp():
    assert part_load_efficiency_factor(19.6, 19.6) == pytest.approx(1.0)
    assert part_load_efficiency_factor(14.0, 19.6) == pytest.approx(1.0)  # >=70%
    assert part_load_efficiency_factor(5.5, 19.6) == pytest.approx(0.80)  # ~28% -> floor
    lo, hi = part_load_efficiency_factor(8.0, 19.6), part_load_efficiency_factor(11.0, 19.6)
    assert lo < hi  # monotonic up
    assert 0.8 <= lo <= 1.0