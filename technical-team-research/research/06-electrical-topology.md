# Electrical Topology & Grid Interconnection

> Merged from `So when they go to grid, how does synchronization .._.docx` (grid sync + data center
> power tap), `I want you to look through that image very well an.._.docx` (switchgear topology),
> and `I have finally understood you. We are looking at.._.docx` (voltage vs current nuance),
> plus §6 of the 6_39_44 Gemini export.

## Power Pooling Sequence

```
+--------------------+   +--------------------+   +--------------------+
| Kawasaki GT-1 Gen  |   | Kawasaki GT-2 Gen  |   | Siemens SST-200 Gen|
|   6.6 kV Output    |   |   6.6 kV Output    |   |   6.6 kV Output    |
+---------+----------+   +---------+----------+   +---------+----------+
          |                        |                        |
          v                        v                        v
+----------------------------------------------------------------------+
|             MAIN SWITCHGEAR / SYNCHRONIZED BUSBAR BLOCK             |
|                 (6.6 kV, Sync Bus, 3 Incomers)             |
+----------------------------------+-----------------------------------+
                     +-------------+-------------+
                     v                           v
         +-----------------------+   +-----------------------+
         | Step-Up Transformer T1|   | Step-Up Transformer T2|
         |  15 MVA, 6.6/33 kV    |   |  15 MVA, 6.6/33 kV    |
         +-----------+-----------+   +-----------+-----------+
                     +-------------+-------------+
                                   v
         =====================================================
         POINT OF COMMON COUPLING: TCN 33 kV UTILITY GRID LINK
         =====================================================
```

### Key points
- All three generators generate at a uniform **6.6 kV** and terminate into the **3 incomers** of the
  common 6.6 kV Main Switchgear sync busbar. Pooling at 6.6 kV avoids a dedicated step-up transformer
  for the steam turbine.
- Aggregated power is split and stepped up through **T1 & T2 (15 MVA each, 6.6→33 kV)** to interface
  with the **TCN grid**.
- An auxiliary step-down transformer taps 6.6 kV → 0.4 kV for plant house loads.

## Grid Synchronization — The 4 Factors

Before the main breaker closes, plant voltage, frequency, phase angle, and phase sequence must match
the grid. If out of sync, large electrical/mechanical forces can damage generators and trip the grid.

1. **Phase sequence (rotational direction):** A-B-C / R-Y-B must match the grid; verified permanently
   during commissioning via hardwiring and phase-rotation meters.
2. **Voltage magnitude:** T1/T2 high side (33 kV) must match grid within ±1–2%. The **Automatic
   Voltage Regulator (AVR)** adjusts DC excitation of all 3 synchronous generators until matched.
3. **Frequency:** must match within fractions of a Hz. Speed governors adjust GT fuel valves and ST
   steam admission valves.
4. **Phase angle:** an **Automatic Synchronizer** monitors waveforms across the open breaker and
   fine-tunes turbine speed until phase shift = 0° ("12 o'clock"), then closes the breaker.

## Tapping Power for the AI Data Center

In a BTM / co-location setup, power is **not** tapped from the 33 kV HV line. It is tapped directly
from the **MV Main Switchgear** (or an auxiliary busbar downstream):

```
[ 3x Turbines ] ──> [ MV Main Switchgear (Busbar) ] ──┬──> [ Step-Up T1 & T2 ] ──> [ 33kV Grid ]
                                                      │
                                                      └──> [ Step-Down / Local Tx ] ──> [ AI Data Center ]
```

- **Direct/island mode:** a dedicated feeder breaker inside the Main Switchgear feeds the data center
  via on-site step-down transformers (6.6 kV / 11 kV → 415 V / 480 V for racks and cooling).
  Taking power at MV avoids double-transformation losses (up to 33 kV and back down).
- **Bidirectional grid tie:**
  - *Surplus (plant > DC load):* data center consumes from the busbar; excess flows through T1/T2 to 33 kV grid.
  - *Deficit / maintenance:* power flows backward from the 33 kV grid through T1/T2 into the Main
    Switchgear to keep the data center online (grid backup).

## Why High Voltage (not "more power") — 415 V/480 V decision

Power = √3 × V × I × PF. Higher voltage does NOT mean more power; it lets you deliver large power
through manageable cable sizes. Copper cable current is physically capped (~60–100 A) before I²R
heating melts it:

| Supply Voltage | Type | Formula (≈) | Required Current | Cable / Feeder Result |
|---|---|---|---|---|
| 120 V | 1-Ph AC | P = V·I | 333 A | Unusable — cables as thick as a wrist |
| 208 V | 3-Ph AC | P = √3·V·I | 111 A | Exceeds standard 60/80 A rack whips; extreme heat |
| **415 V** | **3-Ph AC** | **P = √3·V·I** | **56 A** | **Ideal — fits standard 60 A cabling** |

Server hardware determines power demand (e.g., 72 GPUs → 100 kW); facility voltage determines the
efficiency/current trade-off. This same logic drives the plant-side choice of 6.6 kV MV generation:
manages current to avoid oversized conductors until the 33 kV step-up.

## From the Gemini export (additional detail)

- DCS commands generator control units to match the 4 sync parameters prior to breaker close.
- Synchronizing grid-protection relays at each generator breaker + anti-islanding protection trip the
  plant offline within code limits if grid connectivity fails. *(6_32_12)*
- Grid-tied (not island): confirmed by the requirement to export excess power whenever data center
  load < generation capability.

---

*Sources: `So when they go to grid, how does synchronization .._.docx`; `I want you to look through that image very well an.._.docx`; `I have finally understood you. We are looking at.._.docx`; Gemini export 6_39_44 §6; Gemini export 6_32_12 §3.*