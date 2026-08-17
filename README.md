# AMTS Energython Africa 2026

> **Techno-economic modeling of a natural-gas-powered data center energy system**

## Overview

This repository contains our technical and techno-economic analysis for the **AMTS Energython Africa 2026** challenge.

The project approaches the challenge as an integrated **physical system + operational + financial model**, rather than treating the power plant as a simple financial asset.

Our modeling pipeline is:

```text
Natural Gas
     │
     ▼
Gas Engines
     │
     ├──────────────► Electricity ──────────► Data Center
     │
     ▼
 Waste Heat
     │
     ▼
Heat Recovery
     │
     ▼
Absorption Chilling
     │
     ▼
 Data Center Cooling

          ↓
   Operational Model
          ↓
 Reliability / Dispatch
          ↓
     PPA Revenue
          ↓
   CAPEX + OPEX
          ↓
  Project Cash Flows
          ↓
      NPV / IRR
```

The objective is to determine whether a natural-gas-based generation system can provide **reliable, economically competitive and technically viable power** for a large data-center load while exploiting opportunities for combined heat and power (CHP).

---

## Core Questions

The model is designed to answer:

* What generation configuration is technically appropriate for a 10–20 MW data center?
* How much natural gas is required?
* How does engine efficiency change with load?
* How much waste heat is available?
* How much of that heat can be recovered?
* Can recovered heat meaningfully reduce cooling electricity demand?
* What N+1 configuration provides adequate reliability?
* How do planned and forced outages affect delivered energy?
* What are the CAPEX and OPEX requirements?
* How should the PPA structure electricity and capacity revenue?
* What are the project's NPV and IRR?
* Which assumptions have the greatest effect on project viability?
* What operating and system configuration maximizes project value?

---

# Modeling Architecture

The project is divided into several interconnected layers.

### 1. Physical Model

Models the behavior of the generation and cooling systems.

Key variables include:

* Engine capacity
* Electrical efficiency
* Fuel consumption
* Load
* Waste heat
* Heat recovery
* Chiller COP
* Cooling demand

### 2. Operational Model

Determines how the plant operates under changing conditions.

This includes:

* Engine dispatch
* Part-load operation
* Engine availability
* Planned maintenance
* Forced outages
* N+1 redundancy
* Grid backup
* Reserve capacity

### 3. Revenue Model

Translates physical output into project revenue.

Potential revenue streams include:

* Energy payments
* Capacity payments
* Other contractual services

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

* Natural-gas price
* Electricity/PPA price
* Engine efficiency
* Engine configuration
* CAPEX
* Availability
* Cooling assumptions
* Financing conditions

---

# Repository Structure

```text
amts-energython-africa-2026/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
│
├── research/
│   ├── engineering_checkpoints.md
│   ├── literature_review.md
│   └── sources.md
│
├── docs/
│   ├── challenge.md
│   ├── system_architecture.md
│   ├── modeling_methodology.md
│   ├── assumptions.md
│   └── validation.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── models/
│   ├── physical/
│   │   ├── engine.py
│   │   ├── fuel.py
│   │   ├── heat_recovery.py
│   │   ├── cooling.py
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
│   ├── baseline.yaml
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

# Research Workflow

Engineering assumptions are developed through a structured research process.

```text
Research Question
       ↓
Engineering Discussion
       ↓
Literature / Industry Data
       ↓
Technical Assumption
       ↓
Model Parameter
       ↓
Simulation
       ↓
Validation
       ↓
Financial Impact
```

The `research/engineering_checkpoints.md` document records the technical questions that need to be resolved with input from the:

* Petroleum Engineering team
* Mechanical Engineering team
* Electrical Engineering team

Each major assumption should eventually have a traceable source and justification.

---

# Assumptions

We aim to avoid hard-coding arbitrary assumptions directly into model logic.

Scenario assumptions will be stored separately, for example:

```yaml
plant:
  engine_count: 5
  engine_capacity_mw: 3
  target_load_mw: 10

engine:
  electrical_efficiency: 0.40
  availability: 0.95

gas:
  price_usd_mmbtu: 8.0

cooling:
  heat_recovery_efficiency: 0.60
  absorption_chiller_cop: 0.70

ppa:
  energy_price_usd_kwh: 0.15
  capacity_payment_usd_month: 20000
```

**Values shown above are illustrative model-development assumptions and should not be treated as final project assumptions.**

Final assumptions will be supported by engineering research, manufacturer data, market data, or clearly documented modeling assumptions.

---

# Key Engineering Relationships

### Electrical generation

[
E_{electric}=P_{electric}\times t
]

### Fuel requirement

[
E_{fuel}=\frac{E_{electric}}{\eta_e}
]

### Waste heat

A simplified representation:

[
Q_{waste}=E_{fuel}-E_{electric}
]

### Recoverable heat

[
Q_{recovered}=Q_{waste}\times\eta_{recovery}
]

### Cooling from absorption chiller

[
Q_{cooling}=Q_{recovered}\times COP
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

These relationships will become progressively more detailed as the physical and financial models are developed.

---

# Model Development Principles

### 1. Physics before finance

Financial outputs should be downstream of the physical system.

We should first establish:

> What does the plant physically do?

Then:

> How does it operate?

Then:

> What does that operation cost and produce?

Finally:

> Is the resulting project financially viable?

### 2. Separate assumptions from model logic

Technical assumptions should be configurable rather than embedded directly in Python code.

### 3. Make assumptions traceable

Every major parameter should have:

* Value
* Unit
* Source
* Rationale
* Confidence level

### 4. Validate before optimizing

We should first ensure that the physical and financial models behave correctly before attempting optimization.

### 5. Test edge cases

Examples include:

* Full load
* Part load
* Engine outage
* Multiple engine outages
* Maintenance periods
* Gas supply interruption
* Grid backup
* High gas prices
* Low electricity prices

---

# Current Status

🚧 **Early-stage modeling**

Current work is focused on:

* Understanding the challenge requirements
* Developing the physical system model
* Identifying engineering assumptions
* Establishing the reliability model
* Defining the PPA/revenue structure
* Designing the project-finance model
* Building the computational architecture

The baseline scenario and final technical assumptions are still under development.

---

# Team Contributions

The project brings together complementary engineering and computational perspectives.

| Area                    | Primary Focus                                               |
| ----------------------- | ----------------------------------------------------------- |
| Petroleum Engineering   | Natural gas supply, gas quality, fuel economics             |
| Mechanical Engineering  | Engines, thermodynamics, heat recovery, cooling             |
| Electrical Engineering  | Generation, dispatch, grid integration, reliability         |
| Computational / Finance | Simulation, optimization, techno-economics, project finance |

The final model should integrate these domains rather than treating them as independent analyses.

---

# Reproducibility

The goal is for the final results to be reproducible from the documented assumptions and source data.

Once the model is implemented, the expected workflow will be:

```bash
git clone <repository-url>
cd amts-energython-africa-2026

pip install -r requirements.txt

python -m models.physical.plant
python -m analysis.results
```

Exact commands will be updated as the implementation stabilizes.

---

# Disclaimer

This repository is an analytical and modeling project developed for the **AMTS Energython Africa 2026** challenge.

Early-stage assumptions are illustrative and should not be interpreted as engineering, financial, or investment advice. Final technical and financial conclusions will depend on validated engineering data, site-specific conditions, contractual terms, and market information.
