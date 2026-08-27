# Data

## `load_profiles/` — 8760-hour demand curves (CS#1)

Synthetic hourly facility load for the 10–20 MW data center, one CSV per scenario × deployment
phase. Shared schema:

| Column | Description |
|---|---|
| `hour` | 0–8759 sequential hour index |
| `hour_of_day` | 0–23 |
| `day_of_year` | 1–366 |
| `it_load_kw` | IT-side electrical demand (kW) |
| `facility_load_kw` | Facility demand incl. cooling = IT × PUE (kW) |
| `utilization` | Fraction of rated IT capacity |
| `scenario` | `mixed` / `ai_heavy` / `cloud_heavy` |

Files:

- **Final-phase profiles (plant's baseline load):**
  - `load_profile_mixed.csv`  ← **canonical baseline** for the techno-economic model
  - `load_profile_ai_heavy.csv`
  - `load_profile_cloud_heavy.csv`
- **Phase ramp profiles** `load_profile_phase_{1,2,3}_{scenario}.csv` — 10 / 15 / 20 MW facility
  envelopes for the staged roll-out (Phase 1 → 2 → 3).

> The financial model's demand driver is `facility_load_kw`. The base case is the **mixed** scenario
> at final phase; `ai_heavy` / `cloud_heavy` are sensitivity scenarios.

## `config/parameters.yaml` — data-center configuration

Single source for DC-side parameters consumed by the model:

- facility: PUE 1.25, 12.0 MW IT within 15.0 MW
- deployment phases (10 / 15 / 20 MW) with zone builds (cloud → HPC → AI immersion)
- cooling mix (40% air, 35% direct-to-chip, 25% immersion)
- rack zones (250 @ 20 kW, 80 @ 50 kW, 30 @ 100 kW)
- GPU idle ratio 0.35, CPU idle 0.30
- load-profiling scenario params (peaks, diurnal amplitude, AI batch fraction)
- tropical climate + cooling-technology PUE ranges (for the PUE benchmark memo)

## Plant-side parameters

Not in `data/` — plant parameters live in `scenarios/baselines.yaml` (engineering locked;
financial working). `docs/04_assumptions.md` is the human-readable register.