# Sources

Research phase is **CLOSED**. All engineering inputs trace to the consolidated record in
`research/technical-team-research/`. Original files were merged into the markdown documents there;
this file is the top-level inventory.

## Manufacturer datasheets & brochures

| Source                                                                                      | What it supports                                                                              |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Kawasaki GPB80D (M7A-03D) datasheet (`technical-team-research/assets/datasheets/01-...pdf`) | Chosen GT: 7.67–7.81 MWe, 33.3–33.6% eff, 27.11 kg/s @ 526°C exhaust, heat rate 10,820 kJ/kWh |
| Kawasaki GPB180D datasheets (`02-...pdf`, `03-...pdf`)                                      | Rejected larger model (evaluation basis)                                                      |
| Siemens GT portfolio brochure (`04-...pdf`, gitignored, re-downloadable)                    | Turbine comparison: SGT-750 (41 MWe), SGT-A35 (34–36.5 MWe) rejection rationale               |
| Siemens CCPP offshore brochure (`05-...pdf`, gitignored)                                    | CCGT context / multi-shaft configurations                                                     |
| Siemens combined-cycle web PDF (`06-...pdf`, gitignored)                                    | CCPP design overview, single vs multi-shaft                                                   |

## Original research session exports (merged → `research/technical-team-research/research/`)

| Merged doc                    | Original sources                                                                                            |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 01-ccpp-design-report.md      | 2x Gemini comprehensive reports, `Act as a Senior Power Plant Systems Engineer...`, `what is critical here` |
| 02-gas-turbine-selection.md   | `Act as a Senior...`, `what is critical here`                                                               |
| 03-steam-turbine-selection.md | `So, which series...`, `New Microsoft Word Document` (verification)                                         |
| 04-generators.md              | BRUSH DG overview, Siemens SGM analysis, Marelli (voltage/rating/compat/6.6 kV) chat exports                |
| 05-hrsg-thermal-modeling.md   | `Uh so if we are finding out...`, Gemini exports §3                                                         |
| 06-electrical-topology.md     | `So when they go to grid...`, image-topology chat, `I have finally understood you...`                       |
| 07-fuel-logistics.md          | Gemini export §5 (CNG virtual pipeline), fuel thread in `New Microsoft Word Document`                       |
| 08-plant-layout.md            | `plant_layout.docx`, `New Microsoft Word Document`, `plant_layout.html` (3D)                                |

## CS#1 data center & load profiling (this repo)

- `data/load_profiles/*.csv` — 8,760-hr synthetic demand, 3 scenarios × [final + 3 phases]
- `data/config/parameters.yaml` — DC config: PUE 1.25, rack zones, phases (10/15/20 MW)
- `docs/cs1_data_center/` — it-sizing-spec.md, pue-benchmark-memo.md, load-profiling-spec.md

## Regulatory / infrastructure anchors

- **TCN** — Transmission Company of Nigeria; 33 kV grid code, PCC interconnection.
- **NESREA** — Nigerian emissions/environmental standards (stack ≥ 32 m, DLE NOₓ < 15 ppm).
- **API 612** — steam turbine special-purpose standard (equipment compliance).
- **Nigeria upstream gas** — domestic natural-gas availability rationale for site selection
  (CNG/LNG selection notes in `research/07-fuel-logistics.md`).

## Domain definitions

See challenge briefs and `technical-team-research/research/00-competition-overview.md`
(PUE, DCiE, CHP, BESS, take-or-pay, PAR, etc.).
