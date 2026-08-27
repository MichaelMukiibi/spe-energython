# Plant Layout & Spatial Blueprint

> Merged from `plant_layout.docx` (2D/3D general arrangement), `New Microsoft Word Document.docx`
> (the design conversation that produced it), and §9 of Gemini export 6_39_44.
> Interactive 3D model: `../assets/plant-layout.html` (drag to rotate, scroll to zoom).

## Design Brief (from the original design conversation)

**Layout brief ("New Microsoft Word Document"):**

- 2x Kawasaki gas engines, each with its own synchronized generator (8 MW rating each, ~15.6 MW
  combined actual)
- Combined exhaust: ~195,000 kg/h @ 526°C from both engines into one HRSG
- HRSG: 2 inlets (one per engine exhaust duct), 1 common steam outlet → 34,000–40,000 kg/h steam
- Shared HRSG drives 1x Siemens SST-200 with its own synchronized generator (~5 MW)
- All three generators synchronize onto a common electrical bus ("bussing")
- 2 on-site natural gas storage vessels piped directly to the engines, refilled via CNG "virtual
  pipeline" trucks; one central filling/offload station feeding both tanks; tanks interconnected so
  they remove gas at a leveled rate to feed both turbines
- Plus: transformers, switchgear, and everything a 20 MW plant is meant to have

**Design decisions locked in that conversation:**

- Grid standard confirmed: 50 Hz
- Grid-tied export confirmed (utility wants 10–20 MW flexible output; excess power goes to grid at time t)
- Country: **Nigeria** (good natural gas + developed systems; AI data center needs a supporting
  economy; Kenya rejected — geothermal, insufficient gas)
- CNG (not LNG) — cheaper, no regas skid; fuel consumption modeled on natural gas, not LNG
- HRSG stack height driven by NESREA emissions/dispersion requirements

## General Arrangement Components

```
+-------------------------------------------------------------------------------------------------+
|                                     [N] NORTH BOUNDARY LINK                                     |
|          +-----+  TCN 33 kV Grid Interconnection  +-----+                                        |
|   T1 (15 MVA 6.6/33 kV)                        T2 (15 MVA 6.6/33 kV)                            |
|          +------------------+------------------+                                                  |
|                             |  6.6 kV Main Switchgear (3 incomers)   |                            |
|    +------------------------+-------------------+                     |                            |
|    | Kawasaki GT-1 Module  |===================|  Kawasaki GT-2 Module|                           |
|    |  8 MVA, 6.6 kV        |                   |  8 MVA, 6.6 kV      |                           |
|    +----+    Hot Exhaust   |                   |   Hot Exhaust   +---+                            |
|         +------------------+-------------------+----------------+                                 |
|                           v                                         v                              |
|           +---------------------------------------------------------------+                        |
|           |      Dual-Inlet Unfired HRSG Module & Stack (90 ft relief)    |                        |
|           +------------------------------------+--------------------------+                        |
|                                     Main Steam | 3.8 MPa Line                                      |
|                                                v                                                   |
|      +-------------------------+    +-----------------------+                                      |
|      |    Siemens SST-200      | →  | Steam Condenser Pkg    |                                      |
|      |    (4.72 MWe, 6.6 kV)   |    +-----------+-----------+                                      |
|      +------------+------------+                |                                                  |
|                   ↓                             ↓                                                  |
|      [Feedwater Pump Skid]            [Condensate Return Tank] → [Feedwater Storage Tank]         |
+-------------------------------------------------------------------------------------------------+
| [SOUTH YARD]                                                                                     |
|   Control Room (DCS/SCADA/ESD)   |   CNG Pressure Reduction Skid                                  |
|       Admin Building             |   CNG Tank 1 <—(level-balanced)→ CNG Tank 2                     |
|                                  |        ↑                                  ↑                    |
|                                  |        +—— Central Truck Offloading Station —+                 |
+-------------------------------------------------------------------------------------------------+
```

## Functional Quadrants

- **Northern — Electrical & grid substation:** TCN 33 kV interconnection node, parallel dual
  15 MVA step-up transformers, main 6.6 kV synchronized switchgear busbar.
- **Central — Power island:** twin side-by-side Kawasaki GT skids (~17.4 m × 3.5 m × 3.4 m per
  package), straight-line exhaust ducting into shared central double-inlet HRSG tower (HRSG stack
  ~90 ft relative volumetric relief to satisfy NESREA dispersion criteria), turbine hall with
  SST-200 skid + surface condenser.
- **Southern — Fuel logistics:** isolated CNG truck offloading bay, level-balanced storage cylinder
  manifolds, automated pressure-reduction skids.
- **Southwest — Administration & control:** DCS terminal screens, SCADA monitors, hard-wired ESD
  console — placed outside thermal and volatile-gas envelopes.

## Closed-Loop Fluid Routing (Rankine)

Feedwater Storage Tank → Feedwater Pump Skid → HRSG → Superheated Steam (3.8 MPa, 420°C) →
Siemens SST-200 → LP Exhaust Steam → Steam Condenser → Condensate Return Tank → back to Feedwater
Storage Tank.

## 3D Model Notes

- NESREA stack ≥32 m physical height (plume dispersion for CO/NOₓ ground-level compliance).
- Layout constructed from a singular coordinate matrix: the 3D volumetric model maps directly from
  the 2D schematic vectors (X/Y → X/Z transform) so footprints, piping, safety setbacks map
  identically in both views.
- Auxiliary power: step-down transformer 6.6 kV → 0.4 kV taps the MV switchgear for internal
  control-room power. DCS + ESD instrumentation lines run to every field sensor, governor,
  balancing valve, and breaker.
- _Disclaimer in the source artifact: conceptual process-flow arrangement, not a stamped P&ID /
  SLD; verify dimensions/setbacks against EPC certified drawings and NESREA/TCN requirements._

---

_Sources: `plant_layout.docx`; `New Microsoft Word Document.docx`; `plant_layout.html` / `plant_layout.html -2 / __1_ (3)` variants (kept best: ../assets/plant-layout.html); Gemini export 6_39_44 §9._

