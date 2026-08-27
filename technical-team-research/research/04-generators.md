# Generator Selection — GT Generators & ST Generator

> Merged from 7 research exports: `BRUSH 4-Pole DG Range Overview.docx`,
> `why is the siemens energy SGM series synchronous generator best fit for the siemens SST 200 steam turbine.docx`,
> `tell me about the Marelli,Lorren synchronous generator.docx`,
> `what is the output voltage of the marelli motiri.docx`,
> `whats its rating and is it compatible with the siemens sst 200 steam turbine.docx`,
> `which marelli motori synchronous generator compatible with ghe siemens sst 200 steam turbine gives output voltage of 6.6kv.docx`,
> and the generator verification thread within `New Microsoft Word Document.docx`.

## Final Selection Summary

| Machine | Generator | Specs |
|---|---|---|
| 2x Kawasaki GPB80D (gas turbine) | **BRUSH 4-Pole DG Series** synchronous turbogenerator | Air-cooled, salient-pole, brushless excitation; 1,500 rpm (50 Hz); 6.6 kV terminal; up to 15 kV; 10–65 MVA range |
| 1x Siemens SST-200 (steam turbine) | **Marelli Motori MJH 710/900 High/Medium Voltage** synchronous generator | Natively wound 6.6 kV; 4-pole (1,500 rpm) or 6-pole (1,000 rpm); D-Vo digital AVR; up to 12,500 kVA |

> **Decision context:** the marine **Siemens Energy SGM (Shaft Generator Motor) series** was
> originally under evaluation for the SST-200 but was **rejected** — it is designed for shipboard
> WHRS/PTI-PTO duty, not stationary grid-parallel power generation. Verified via datasheet review:
> Siemens' in-house SGen-100A/1000A land lines start at ~25 MVA, over 4x too large for the
> ~6.25 MVA 5 MW steam turbine, so the SST-200 package pairs with a partner OEM.
> The Marelli MJH series is the confirmed replacement.

## BRUSH 4-Pole DG Series (Gas Turbine Generators)

High-performance, air-cooled, salient-pole synchronous turbogenerators for gas & steam turbine
interfaces; 750+ active installations globally (utilities, geothermal, heavy industry, offshore,
CHP).

**Core specifications**
- Output: 10–75 MVA (typically 10–55 MVA at 40°C reference)
- Speed: 1,500 rpm (50 Hz) or 1,800 rpm (60 Hz)
- Voltage: up to 15 kV
- Service life: ≥25 years
- Excitation: integrated brushless system (no carbon brushes / slip rings / commutators)

**Design features**
- One-piece forged rotor (de-gassed, vacuum-poured, stress-relieved alloy steel)
- Mild-steel stator with laminated high-silicon electrical-steel core + radial ventilation ducts
- Class F insulation, aramid-and-epoxy resin matrix on copper strip coils
- Standardized modular architecture; custom interfaces for major turbine OEM reduction gearboxes
- Cooling: open air circuit, or closed circuit (TEWAC/CACW) for harsh environments
- Rigorous full-load factory testing; simplified civil footprint

**Fit note:** an 8 MW gas turbine at ~0.8 PF needs ≈10 MVA — at the bottom of the DG range.
Custom-winding near the bottom of the range is common; exact frame/model requires a formal quote
citing "M7A-03D, 8 MW, 50 Hz" from Brush/Baker Hughes.

## Marelli Motori MJH 710 / MJH 900 (Steam Turbine Generator)

High-efficiency industrial three-phase alternators for marine, oil & gas, hydropower, and
cogeneration duty.

**Key features**
- Brushless self-excited system with AVR, voltage regulation within ±0.5%
- Class H insulation with VPI resin treatment
- Oversized bearings + dynamic balancing
- Up to IP55; dual-frequency (50/60 Hz); optional temp/vibration sensors
- MJH 710/900 = the medium/high-voltage platform (voltage band 1,000–7,200 V includes 6.6 kV)

**Voltage classes (Marelli range)**
- LV: 380–1,000 V (400/440/480/690 V)
- MV: 1,000–7,200 V (**3.3 kV and 6.6 kV** — our target) ← selected
- HV: 7,200–15,000 V (11/13.8/15 kV)

**Rating & compatibility with SST-200**
- Range: 10 kVA up to 12,500 kVA (12.5 MVA)
- SST-200 runs 4–20 MW; MJH 710/900 largest frames reach 12.5 MVA → matches lower-to-middle
  spectrum (~4–10 MW) of the SST-200 duty
- A **speed-reduction gearbox** is mandatory between the high-speed SST-200 shaft and the 4-pole
  (1,500/1,800 rpm) or 6-pole (1,000/1,200 rpm) generator
- Both units comply with IEC, ISO, API 612
- **D-Vo digital AVR** standard on frames ≥ 800 and all MV/HV machines — strict voltage stability
  under shifting steam turbine thermal loads

## System Wiring Note (from final verification)

- Kawasaki generator sync speed: 1,500 rpm (4-pole at 50 Hz) — the M7A-03D rotor is 13,790 rpm,
  reduced via gearbox.
- 6.6 kV keeps generator current manageable and avoids double transformation losses at the plant
  (see 06-electrical-topology.md).

---

*Sources: `BRUSH 4-Pole DG Range Overview.docx` (+ `(1)` near-duplicate, identical content); `why is the siemens energy SGM series...docx` (+ `(1)` duplicate); `tell me about the Marelli,Lorren synchronous generator.docx`; `what is the output voltage of the marelli motiri.docx`; `whats its rating and is it compatible with the siemens sst 200 steam turbine.docx`; `which marelli motori synchronous generator compatible with ghe siemens sst 200 steam turbine gives output voltage of 6.6kv.docx`; generator thread within `New Microsoft Word Document.docx`.*