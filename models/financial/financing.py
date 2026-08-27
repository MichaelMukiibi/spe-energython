"""Debt financing: amortizing construction loan drawdown."""
from __future__ import annotations

import numpy as np


class DebtSchedule:
    """Senior debt: share of CAPEX funded at year 0, amortized over tenor.

    Annuity repayment with a simple cash-flow waterfall; interest on outstanding
    balance, principal strips constant per annum (straight-line amortization).
    """

    def __init__(self, cfg, total_capex_usd):
        self.share = cfg["financing"]["debt_share"]
        self.principal = total_capex_usd * self.share
        self.interest = cfg["financing"]["debt_interest_pct"] / 100.0
        self.tenor = cfg["financing"]["debt_tenor_years"]

    def annual_principal(self):
        return self.principal / self.tenor

    def schedule(self, n_years):
        principal_pay = np.zeros(n_years + 1)
        interest_pay = np.zeros(n_years + 1)
        outstanding = np.zeros(n_years + 1)
        outstanding[0] = self.principal  # drawn at year 0 construction
        annual_principal = self.annual_principal()
        for yr in range(1, n_years + 1):
            interest_pay[yr] = outstanding[yr - 1] * self.interest
            principal_pay[yr] = min(annual_principal, outstanding[yr - 1])
            outstanding[yr] = outstanding[yr - 1] - principal_pay[yr]
        return {
            "principal_payment_usd": principal_pay,
            "interest_payment_usd": interest_pay,
            "outstanding_usd": outstanding,
            "total_debt_service_usd": principal_pay + interest_pay,
        }