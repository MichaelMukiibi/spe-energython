# Modeling Methodology

Approach follows the principle **physics before finance**, per the model layers:

```
Physical → Operational → Revenue + Cost → Cash Flow → NPV/IRR → Sensitivity
```

## 1. Physical Model

Hourly engineering simulation of the CCGT:

- **Generation:** net plant capacity (gross − parasitic) ~19.6 MWe; combined-cycle efficiency 0.44;
  simple-cycle GT heat rate 10,820 kJ/kWh.
- **Fuel:**
  ```
  gas_energy_MMBtu = generated_MWh × 3.412 / η_cc
  gas_nm3 = gas_energy_MMBtu × (1,055.06 MJ/MMBtu) / LHV_MJ_per_nm3
  ```
  Design check: 20.06 MW × 3.412 / 0.44 ≈ 155.6 MMBtu/h ≈ 157.3 MMBtu/h (research figure).
- **Waste heat → electricity:** HRSG steam (34 t/h @ 3.8 MPa) → SST-200 → 4.72 MWe.
- **Grid interface:** net generation vs data-center facility load ⇒ export (surplus) or import
  (deficit) at the 33 kV PCC.

## 2. Operational Model

- **Dispatch:** meet hourly DC load with 2x GT + ST; ST tracks GT exhaust (bottoming), GT(s) follow
  load.
- **Availability:** 8,000 h/yr utilisation; availability 0.95 / forced-outage 0.05 (working;
  refined by `models/operational/reliability.py`).
- **Redundancy:** one-GT-out capability still serves the DC load band; grid import is the backstop.
- **CNG supply reliability:** storage buffer absorbs truck-delivery windows (separate from engine
  availability).

## 3. Revenue Model

- **Energy payments:** delivered MWh × PPA energy price (data center) + exported MWh × export price.
- **Capacity payments:** $/month subject to availability performance.
- PPA term: 20 yr, 2%/yr escalation (working).

## 4. Financial Model

- **CAPEX:** the next module to define ($/kW for GT packages, HRSG, SST-200, CNG station,
  transformers/switchgear, BOP, EPC, owners' costs).
- **OPEX:** fuel (consumption × delivered $/MMBtu) + fixed/variable O&M + CNG logistics + insurance.
- **Financing:** debt share 0.70 @ 8%/15-yr; equity hurdle 12%.
- **Cash flows:** project + equity; taxes; depreciation.
- **Returns:** NPV at discount/WACC 10%; IRR; payback.

## 5. Sensitivity & Scenarios

- Sweeps (see `scenarios/sensitivity.yaml`): fuel price ($6–10.5/MMBtu), PPA energy price, capacity
  payment, availability, financing, DC load scenario.
- Point scenarios: `high_gas_price.yaml`, `low_gas_price.yaml` (overrides on `baselines.yaml`).
- Tornado charts for shark-pitch defensibility.

## Validation

- All assumptions traceable: locked engineering from `technical-team-research/`, financial `WORKING`
- Unit tests per module (see `docs/05_validation.md` and `/tests` after build)
- Cross-check: fuel consumption recomputed from first principles (MWh ↔ MMBtu ↔ Nm³)