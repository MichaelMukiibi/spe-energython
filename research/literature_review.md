# Literature & Technical Review Summary

Research phase is **CLOSED**. This review consolidates what the technical/research work established
(see `sources.md` and `research/technical-team-research/research/` for the full record).

## What was reviewed, and what it established

### 1. Gas-turbine selection (10–20 MW class)

- **Competing platforms:** Kawasaki GPB80D / GPB180D (7–18 MW), Siemens SGT-100 / SGT-750 /
  SGT-A35 (6–41 MW). Reviewed via manufacturer datasheets/brochures.
- **Outcome:** 2x1 CCGT with **Kawasaki GPB80D (M7A-03D)** selected — 7.67 MWe ISO, 33.6%
  simple-cycle, 526°C exhaust at 27.11 kg/s, DLE NOₓ < 15 ppm. Larger frames (SGT-750 41 MWe,
  SGT-A35 34–36.5 MWe, GPB180D 17.97 MWe) rejected as oversized for a 10–20 MW data-center block.
- Decision matrix and rationale: `02-gas-turbine-selection.md`.

### 2. Steam bottoming cycle / CC efficiency

- **Siemens SST-200 condensing** (4–20 MW frame) selected over SST-400/SST-600: 4.72 MWe at steam
  conditions 3.8 MPa / 420°C, ~34 t/h from a dual-inlet unfired HRSG.
- **Combined-cycle efficiency: 43.5–45.0%** (simple-cycle GT ≈ 33.3–33.6%). Waste heat converts to
  **electricity**, not cooling → this is a CCPP, not a CHP-for-chilling plant.
- `01-ccpp-design-report.md`, `03-steam-turbine-selection.md`, `05-hrsg-thermal-modeling.md`.

### 3. Heat recovery engineering (HRSG)

- Unfired, dual-inlet, single-pressure; combined exhaust 54.22 kg/s @ 526°C; steam superheat to
  380–420°C; pinch 10–15°C; stack ≥ 140°C (acid dew point). Recovery ≈ 82–85%.
- `05-hrsg-thermal-modeling.md`.

### 4. Electrical topology & grid code

- Generation at 6.6 kV on a sync bus (3 incomers: GT1, GT2, ST) → 2x 15 MVA 6.6/33 kV transformers →
  TCN 33 kV PCC. Behind-the-meter DC tap at MV; grid-tied export/import.
- `06-electrical-topology.md`.

### 5. Fuel strategy — CNG virtual pipeline (Nigeria)

- **CNG (compressed natural gas), trucked** — no LNG regas. Design basis LHV 35.9 MJ/Nm³, flow
  ~4,623 Nm³/h (~3.3 t/h), two level-balanced 250-bar vessels + pressure-reduction skid.
- Rationale vs LNG: Nigerian downstream/infrastructure reality, compression + trucking dominate
  delivered cost, take-or-pay alignment is a scheduling/commercial concern.
- `07-fuel-logistics.md`.

### 6. Data-center load & PUE (CS#1)

- 10–20 MW IT data center, 12.0 MW net IT within 15.0 MW facility; target **PUE 1.25** (tropical,
  hybrid air + direct-to-chip + single-phase immersion cooling); GPU idle 30–40% peak drives
  demand-curve shape; three 8,760-hr scenarios (mixed / AI-heavy / cloud-heavy).
- `docs/cs1_data_center/*`, `data/load_profiles/`.

### 7. Regulatory / standards anchors used

- TCN (grid code / PCC), NESREA (stack height ≥ 32 m, emissions), API 612 (steam turbines).
- Original competition brief and flyer: `00-competition-overview.md`.

## Gap between review and build

- **Financial values are WORKING, not literature-backed** ($/MMBtu CNG, PPA $/kWh, capacity payment,
  CAPEX $/kW, financing). Research phase closed → these are seeded in `scenarios/baselines.yaml`,
  flagged ⚠️, and carried by sensitivity analysis in the pitch.
- Next build steps: CAPEX module (highest remaining source of model uncertainty), then full pipeline
  execution and scenario sweeps.
