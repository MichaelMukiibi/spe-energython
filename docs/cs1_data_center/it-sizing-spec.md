# IT Architecture Sizing Specification

**SPE AMTS Energython 2026 — Data Center Architecture & Load Profiling (CS #1)**

## 1. Executive Summary

This specification defines the IT compute infrastructure for a 10–20 MW natural gas-powered data center campus in tropical Africa. The facility deploys in **3 phases**, scaling from 7.69 MW to 16.67 MW net IT capacity, with PUE improving from 1.30 to 1.20 as chiller utilization increases.

| Phase       | Gross MW | PUE  | IT MW | Racks | Purpose                             |
| ----------- | -------- | ---- | ----- | ----- | ----------------------------------- |
| **Phase 1** | 10.0     | 1.30 | 7.69  | 250   | Initial deployment, prove the model |
| **Phase 2** | 15.0     | 1.25 | 12.00 | 360   | Scale to meet demand                |
| **Phase 3** | 20.0     | 1.20 | 16.67 | 490   | Full build-out, maximum revenue     |

**Why PUE improves with scale**: At partial load (Phase 1, 50% chiller utilization), cooling systems run below optimal efficiency. At full load (Phase 3, 95%+ utilization), hybrid liquid cooling achieves peak COP.

## 2. Facility Power Envelope

$$E_{\text{IT}} = \frac{E_{\text{Total}}}{\text{PUE}}$$

| Phase   | Gross MW | PUE  | IT MW | DCiE  | Overhead |
| ------- | -------- | ---- | ----- | ----- | -------- |
| Phase 1 | 10.0     | 1.30 | 7.69  | 76.9% | 0.30     |
| Phase 2 | 15.0     | 1.25 | 12.00 | 80.0% | 0.25     |
| Phase 3 | 20.0     | 1.20 | 16.67 | 83.3% | 0.20     |

## 3. Rack Density Allocation

Compute halls are partitioned into three density tiers to support heterogeneous workloads:

| Zone       | Workload                        | Density     | Phase 1                | Phase 2                 | Phase 3                 |
| ---------- | ------------------------------- | ----------- | ---------------------- | ----------------------- | ----------------------- |
| **Zone A** | Enterprise Cloud / SaaS         | 20 kW/rack  | 180 racks (3.6 MW)     | 250 racks (5.0 MW)      | 330 racks (6.6 MW)      |
| **Zone B** | High-Performance Computing      | 50 kW/rack  | 60 racks (3.0 MW)      | 80 racks (4.0 MW)       | 120 racks (6.0 MW)      |
| **Zone C** | AI LLM Training & Deep Learning | 100 kW/rack | 10 racks (1.0 MW)      | 30 racks (3.0 MW)       | 40 racks (4.0 MW)       |
| **Total**  | Combined Compute Estate         | —           | **250 racks (7.6 MW)** | **360 racks (12.0 MW)** | **490 racks (16.7 MW)** |

### Zone Deployment Strategy

1. **Phase 1 (Cloud-First)**: Deploy 180 cloud racks + 60 HPC racks + 10 AI immersion racks. Cloud provides fastest revenue; HPC and initial AI prove the model.
2. **Phase 2 (Full Scale)**: Expand all zones to full capacity. 360 racks, 12 MW IT — the target operating point.
3. **Phase 3 (Maximum Revenue)**: Expand all zones by ~30%. 490 racks, 16.67 MW IT — full build-out.

## 4. Zone Design Rationale

### Zone A — Standard Cloud

- **Workload**: General enterprise cloud, SaaS hosting, web serving, API gateways
- **Power profile**: Bursty, latency-sensitive, CPU-heavy, diurnal demand curves
- **Cooling**: Traditional hot/cold aisle containment with chilled water CRAC units
- **Rationale**: Cloud racks are the revenue baseline; enterprise clients expect standard 10–20 kW densities

### Zone B — High-Density HPC

- **Workload**: Scientific computing, CFD simulations, financial modeling, data analytics
- **Power profile**: Sustained high utilization (80–95%), long-duration jobs
- **Cooling**: Direct-to-Chip cold plate liquid cooling for racks exceeding 30 kW
- **Rationale**: HPC workloads justify higher capital cost per rack through premium pricing; D2C cooling at 50 kW is the industry sweet spot for non-AI dense compute

### Zone C — AI Immersion

- **Workload**: LLM pre-training, fine-tuning, deep learning at scale
- **Power profile**: Near-constant 95–100% GPU utilization for days/weeks; idle power 30–40% of peak
- **Cooling**: Single-phase liquid immersion tanks (dielectric fluid, $C_p \approx 2.1 \text{ kJ/kg·K}$)
- **Rationale**: AI racks push beyond air/D2C limits; immersion cooling achieves PUE 1.08–1.15 and eliminates water consumption

## 5. Power Distribution

- **Architecture**: 800V DC distribution to reduce copper usage by 45% and conversion losses
- **UPS**: Modular 250–2500 kVA blocks (pay-as-you-grow); target 40–60% load efficiency
- **Redundancy**: N+1 for Zones A/B; 2N for Zone C (AI training interruption cost is severe)

## 6. Cross-Role Deliverables

| Output                             | Consuming Role  | Purpose                                     |
| ---------------------------------- | --------------- | ------------------------------------------- |
| Hourly MW Load Profile (per phase) | Electrical Eng  | Generator capacity sizing, UPS battery calc |
| Rack Density by Zone (per phase)   | Mechanical Eng  | Cooling flow rates ($\dot{m}$), pipe layout |
| PUE Sensitivity by Phase           | CS #2 (Finance) | OPEX projection, LCOE calculation           |
| Peak-to-Average Ratio              | Electrical Eng  | Generator over-provisioning factor          |

---

_Generated by `src/it_sizing/` — see `data/output/csv/` for raw data._
