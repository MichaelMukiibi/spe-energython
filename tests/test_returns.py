"""Closed-form checks for NPV/IRR/payback helpers."""
import numpy as np
import pytest

from models.financial.returns import npv, irr, payback_years, cumulative_cashflow


def test_npv_closed_form():
    # 1000 today, 1100 in one year at 10% -> NPV = 0
    cf = np.array([-1000.0, 1100.0])
    assert npv(cf, 0.10) == pytest.approx(0.0, abs=1e-9)


def test_irr_known_profile():
    cf = np.array([-1000.0, 1100.0])
    assert irr(cf) == pytest.approx(0.10, abs=1e-6)


def test_irr_multiperiod():
    # two equal inflows of 600 at years 1,2 on -1000 -> ~0.13066
    cf = np.array([-1000.0, 600.0, 600.0])
    assert irr(cf) == pytest.approx(0.130663, abs=1e-4)


def test_payback_interpolation():
    cf = cumulative_cashflow(np.array([-100.0, 40.0, 40.0, 40.0]))
    # crosses zero between year 2 and 3
    assert payback_years(cf) == pytest.approx(2.5, abs=1e-9)


def test_payback_none_when_never_recouped():
    cf = cumulative_cashflow(np.array([-100.0, 10.0, 10.0]))
    assert payback_years(cf) is None