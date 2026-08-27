# SPE Energython Research — Cleaned & Consolidated

This folder consolidates the team's research on the **20 MW Combined Cycle Power Plant (CCPP)**
for a co-located AI data center in Nigeria. Original files were AI-chat exports, datasheets, and
layout artifacts in a messy, duplicated state; they are merged below by topic.

## Index

| Doc | Covers | Original sources it merges |
|---|---|---|
| **00-competition-overview.md** | Challenge scope, scoring weights (Innov 20 / Rigor 25 / Fin 25 / Pres 30), team context | Competition flyer (assets/images/01-competition-flyer.jpeg) |
| **01-ccpp-design-report.md** | Full plant design + revenue/engineering summary: 20.06 MWe gross, 43.5-45% CC efficiency, generator architecture, control, site quadrants, next milestone (LCOE) | `Gemini Export ...6_32_12...docx`, `Gemini Export ...6_39_44...docx`, `what is critical here.docx`, `Act as a Senior Power Plant Systems Engineer...docx` |
| **02-gas-turbine-selection.md** | Why 2x Kawasaki GPB80D (M7A-03D) / 15.34 MWe; rejection of SGT-750, SGT-A35, GPB180D; decision matrix | `Act as a Senior Power Plant Systems Engineer...docx`, `what is critical here.docx` (+1 duplicate copy) |
| **03-steam-turbine-selection.md** | Siemens SST-200 (4-20 MW): SST-200 vs SST-400 vs SST-600, specs, recommended configuration | `So, which series do you recommend...docx`, `New Microsoft Word Document.docx` (verification) |
| **04-generators.md** | GT gensets = BRUSH 4-Pole DG; ST genset = Marelli MJH 710/900 @ 6.6 kV; SGM marine series rejected | `BRUSH 4-Pole DG Range Overview.docx` (+`(1)` near-dup), `why is the siemens energy SGM series...docx` (+`(1)` dup), `tell me about the Marelli,Lorren...docx`, `what is the output voltage...docx`, `whats its rating...docx`, `which marelli motori...6.6kv.docx`, `New Microsoft Word Document.docx` (generator thread) |
| **05-hrsg-thermal-modeling.md** | Dual-inlet unfired HRSG: combined 195,200 kg/h @ 526°C → ~34 t/h steam @ 3.8 MPa/420°C; pinch/superheat/stack constraints; workflow | `Uh so if we are finding out...docx`, Gemini exports §3 |
| **06-electrical-topology.md** | 6.6 kV sync bus (3 incomers), T1/T2 (15 MVA 6.6/33 kV), TCN grid sync (4 factors), BTM data-center tap, 415 V rack current logic | `So when they go to grid...docx`, `I want you to look through that image...docx`, `I have finally understood you...docx`, Gemini exports §6 |
| **07-fuel-logistics.md** | CNG virtual pipeline: 4,623 Nm³/hr / ~3.3 t/hr fuel, 250-bar truck offload, level-balanced dual tanks, pressure-reduction skid, LN G rejection, water/steam BOP loop | Gemini export 6_39_44 §5, fuel thread in `New Microsoft Word Document.docx` |
| **08-plant-layout.md** | Site GA: functional quadrants, inline parallel dual-train, NESREA stack, 3D model mapping, closed-loop water/steam | `plant_layout.docx`, `New Microsoft Word Document.docx`, `plant_layout*.html` (3 variants → best kept), Gemini 6_39_44 §9 |

## Non-documentation assets (`../assets/`)

| Path | Contents |
|---|---|
| `datasheets/01-kawasaki-gpb80d-datasheet.pdf` | Chosen turbine spec (7.81 MW / 33.6% / 27.3 kg/s / 526°C, EN-DE) |
| `datasheets/02-kawasaki-gpb180d-datasheet.pdf` | Kawasaki GPB180D (rejected model) |
| `datasheets/03-kawasaki-gpb180d-kga-datasheet.pdf` | GPB180D (KGE variant) |
| `datasheets/04-siemens-gt-portfolio-brochure.pdf` | Siemens full GT portfolio (SGT-100→SGT-A35), 78 MB — basis of the turbine comparison |
| `datasheets/05-siemens-ccpp-offshore-brochure.pdf` | Siemens offshore CCPP (SGT-750/SGT-A35 context) |
| `datasheets/06-siemens-combined-cycle-web.pdf` | Siemens CCPP overview + single/multi-shaft |
| `images/*` | Competition flyer, CCGT reference, 2-Kawasaki-1-steam photo, Kawasaki 8 MW engine |
| `plant-layout.html` | Interactive 3D plant layout (drag to rotate, scroll to zoom) |

## Removed / Archived

- **`archive/01-hydropower-plant-models.pdf`** — unrelated academic paper (hydro PID modeling);
  kept for reference only.
- **Deleted as duplicates** (content preserved in the merged docs above):
  - `energython/` subfolder (all 11 files were duplicates of root files)
  - `what is critical here(1).docx`, `BRUSH 4-Pole DG Range Overview(1).docx`,
    `why is the siemens energy SGM series...(1).docx`, `kga-com-my-product-gpb180d-... (1).pdf`
  - `plant_layout-2.html`, `plant_layout__1_ (3).html` (variants; best kept as assets/plant-layout.html)