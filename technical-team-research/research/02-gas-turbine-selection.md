# Gas Turbine Selection — Evaluation & Decision Log

> Merged from `Act as a Senior Power Plant Systems Engineer and....docx` (full evaluation)
> and `what is critical here.docx` (decision summary). These are the AI research-session
> outputs used to lock the turbine choice.

## Task: Gas Turbine & Generator Evaluation (Siemens vs. Kawasaki)

### 1. Analysis of Specifications

#### Siemens SGT-750

- Gross Power Output: 41.0 MWe (simple cycle)
- Simple-cycle efficiency: 40.5% (Heat rate: 8,884 kJ/kWh)
- CCPP fit: 2x1 config = 108.4 MW total (29.3 MW from steam turbine) — **far exceeds ~20 MW target**
- CAPEX/OPEX: very high; scaled for large utility/industrial installations

#### Siemens SGT-A35 (SCC-600)

- Gross Power Output: ~34–36.5 MWe per unit
- Simple-cycle efficiency: ~37–40%
- CCPP fit: 2x1 config = ~74.2 MW — **far exceeds ~20 MW target**
- CAPEX/OPEX: high CAPEX; aeroderivative maintenance profile

#### Kawasaki GPB180D (L20A)

- Gross Power Output: 17.97 MWe (17,970 kW at ISO)
- Simple-cycle efficiency: 33.7% (Heat rate: 10,690 kJ/kWh)
- Exhaust mass flow: 213×10³ kg/hr (~59.17 kg/s)
- Exhaust temperature: 545°C
- CCPP fit: 2 units alone = ~35.9 MW — **exceeds target before adding steam capacity**

#### Kawasaki GPB80D (M7A-03D) — SELECTED

- Gross Power Output: 7.67–7.81 MWe (7,670 kW at 15°C ISO)
- Simple-cycle efficiency: 33.3–33.6% (Heat rate: 10,820 kJ/kWh)
- Exhaust mass flow: 97.6×10³ kg/hr (~27.11 kg/s) per unit
- Exhaust temperature: 526°C (978.8°F)
- CAPEX/OPEX: low-to-moderate capex; highly scalable modular skid

### 2. Selected Optimal Pair — 2x Kawasaki GPB80D (M7A-03D)

- Combined simple-cycle output: 2 × 7.67 MW = **15.34 MWe**
- Combined exhaust thermal potential: 2 × 27.11 kg/s = **54.22 kg/s @ 526°C**
- Thermal alignment: a ~4.7–5.0 MW steam turbine driven by the shared HRSG brings net output
  to ~20.0–20.3 MW, matching the project constraint

### 3. Comparative Justification

1. **Capacity matching:** Siemens units are too large (single SGT-750 > 40 MW; GPB180D dual = 35.9 MW
   baseline). The 2x GPB80D goes to ~15.3 MW baseline, leaving room for the ~4.7 MW bottoming cycle.
2. **High exhaust quality:** 526°C TEGT maximizes superheated steam in the HRSG without heavy
   supplemental firing.
3. **Low CAPEX / lifecycle cost:** industrial single-shaft architecture with DLE (<15 ppm NOₓ),
   long maintenance intervals (MTBF), simple BOP integration vs aeroderivative alternatives.

## Combined-Cycle Performance Summary

| Plant Parameter                        | Design Value    |
| -------------------------------------- | --------------- |
| Gas Turbine 1 Output (Kawasaki GPB80D) | 7.67 MW         |
| Gas Turbine 2 Output (Kawasaki GPB80D) | 7.67 MW         |
| Combined GT Output (2x GPB80D)         | 15.34 MW        |
| Steam Turbine Output (1x SST-200 / ST) | 4.72 MW         |
| Total Gross Electrical Output          | 20.06 MW        |
| Parasitic Load / Station Auxiliary     | -0.46 MW        |
| Net Power Output                       | ~19.60–20.00 MW |
| Combined Cycle Electrical Efficiency   | ~43.5%–45.0%    |

## Decision Matrix

| Component          | Manufacturer & Model                 | Output                       | Efficiency               | Key Advantages                                          | Cost                        | Justification                                                            |
| ------------------ | ------------------------------------ | ---------------------------- | ------------------------ | ------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------ |
| Gas Turbines (2x)  | Kawasaki GPB80D (M7A-03D)            | 7.67 MWe ea (15.34 total)    | 33.3% simple cycle       | Robust single-shaft; DLE <15 ppm; ideal 526°C exhaust   | Moderate CAPEX / low OPEX   | Perfect sizing step for 20 MW CCPP; larger Siemens units exceed capacity |
| HRSG (1x)          | Custom Dual-Inlet Unfired HRSG       | ~34 t/h steam                | ~82–85% thermal recovery | Low maintenance; simple single-pressure; bypass dampers | Low CAPEX / very low OPEX   | Matches 195.2 t/h exhaust without supplemental firing                    |
| Steam Turbine (1x) | Siemens SST-200 / Triveni condensing | 4.72 MWe                     | ~28% (Rankine)           | Compact; flexible grid response                         | Moderate CAPEX / low OPEX   | Converts 34 t/h waste-heat steam into remaining ~4.7 MW                  |
| Plant Total        | 2x GT + 1x HRSG + 1x ST              | ~20.06 MWe gross / ~19.6 net | ~44% CCPP                | Good turndown (1x GT running during maintenance)        | Optimal ROI for 20 MW class | Meets target, optimizes fuel, within capacity limits                     |

## Equipment Sizing (Task 2)

- **HRSG:** Dual-inlet, single-pressure unfired with superheater (dual-pressure optional for max
  efficiency). Steam ~3.8–4.0 MPa(a), 400–450°C; unfired keeps CAPEX low, simplifies emissions,
  extracts heat down to stack pinch ~130°C.
- **Steam turbine:** Siemens SST-110 / SST-200 or Triveni / MAN condensing (~4.7–5.0 MW),
  vacuum condenser (air- or water-cooled), 34 t/h @ 3.8 MPa / 420°C → ~4.72 MWe at ~7.2 t/h per MW.

## Layout Recommendation (Task 3)

The **Inline Parallel Dual-Train Layout** (per the CCGT Siemens reference + 90 MW sample layout):

- GTs side-by-side on concrete pads; straight-line exhaust ducting into central twin-inlet HRSG
  (or two identical side-by-side HRSG modules feeding a common steam header)
- Overhead crane access for rotor pulls, filter replacement, turbine swaps
- Dedicated pipe rack for HP steam lines; transformers separated from fuel-gas valve units (GVU)

---

_Sources: `Act as a Senior Power Plant Systems Engineer and....docx`; `what is critical here.docx` (×2 copies, content identical); datasheets in assets/datasheets/ (Kawasaki GPB80D/GPB180D, Siemens GT portfolio)._

