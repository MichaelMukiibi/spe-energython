# AMTS Energython 2026 — Engineering Checkpoints: RESOLVED

> Research phase is **CLOSED**. This document converts the original open engineering checkpoints
> into the **resolved engineering decisions** that drive the techno-economic model.
> Sources: `research/technical-team-research/` (consolidated design record) + `data/config/parameters.yaml`.

## Locked System Configuration

| Item | Decision | Value |
|---|---|---|
| Prime movers | 2x Kawasaki GPB80D gas turbines (M7A-03D) | 2 x 7.67 MWe = 15.34 MWe |
| Bottoming cycle | 1x Siemens SST-200 condensing steam turbine | 4.72 MWe |
| Heat recovery | Dual-inlet, single-pressure **unfired** HRSG | 34 t/h steam @ 3.8 MPa, 420°C |
| Total gross / net | — | 20.06 MWe gross / ~19.60 MWe net |
| CC efficiency | — | 43.5–45.0% |
| Fuel | CNG trucked "virtual pipeline" (no LNG regas) | ~4,623 Nm³/h (~157 MMBtu/h) |
| Electrical | 6.6 kV → 2x 15 MVA → 33 kV TCN | Grid-tied, 50 Hz |
| Data center demand | CS#1 load profiles (mixed = baseline) | 10–20 MW, PUE 1.25 |

## Original Checkpoints → Resolved Answers

### 1–2. Power, energy, efficiency
- **Engine technology:** gas turbines (not reciprocating engines).
- **Efficiency:** simple-cycle 33.3–33.6% (heat rate 10,820 kJ/kWh) per GT; **combined-cycle
  43.5–45.0%** after steam bottoming. Effective model efficiency for financial fuel mapping:
  **η_cc = 0.44**.
- **Gas spec / calorific value:** design-basis LHV **35.9 MJ/Nm³**.
- **Gas price:** CNG delivered **$/MMBtu** — WORKING assumption seeded in `scenarios/baselines.yaml`
  (research closed; sensitivity-swept).

### 3–5. Waste heat and CHP
- **Heat recovery route:** exhaust → HRSG → steam **drives MORE electricity** (SST-200),
  it is NOT used for absorption chilling. Data-center cooling is handled electrically and captured
  by the facility's **PUE (1.25 tropical)**.
- HRSG thermal recovery ~82–85%, stack floor 140°C (acid dew point), pinch 10–15°C.
- GT exhaust per unit: 27.11 kg/s @ 526°C → combined 54.22 kg/s @ 526°C.

### 6. Natural-gas cost
- Fuel model: `Gas Cost = consumption (Nm³/h) × LHV (MJ/Nm³) × price ($/MMBtu)`.
- Consumption locked at ~4,623 Nm³/h (~157.3 MMBtu/h, ~3,315 kg/h) at design point.
- Price + escalation: WORKING in `scenarios/baselines.yaml` (`fuel.price_usd_per_mmbtu: 8.0`,
  escalation 2%/yr), swept in `sensitivity.yaml`.

### 7–10. Electricity value and operating margin
- Generation voltage 6.6 kV; step-up 6.6/33 kV via 2x 15 MVA; TCN PCC at 33 kV.
- Auxiliary (parasitic) load: **0.46 MW**; net ≈ 19.6 MW.
- Delivery: BTM co-location (data center tapped at MV switchgear) + grid export of surplus.
- UPS/grid backup handled in the operational layer (grid-tied; island fallback).

### 11. Availability
- 8,000 h/yr utilisation standard seeded; **availability 0.95** and **forced-outage 0.05** are
  WORKING placeholders in `baselines.yaml` → refined via the reliability model + sensitivity sweep.

### 12–16. N+1 redundancy and reliability
- Configuration is **2x1 CCGT**: two independent GT trains + shared HRSG/ST.
- Removing one GT leaves ~12–15 MWe usable; the plant maintains 10–20 MW-rated DC supply through
  part-load and GT-outage operation. Grid export/import provides the backstop.

### 17–18. Expected revenue
- `Plant failure ≠ customer outage` holds: grid-tied export/import modelled in the operational layer.
- Revenue = energy payments (DC + export) + capacity payments.

### 19–20. PPA revenue structure
- Structure: energy ($/kWh) + capacity ($/month). WORKING values in `baselines.yaml`
  (`0.15 USD/kWh`, `20,000 USD/month`, 20-yr term, 2% escalation).
- Take-or-pay alignment: fuel contract structure is a financial-layer input (CNG trucking), not an
  engineering constraint on dispatch — flagged for the financial model.

## Model inputs each discipline now OWNS

| Discipline | Delivered input | Where it lives |
|---|---|---|
| CS#1 (this repo) | 8760-hr load profiles (mixed / AI-heavy / cloud-heavy), PUE, DC sizing | `data/load_profiles/`, `data/config/parameters.yaml` |
| Mechanical | GT specs, HRSG, SST-200, Rankine, maintenance | `technical-team-research/` + `scenarios/baselines.yaml` |
| Electrical | 6.6 kV topology, transformers, grid tie, aux load | `technical-team-research/research/06-electrical-topology.md` |
| Petroleum | CNG supply, calorific value, fuel price/escalation | `technical-team-research/research/07-fuel-logistics.md`, `scenarios/baselines.yaml` (financials WORKING) |
| Finance | CAPEX/OPEX/financing/PPA → NPV/IRR | model build (this session onward) |

## What the model must now compute

1. Hourly DC demand → generation dispatch → fuel consumption → net/gross + export.
2. Gross-to-net conversion (0.46 MW parasitic) and grid export/import.
3. Annual operating profile → energy revenue + capacity revenue.
4. CAPEX + OPEX (fuel, O&M, CNG logistics) → project cash flows → NPV/IRR.
5. Sensitivity across gas price, PPA pricing, availability, financing, and load scenario.