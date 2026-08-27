# CCPP Design Report — 20 MW Combined Cycle Power Plant

> Merged from the two Gemini comprehensive-report exports (`6_32_12` technical report and
> `6_39_44` revenue & engineering report). The 6_39_44 export is the base; unique
> technical detail from 6_32_12 is folded in where marked *(6_32_12)*.

## Executive Brief

**Project Location:** Nigeria, Africa Region
**Design Capacity:** ~20.06 MWe Gross / ~19.60–20.00 MWe Net Combined Cycle Power Plant (CCPP)
**Configuration:** 2x1 CCGT Layout
**Target Load:** 10–20 MW Flexible Data Center Demand Profile
**Interconnection:** TCN 33 kV Utility Grid / Behind-the-Meter (BTM) Data Center Co-location Option
**Grid Standard:** 50 Hz (Nigeria / TCN)

### 1.1 Core Strategic Decision Points

- **Prime movers:** 2x Kawasaki Heavy Industries GPB80D (M7A-03D) gas turbine packages — 15.34 MWe gross.
- **Bottoming Rankine cycle:** 1x Siemens Energy SST-200 condensing steam turbine — 4.72 MWe gross.
- **Total gross capacity:** 20.06 MWe; net ~19.60–20.00 MWe after 0.46 MW plant parasitic load.
- **Thermal efficiency:** 43.5%–45.0% combined cycle (vs ~33.3% simple-cycle baseline).
- **Fuel:** CNG "virtual pipeline" truck-delivery framework, two pressure-equalized on-site storage vessels.
  **LNG-to-gas regasification was explicitly rejected** (lower levelized cost of fuel — LCOF for piped/trucked
  CNG; avoids cryogenic vaporizers, boil-off compressors, insulation envelopes).

```
    +------------------------------+
    |  2x Kawasaki GPB80D (GTGs)   |  15.34 MWe
    +--------------+---------------+
                   |
      Exhaust Gas | 195,200 kg/hr @ 526°C
                   v
    +------------------------------+
    |   Dual-Inlet Unfired HRSG    |  ~34.0 tons/hr Steam
    +--------------+---------------+
                   |
     Superheated  | 3.8 MPa, 420°C
     Steam        v
    +------------------------------+
    |     Siemens SST-200 (STG)    |  4.72 MWe
    +--------------+---------------+
                   |
                   v
     TOTAL GROSS: 20.06 MWe ELECTRICAL
```

### 1.2 Region & Site Rationale

- Nigeria chosen for dense domestic natural gas infrastructure and co-location viability for
  high-availability IT loads (AI data centers).
- Kenya was evaluated but rejected (geothermal system already developed, insufficient natural gas).
- CNG virtual pipeline circumvents physical pipeline right-of-way development delays and capex.

## Performance Summary

| Plant Component / Metric | Technical Specification |
|---|---|
| Gas Turbines (2x Kawasaki GPB80D) | 15.34 MWe Gross |
| Steam Turbine (1x Siemens SST-200) | 4.72 MWe Gross |
| Total Gross Electrical Output | 20.06 MWe |
| Parasitic / Station Auxiliary Load | -0.46 MW |
| Net Power Output Envelope | ~19.60–20.00 MWe |
| CCPP Overall Electrical Efficiency | ~43.5%–45.0% |
| Plant Operational Footprint | Inline Parallel Dual-Train Architecture |

## Prime Mover Selection & Thermal Balance

### Gas Turbine Candidates (evaluated & rejected)

| Model | Output (simple cycle) | CCPP fit |
|---|---|---|
| Siemens SGT-750 | 41.0 MWe (40.5% eff, HR 8,884 kJ/kWh) | 2x1 = 108.4 MW — **severely oversized** |
| Siemens SGT-A35 (SCC-600) | ~34–36.5 MWe (37–40% eff) | 2x1 = ~74.2 MW — **oversized** |
| Kawasaki GPB180D (L20A) | 17.97 MWe (33.7% eff, HR 10,690 kJ/kWh), exhaust 213×10³ kg/hr @ 545°C | 2 units = 35.94 MW — **exceeds target before bottoming** |
| **Kawasaki GPB80D (M7A-03D)** | **7.67–7.81 MWe (33.3–33.6% eff, HR 10,820 kJ/kWh)** | **Selected — leaves margin for ~4.7 MW bottoming cycle** |

### Selected Prime Movers

Each Kawasaki GPB80D unit:
- Gross output: 7.67 MWe at 15°C ISO (2 × 7.67 = 15.34 MWe combined)
- Exhaust: 97,600 kg/hr (27.11 kg/s) @ 526°C (978.8°F) per unit → 195,200 kg/hr (54.22 kg/s) combined
- DLE combustor: NOₓ < 15 ppm
- Turbine rotor speed: 13,790 rpm (reduction gearbox → 1,500 rpm generator)

### Bottoming Cycle

- **HRSG:** Dual-inlet, single-pressure unfired HRSG (economizer + drum + superheater).
  34,000–40,000 kg/hr steam, design point ~34.0 t/h @ 3.8 MPa, 420°C.
- **Steam turbine:** Siemens SST-200 condensing. Thermo-flexible single-casing design for
  rapid thermal cycling / fast load-following (data center transients).
- Conversion: ~4.72 MWe from ~34 t/h (industrial Rankine ~7.2 t/h per MW).

## Generator Architecture

- **Gas turbines:** each drives a **BRUSH Power Generation 4-Pole DG Series** air-cooled,
  salient-pole synchronous turbogenerator, 1,500 rpm, 6.6 kV terminal voltage, brushless
  excitation, Class F insulation. *(6_32_12)*
- **Steam turbine:** **Marelli Motori MJH 710 Series** H/MV synchronous generator, natively wound
  for 6.6 kV, 4- or 6-pole via reduction gearbox, D-Vo digital AVR. *(6_32_12 — replaces the
  mistakenly evaluated marine SGM series, which is not fit for stationary grid duty.)*

## Electrical Balance of Plant

- All three generators feed a **6.6 kV Main Switchgear (3-incomer synchronized busbar)**:
  GT-1, GT-2, SST-200 generator incomers.
- **Main step-up transformers T1 & T2:** dual 15 MVA, 6.6 kV → 33 kV, parallel/redundant.
- **Auxiliary step-down transformer:** 6.6 kV → 0.4 kV for house loads
  (pumps, control room, gas compressor skids). *(6_32_12)*
- **PCC:** Transmission Company of Nigeria (TCN) 33 kV grid; grid-tied export of excess power
  whenever data center load < generation.

## Process Control, Automation & Dynamics

**(6_32_12)**
- Central DCS + SCADA; local PLCs over isolated Ethernet/Modbus plant network.
- Control loops: GT load/droop control; HRSG three-element feedwater (level/swell-shrink);
  exhaust-gas bypass dampers (simple-cycle mode on ST trip); auto-sync check + anti-islanding relays.
- ESD: fully independent hard-wired system; fixed gas detection around CNG offloading;
  automatic fuel isolation + breaker de-energization.

## Site Layout (Functional Quadrants)

- **Northern — Grid substation:** TCN 33 kV node, dual 15 MVA transformers, 6.6 kV switchgear.
- **Central — Power island:** twin side-by-side Kawasaki GT skids (~17.4 m × 3.5 m × 3.4 m per
  package *(6_32_12)*), straight-line exhaust ducting into shared central double-inlet HRSG tower,
  HRSG stack ~90 ft vertical relief to satisfy NESREA dispersion criteria *(6_32_12)*, SST-200
  + condenser in adjacent turbine hall.
- **Southern — Fuel logistics:** CNG truck offloading bay, level-balanced storage manifolds,
  pressure-reduction skids.
- **Southwest — Administration & control:** DCS/SCADA/ESD control room outside thermal/gas envelopes.

## Next Engineering Milestones (per 6_32_12 report)

> "Would you like me to compile a comprehensive economic model analysis focusing on the gas
> consumption tariffs and levelized cost of electricity (LCOE) for this Nigerian plant layout?"

*(6_39_44 adds, beyond 6_32_12: fuel logistics calculations §5, detailed electrical topology §6,
grid synchronization loops §6.2, regulatory compliance §8, and 3D layout registry §9 —
captured in the dedicated topic docs 05, 06, 07 and 08.)*

---

*Sources: `Gemini Export August 26, 2026 at 6_32_12 PM GMT+3.docx`; `Gemini Export August 26, 2026 at 6_39_44 PM GMT+3.docx`; `what is critical here.docx`; `Act as a Senior Power Plant Systems Engineer and....docx`.*