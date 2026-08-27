# System Architecture

## Power Block — 2x1 Combined Cycle (CCGT)

```
   [CNG Storage Vessel 1] <══level-balance══> [CNG Storage Vessel 2]
            └──────────────┬───────────────┘
                           │ 250 bar → pressure-reduction skid
                           ▼
        ┌──────────────────┴──────────────────┐
        │  Kawasaki GT-1 (7.67 MWe, GPB80D)   │
        │  Kawasaki GT-2 (7.67 MWe, GPB80D)   │
        └──────────────┬─────────────────────┘
              exhaust  │ 2 x 27.11 kg/s @ 526°C
                       ▼
        [ Dual-Inlet Unfired HRSG ]
                       │ ~34 t/h steam @ 3.8 MPa, 420°C
                       ▼
        [ Siemens SST-200, 4.72 MWe ]
                       ▼
        [ Surface Condenser → feedwater loop ]
```

## Electrical Topology

```
 GT-1 gen (6.6 kV) ─┐
 GT-2 gen (6.6 kV) ─┤→ 6.6 kV Main Switchgear (sync bus, 3 incomers) → aux transf. 6.6→0.4 kV
 ST  gen (6.6 kV) ─┘              │
                                  ├── T1 (15 MVA, 6.6/33 kV) ─┐
                                  ├── T2 (15 MVA, 6.6/33 kV) ─┤→ TCN PCC at 33 kV (grid export/import)
                                  │
                                  └── DC feeder breakers → DC step-down → AI data center
```

- **Behind-the-meter:** data center tapped at MV switchgear (avoids double transformation).
- **Grid-tied:** surplus → TCN 33 kV; deficits/outages backed by grid import.
- Plant parasitic load: 0.46 MW (pumps, controls, compressors).

## Data & Model Data Flow

```
data/load_profiles/*.csv  ─┐
data/config/parameters.yaml─┤→ Physical model (generation, fuel, net/export)
scenarios/baselines.yaml ──┘        │
                                    ▼
                            Operational model (dispatch, availability)
                                    ▼
                            Revenue (energy + capacity) ─┐
                            CAPEX / OPEX ───────────────┤→ Cash flows → NPV / IRR
                            Financing ──────────────────┘
                                    ▼
                            Sensitivity / scenario sweep → results
```

## Directories

- `models/` — physical, operational, financial modules (build in progress)
- `data/` — CS#1 load profiles and DC config
- `scenarios/` — parameter files (canonical: `baselines.yaml`)
- `analysis/` — sensitivity, optimization, results
- `research/technical-team-research/` — locked engineering record