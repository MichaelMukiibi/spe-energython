# HRSG Thermal Modeling — Boundary Conditions & Constraints

> Merged from `Uh so if we are finding out, if we have our condit.._.docx` (the modeling workflow)
> and HRSG sections of the Gemini CCPP reports (01-ccpp-design-report.md).

## Overview

The plant uses a **dual-inlet, single-pressure unfired HRSG**: two gas turbine exhaust streams enter,
one superheated-steam outlet. Modeling combines the exhaust properties **upfront**, then enforces
the system's thermal constraints.

## Step 1 — Combining the Exhaust Streams

- **Combined mass flow:** m_gas,total = m_GT1 + m_GT2 = 97,600 + 97,600 = **195,200 kg/hr** (~54.22 kg/s)
  _(the modeling doc used 195,000 kg/hr / 54.17 kg/s; the datasheet-based figure is 195,200 kg/hr)_
- **Mixed exhaust temperature:** both turbines run at identical load → combined inlet = individual
  outlet = **526°C**. If loads differ, use mass-weighted average:
  T_mix = (m₁·T₁ + m₂·T₂) / (m₁ + m₂)

## Step 2 — The 3 Core Modeling Constraints

| Parameter                          | Recommended Value | Purpose in Model                                                         |
| ---------------------------------- | ----------------- | ------------------------------------------------------------------------ |
| Steam Turbine Inlet Pressure (P_s) | 35–45 bar         | Fixes boiling point (T_sat) in the evaporator drum                       |
| Superheat Temperature (T_s1)       | 380–420°C         | Selected 80–100°C below exhaust gas inlet (526°C)                        |
| Pinch Point Difference (ΔT_pinch)  | 10–15°C           | Prevents temperature crossover in evaporator; controls total steam yield |

Additional constraint: **stack outlet temperature > 140°C** to avoid acid condensation / corrosion
of the carbon-steel stack (sulfur compounds in exhaust).

## Step 3 — Sequential Solution Workflow

1. **Upper zone (superheater + evaporator):** use T_gas,in = 526°C down to the pinch temperature
   (T_g,pinch = T_sat + ΔT_pinch) to solve for maximum allowable steam mass flow (m_steam).
2. **Lower zone (economizer):** use derived m_steam to calculate heat extraction from remaining gas
   flow down to final stack temperature (T_stack).
3. **Validation check:** ensure T_stack > 140°C.

## Design Point Performance

- Steam output: 34,000–40,000 kg/hr (design point ~34.0 t/h) @ **3.8 MPa, 420°C**
- Unfired operation → low CAPEX, simplified emissions compliance, maximum heat extraction down to
  stack pinch ~130–140°C
- HRSG thermal recovery: ~82–85%

## Related Control Loops

- **Three-element drum level control:** balances steam flow out, feedwater flow in, and drum level —
  counters "swell and shrink" during abrupt GT load changes (most transient-sensitive loop).
- **Exhaust bypass dampers:** on steam-turbine trip, route hot exhaust directly to atmospheric
  bypass stack → gas turbines keep running in simple-cycle mode, preserving export stability.

---

_Sources: `Uh so if we are finding out, if we have our condit.._.docx`; HRSG sections of both Gemini exports; 01-ccpp-design-report.md._

