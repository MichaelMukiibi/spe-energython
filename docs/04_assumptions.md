# Assumptions Register

Research phase is **CLOSED**. Engineering assumptions are **locked** (sourced from
`research/technical-team-research/`). Financial values are **WORKING** — they seed the model and are
swept in sensitivity analysis.

Legend: 🔒 = locked (research-backed) · ⚠️ = working assumption (sensitivity-swept)

## Plant — 2x1 CCGT

| Parameter | Value | Unit | Source | Confidence |
|---|---|---|---|---|
| Gas turbine model | Kawasaki GPB80D (M7A-03D) | — | Datasheet `assets/datasheets/01-...datasheet.pdf` | 🔒 High |
| GT unit capacity | 7.67 | MWe | Datasheet (ISO 15°C) | 🔒 High |
| GT count | 2 | — | Design research | 🔒 High |
| Steam turbine model | Siemens SST-200 condensing | — | Selection doc | 🔒 High |
| Steam turbine capacity | 4.72 | MWe | Design research | 🔒 High |
| Gross capacity | 20.06 | MWe | Sum | 🔒 High |
| Parasitic / aux load | 0.46 | MW | Design research | ⚠️ Medium |
| Net capacity | 19.60 | MWe | Gross − parasitic | 🔒 High |
| Combined-cycle efficiency | 0.44 (43.5–45.0%) | — | Thermodynamic analysis | 🔒 High |
| GT simple-cycle efficiency | 0.333 | — | Datasheet | 🔒 High |
| GT heat rate | 10,820 | kJ/kWh | Datasheet | 🔒 High |
| Availability | 0.95 | — | Placeholder → reliability model | ⚠️ Low |
| Forced-outage rate | 0.05 | — | Placeholder → reliability model | ⚠️ Low |

## Heat recovery

| Parameter | Value | Unit | Source | Confidence |
|---|---|---|---|---|
| HRSG type | Dual-inlet, single-pressure, unfired | — | Design research | 🔒 High |
| GT exhaust (per unit) | 27.11 kg/s @ 526°C | — | Datasheet | 🔒 High |
| Combined exhaust | 54.22 | kg/s | Sum | 🔒 High |
| Steam yield | 34.0 (34–40) | t/h | Design research | 🔒 Medium |
| Steam conditions | 3.8 MPa / 420°C | — | Design research | 🔒 High |
| Thermal recovery | ~0.83 (82–85%) | — | Design research | ⚠️ Medium |
| Stack temperature | ≥140 | °C | Acid dew-point floor | 🔒 High |
| Rankine efficiency | 0.28 | — | Design research | ⚠️ Medium |

## Fuel (CNG)

| Parameter | Value | Unit | Source | Confidence |
|---|---|---|---|---|
| Fuel type | CNG trucked virtual pipeline | — | Logistics research (LNG rejected) | 🔒 High |
| LHV | 35.9 | MJ/Nm³ | Kawasaki design basis | 🔒 High |
| Consumption | 4,623 | Nm³/h | Calculation from heat rate | 🔒 High |
| Mass flow | 3,315 | kg/h | Calculation (ρ≈0.717) | 🔒 High |
| Energy basis | 157.3 | MMBtu/h | Calculation | 🔒 High |
| Delivered price | **8.0** | USD/MMBtu | Working — Nigerian CNG range | ⚠️ Low |
| Price escalation | **2.0** | %/yr | Working | ⚠️ Low |

## Data center (CS#1)

| Parameter | Value | Unit | Source | Confidence |
|---|---|---|---|---|
| Baseline load scenario | mixed | — | CS#1 (default set in this repo) | 🔒 High |
| Alternate scenarios | ai_heavy, cloud_heavy | — | `data/load_profiles/` | 🔒 High |
| IT capacity | 12.0 | MW | 12 MW net IT within 15 MW facility | 🔒 High |
| Facility capacity | 15.0 | MW | CS#1 sizing spec | 🔒 High |
| Target PUE | 1.25 | — | Tropical, hybrid liquid cooling | 🔒 High |
| Deployment phases | 10 / 15 / 20 | MW | `data/config/parameters.yaml` | 🔒 High |

## PPA & financing

| Parameter | Value | Unit | Source | Confidence |
|---|---|---|---|---|
| Energy price | **0.15** | USD/kWh | Working | ⚠️ Low |
| Capacity payment | **20,000** | USD/month | Working | ⚠️ Low |
| PPA escalation | **2.0** | %/yr | Working | ⚠️ Low |
| Contract tenor | 20 | yr | Typical IPP | ⚠️ Medium |
| Debt share | **0.70** | — | Working | ⚠️ Low |
| Debt interest | **8.0** | %/yr | Working | ⚠️ Low |
| Debt tenor | **15** | yr | Working | ⚠️ Low |
| Equity hurdle | **12.0** | %/yr | Working | ⚠️ Low |
| Inflation | **3.0** | %/yr | Working | ⚠️ Low |
| Discount rate | **10.0** | %/yr | Working — project WACC | ⚠️ Low |

> CAPEX ($/kW for turbines, HRSG, CNG station, BOP) is the **next build step**; it is intentionally
> deferred to the CAPEX module rather than hard-coded here.

## Retired placeholder (DO NOT reuse)

| Old | New |
|---|---|
| 5 x 3 MW reciprocating engines | 2x1 CCGT (2x GPB80D GT + SST-200 ST) |
| 40% engine efficiency | 44% combined-cycle efficiency |
| Absorption-chiller cooling CHP | Steam bottoming → more electricity; cooling via PUE 1.25 |
| 15 MW net | ~19.6 MWe net |