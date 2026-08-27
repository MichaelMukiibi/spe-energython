# Validation

## 1. Input Validation

- **Load profiles:** 8,760 hourly rows per scenario (mixed / AI-heavy / cloud-heavy), generated and
  validated by CS#1 (`data/load_profiles/*.csv`; column schema:
  `hour, hour_of_day, day_of_year, it_load_kw, facility_load_kw, utilization, scenario`).
- **Engineering parameters:** locked against manufacturer datasheets (Kawasaki GPB80D, Siemens
  SST-200) and the consolidated research in `research/technical-team-research/`.

## 2. Cross-Checks (first principles)

| Check | Expected | Derivation |
|---|---|---|
| CC efficiency | 0.435–0.45 | `20.06 MW × 3.412 / 0.44 ≈ 155.6 MMBtu/h` ≈ research 157.3 |
| Fuel volume | ~4,623 Nm³/h | `(gas_MMBtu/h) → MJ → / LHV 35.9 MJ/Nm³` |
| Fuel mass | ~3,315 kg/h | volume × ρ 0.717 |
| Net vs gross | 19.60 ≈ 20.06 − 0.46 | gross − parasitic |
| Steam→ST power | 4.72 MWe | 34 t/h at ~7.2 t/h per MW |
| DC PUE | 1.25 | facility = IT × PUE (CS#1) |

## 3. Unit Testing

- `/tests/` will contain per-module tests as the model is built:
  - physical: fuel, generation, export math
  - operational: dispatch, availability, one-GT-out
  - financial: CAPEX build-up, revenue, debt service, NPV/IRR closed-form check
- Run: `pytest` (or `python -m unittest`, whichever is adopted).

## 4. Simulation Validation

- **Baseline health:** NPV/IRR sign and magnitude sanity vs comparable Nigerian 20 MW IPP
  benchmarks (to be documented in outputs after build).
- **Scenario monotonicity:** higher gas price ⇒ lower NPV; higher PPA price ⇒ higher NPV.
- **Edge cases:** full load, part load, GT outage, HRSG/ST trip, gas interruption, grid export/import
  spikes.

## 5. Presentation Readiness

- Tornado sensitivity charts, NPV/IRR summary tables, and scenario comparison figures exported to
  `outputs/` for the shark-pitch deck.