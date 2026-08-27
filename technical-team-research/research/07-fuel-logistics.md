# Fuel Logistics — CNG Virtual Pipeline

> Extracted from Gemini export 6_39_44 §5 (already clean) + fuel verification thread from
> `New Microsoft Word Document.docx`. Target cross-check for the financial model's fuel OPEX line.

## Strategy

Natural gas in its ambient sweetened state provides a major OPEX advantage over LNG:
no liquefaction, no cryogenic transport, no site regasification skids. The fuel architecture is a
**CNG Virtual Pipeline** of heavy truck trailers delivering compressed gas on a rotating matrix
schedule — circumventing physical pipeline right-of-way development delays and capital costs.

> **Decision:** Standalone LNG-to-gas regasification was explicitly rejected (lower LCOF for piped/
> trucked CNG within the Nigerian regime; avoids cryogenic vaporizers, boil-off gas compressors,
> and thermal insulation envelopes).

## Fuel Consumption Calculations

Design basis: natural gas LHV = **35.9 MJ/Nm³** at standard conditions.
_(Kawasaki's own rating basis; heat rate 10,820–10,880 kJ/kWh for M7A-03D.)_

**Per unit (at 7,670 kW):**

- Hourly energy input: 7,670 kW × 10,820 kJ/kWh = 82,989,400 kJ/hr (~78.66 MMBtu/hr)
- Volumetric flow: 82,989,400 ÷ 35,900 kJ/Nm³ ≈ **2,311.68 Nm³/hr**

**Combined site (dual units):**

- **4,623.36 Nm³/hr**
- Mass equivalent (ρ ≈ 0.717 kg/Nm³): **~3,315 kg/hr (~3.3 t/hr)**

_(First-pass verification from chat: ~4,848 Nm³/hr using 8,000 kW & 10,880 kJ/kWh heat rate. Use the
factor-verified 4,623 Nm³/hr for design basis; ambient temp, altitude, part-load, and gas quality
shift actual consumption.)_

## Storage & Receipt Architecture

```
[CNG Truck Discharge] ===> [Central Filling Station]
                                   ||
                    +--------------+--------------+
                    |                             |  (Automated Equalization)
                    v                             v
          [CNG Storage Tank 1] <====================> [CNG Storage Tank 2]
                    |        (Level-Balancing Line)    |
                    +--------------+--------------+
                                   ||
                                   v
                       [Pressure Reduction Skid]
                       (250 bar → turbine inlet)
                                   ||
                     +-------------+-------------+
                     v                           v
             [Kawasaki GT-1]             [Kawasaki GT-2]
```

### Operating logic

- **Offloading:** truck discharge at high pressure (~250 bar) through a single localized
  refilling/truck offload station into the two storage vessels.
- **Balanced drawdown/fill:** the two tanks are interconnected via a differential-pressure control
  loop and level-balancing line, so both receipt and extraction occur at perfectly balanced rates —
  eliminates asymmetric pressure loading, gives a uniform low-pulsation fuel stream to the pressure
  reduction skid.
- **Pressure reduction skid:** steps 250 bar down to the Kawasaki fuel-gas valve unit (GVU) inlet
  requirement.
- **Safety:** dedicated CNG Storage Setback Zone; fixed gas detection linked to hard-wired ESD;
  auto-isolates tank line valves at ≥10% of Lower Explosive Limit (LEL).

## Closed-Loop Water/Steam Train (BOP)

```
 Feedwater Storage Tank → Feedwater Pump Skid → HRSG Economizer
    ↑                                                    ↓
 Condensate Return Tank ← Surface Condenser ← Siemens SST-200 ← HRSG Superheated Steam
```

Fully closed cycle: treated water, HP feed injection, steam expansion, condenser, condensate return.

---

_Sources: Gemini export 6_39_44 §5; fuel-thread verification in `New Microsoft Word Document.docx`; plant_layout.docx (fuel train)._

