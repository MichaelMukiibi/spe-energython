# AMTS Energython Africa 2026

> **Techno-economic modeling of a natural-gas-powered data center energy system**

## Overview

This repository contains our technical and techno-economic analysis for the **AMTS Energython Africa 2026** challenge.

The project approaches the challenge as an integrated **physical system + operational + financial model**, rather than treating the power plant as a simple financial asset.

Our modeling pipeline is:

```text
Natural Gas (CNG virtual pipeline)
     │
     ▼
2x Gas Turbines (Kawasaki GPB80D)
     │
     ├──────────────────────► Electricity (15.34 MWe)
     │                              │
     │                              ▼
     │                       Data Center (facility load)
     ▼
   Exhaust (526°C)
     │
     ▼
    HRSG (steam 34 t/h @ 3.8 MPa)
     │
     ▼
   Steam Turbine (Siemens SST-200)
     │
     ├──────────────────────► Electricity (4.72 MWe)
     │                              │
     │                              ▼
     │                    Data Center / Grid export
     ▼
   Surplus to TCN 33 kV Grid (grid-tied export)
          ↓
   Operational Model (dispatch / availability)
          ↓
     PPA Revenue
          ↓
   CAPEX + OPEX
          ↓
   Project Cash Flows
          ↓
       NPV / IRR
```

The objective is to determine whether a natural-gas-based **combined-cycle** generation system can
provide **reliable, economically competitive and technically viable power** for a large data-center
load. Waste heat is converted into **additional electricity** via a steam bottoming cycle (CCGT) —
not into cooling. Data-center cooling electricity is represented directly through the facility's
PUE (1.25 tropical target).

---

## Core Questions

The model is designed to answer:

* What generation configuration is technically appropriate for a 10–20 MW data center?
* How much natural gas is required (CNG truck-delivered)?
* How does combined-cycle efficiency change with load?
* How much electricity does the steam bottoming cycle add from turbine exhaust?
* What N+1 reliability does the 2x1 GT+ST configuration provide?
* How do planned and forced outages affect delivered energy?
* What are the CAPEX and OPEX requirements?
* How should the PPA structure electricity and capacity revenue?
* How does grid-tied export of surplus generation contribute to revenue?
* What are the project's NPV and IRR?
* Which assumptions have the greatest effect on project viability?
* What operating and system configuration maximizes project value?

---

# Modeling Architecture

The project is divided into several interconnected layers.

### 1. Physical Model

Models the CCGT generation system.

Key variables include:

* Gas turbine capacity and simple-cycle efficiency (heat rate)
* Combined-cycle configuration (2x GT + 1x ST via HRSG)
* Fuel consumption (CNG, Nm³/h and kg/h)
* Tesla exhaust temperature and mass flow
* HRSG steam yield and steam-turbine output
* Load
* Grid export

### 2. Operational Model

Determines how the plant operates under changing conditions.

This includes:

* GT/ST dispatch
* Part-load operation
* Engine availability
* Planned maintenance
* Forced outages
* N+1 redundancy (2x GT + 1x ST)
* Grid backup
* Reserve capacity
* CNG fuel-supply reliability

### 3. Revenue Model

Translates physical output into project revenue.

Revenue streams:

* Energy payments (data center + grid export)
* Capacity payments
* Grid export of surplus power

### 4. Financial Model

Models:

* CAPEX
* Fuel costs
* Maintenance
* Other OPEX
* Financing
* Debt service
* Taxes
* Project cash flow
* Equity cash flow
* NPV
* IRR

### 5. Sensitivity & Optimization

Tests how project viability changes under different assumptions.

Examples:

* Natural-gas price (CNG delivered $/MMBtu)
* Electricity/PPA price
* Combined-cycle efficiency
* Engine configuration
* CAPEX
* Availability
* Financing conditions
* Load profile scenario (mixed / AI-heavy / cloud-heavy)

---

# Repository Structure

```text
spe-energython/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
│
├── research/
│   ├── engineering_checkpoints.md        # resolved engineering decisions (CLOSED)
│   ├── literature_review.md
│   ├── sources.md
│   └── technical-team-research/          # consolidated design research (CS#1)
│       ├── research/                     # merged markdown docs 00–08
│       ├── assets/                       # datasheets, images, plant layout
│       └── archive/
│
├── docs/
│   ├── 01_challenge.md
│   ├── 02_system_architecture.md
│   ├── 03_modeling_methodology.md
│   ├── 04_assumptions.md
│   ├── 05_validation.md
│   └── cs1_data_center/                  # CS#1 specs: sizing, PUE, load profiling
│
├── data/
│   ├── load_profiles/                    # 8760-hr CSVs (3 scenarios x 3 phases)
│   ├── config/parameters.yaml            # CS#1 data center config
│   └── README.md
│
├── models/
│   ├── physical/
│   │   ├── engine.py
│   │   ├── fuel.py
│   │   ├── heat_recovery.py
│   │   ├── combined_cycle.py
│   │   └── plant.py
│   │
│   ├── operational/
│   │   ├── dispatch.py
│   │   ├── reliability.py
│   │   ├── availability.py
│   │   └── maintenance.py
│   │
│   └── financial/
│       ├── revenue.py
│       ├── opex.py
│       ├── capex.py
│       ├── financing.py
│       ├── cashflow.py
│       └── returns.py
│
├── scenarios/
│   ├── baselines.yaml                    # CANONICAL — locked engineering + working financials
│   ├── high_gas_price.yaml
│   ├── low_gas_price.yaml
│   └── sensitivity.yaml
│
├── analysis/
│   ├── sensitivity.py
│   ├── optimization.py
│   └── results.py
│
├── notebooks/
│   ├── 01_physical_model.ipynb
│   ├── 02_dispatch_model.ipynb
│   ├── 03_financial_model.ipynb
│   └── 04_sensitivity_analysis.ipynb
│
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── reports/
│
└── tests/
```

---

# Research Status

🚧 **Research phase CLOSED — moving to model build.**

The engineering configuration is **locked**:

* 2x1 CCGT: 2x Kawasaki GPB80D gas turbines (15.34 MWe) + 1x Siemens SST-200 condensing steam
  turbine (4.72 MWe) = 20.06 MWe gross / ~19.60 MWe net
* Combined-cycle efficiency: 43.5–45.0%
* Fuel: CNG truck-delivered "virtual pipeline", ~4,623 Nm³/h (~157 MMBtu/h)
* Electrical: 6.6 kV generation → 2x 15 MVA transformers → TCN 33 kV, grid-tied
* Data center: 10–20 MW (CS#1 8760-hr load profiles), PUE 1.25 tropical

See `research/technical-team-research/research/` for the full consolidated design record, and
`scenarios/baselines.yaml` for the canonical model parameter file.

---

# Assumptions

Assumptions are **not hard-coded** into model logic — they are stored in `scenarios/*.yaml`.

The canonical baseline is `scenarios/baselines.yaml`. Key values:

```yaml
plant:
  gas_turbine_count: 2
  gas_turbine_capacity_mw: 7.67
  steam_turbine_capacity_mw: 4.72
  net_capacity_mw: 19.60
  combined_cycle_efficiency: 0.44

engine:
  availability: 0.95

fuel:
  price_usd_per_mmbtu: 8.0        # WORKING — delivered CNG

data_center:
  baseline_load_profile: "mixed"
  target_pue: 1.25

ppa:
  energy_price_usd_per_kwh: 0.15  # WORKING
  capacity_payment_usd_per_month: 20000  # WORKING
```

**Engineering values are locked from research. Financial values ($/MMBtu gas, PPA pricing,
financing terms) are marked `WORKING` — they seed the build and are sensitivity-swept, since the
research phase has closed.**

---

# Key Engineering Relationships

### Electrical generation (CCGT)

[
E_{electric}=P_{electric}\times t
]

### Fuel requirement

[
E_{fuel}=\frac{E_{electric}}{\eta_{cc}}
]

where combined-cycle efficiency
[
\eta_{cc}\approx 0.435\text{--}0.45
]

### Gas turbine exhaust → HRSG steam

[
\dot m_{steam}=f(\dot m_{exhaust},T_{exhaust})
]

### Steam turbine output (bottoming cycle)

[
P_{ST}=\dot m_{steam}\times \Delta h \times \eta_{Rankine}
]

### Grid export

[
E_{export}=E_{generated}-E_{data\ center\ load}
]

### Gas cost

[
Gas\ Cost=Gas\ Consumption\times Gas\ Price
]

### Energy revenue

[
Energy\ Revenue=E_{delivered}\times P_{energy}
]

### Present value

[
PV_t=\frac{CF_t}{(1+r)^t}
]

### Project NPV

[
NPV=-CAPEX+\sum_{t=1}^{T}\frac{CF_t}{(1+r)^t}
]

---

# Model Development Principles

### 1. Physics before finance

Financial outputs are downstream of the physical system:

> What does the plant physically do? → How does it operate? → What does that operation cost and
> produce? → Is the resulting project financially viable?

### 2. Separate assumptions from model logic

Technical assumptions are configurable via `scenarios/*.yaml`, not embedded in Python.

### 3. Make assumptions traceable

Every major parameter should have: value, unit, source, rationale, confidence level.
(Engineering values are locked and sourced; financial values are `WORKING`.)

### 4. Validate before optimizing

Ensure physical and financial models behave correctly before attempting optimization.

### 5. Test edge cases

Examples: full load, part load, GT outage, HRSG/ST trip, maintenance periods, gas-supply
interruption, grid export/import, high/low gas prices, high/low electricity prices.

---

# Reproducibility

```bash
git clone <repository-url>
cd spe-energython

pip install -r requirements.txt

python -m models.physical.plant --scenario baselines
python -m analysis.results --scenario baselines
```

Exact commands will be updated as the implementation stabilizes.

---

# Disclaimer

This repository is an analytical and modeling project developed for the **AMTS Energython Africa 2026** challenge. Financial parameters are working assumptions for a competition submission and should not be interpreted as engineering, financial, or investment advice.