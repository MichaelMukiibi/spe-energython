# Load Profiling Specification

**SPE AMTS Energython 2026 — Data Center Architecture & Load Profiling (CS #1)**

## 1. Executive Summary

This document defines the methodology for generating synthetic 8760-hour IT load profiles across a **3-phase deployment** (10→15→20 MW gross). Three scenarios — Cloud-Heavy, AI-Heavy, and Mixed — model distinct workload compositions. The profiles capture diurnal cycles, weekend effects, GPU idle draw (30–40% of peak), and stochastic variation, scaled to each phase's IT capacity.

| Phase   | Gross MW | PUE  | IT MW | Peak Cloud | Peak AI  | Peak Mixed |
| ------- | -------- | ---- | ----- | ---------- | -------- | ---------- |
| Phase 1 | 10.0     | 1.30 | 7.69  | 8.08 MW    | 8.08 MW  | 8.08 MW    |
| Phase 2 | 15.0     | 1.25 | 12.00 | 12.60 MW   | 12.60 MW | 12.60 MW   |
| Phase 3 | 20.0     | 1.20 | 16.67 | 17.50 MW   | 17.50 MW | 17.50 MW   |

## 2. Load Profile Methodology

### 2.1 Power Model

At facility level:

$$P_{\text{IT}}(t) = P_{\text{Idle}} + P_{\text{AI\_Batch}} + P_{\text{Cloud}}(t) + \epsilon(t)$$

Where:

- $P_{\text{Idle}}$ = baseline draw from idle servers, networking, fans (35% of peak)
- $P_{\text{AI\_Batch}}$ = sustained AI training floor (scenario-dependent)
- $P_{\text{Cloud}}(t)$ = time-varying cloud/enterprise component
- $\epsilon(t)$ = stochastic noise (±3% Gaussian)

### 2.2 Diurnal Shape

Cloud workloads follow a Gaussian diurnal profile peaking at 14:00 local time:

$$D(h) = \exp\left(-\frac{(h - 14)^2}{2 \cdot 6^2}\right)$$

Weekend reduction: 70% of weekday amplitude (business SaaS drops on weekends).

### 2.3 Facility Load

$$P_{\text{Facility}}(t) = P_{\text{IT}}(t) \times \text{PUE}$$

PUE varies by phase: 1.30 (Phase 1), 1.25 (Phase 2), 1.20 (Phase 3).

### 2.4 Phase-Aware Scaling

The same diurnal and scenario shapes apply across phases, but absolute MW values differ based on IT capacity:

$$P_{\text{IT,phase}}(t) = P_{\text{IT,normalized}}(t) \times \text{IT}_{\text{capacity,phase}}$$

Where $\text{IT}_{\text{capacity,phase}}$ is 7.69 MW (Phase 1), 12.00 MW (Phase 2), or 16.67 MW (Phase 3).

## 3. Scenario Definitions

| Parameter                     | Cloud-Heavy                       | AI-Heavy                          | Mixed                          |
| ----------------------------- | --------------------------------- | --------------------------------- | ------------------------------ |
| Peak utilization              | 95%                               | 98%                               | 92%                            |
| Off-peak utilization          | 45%                               | 80%                               | 55%                            |
| Diurnal amplitude             | 0.50                              | 0.10                              | 0.30                           |
| AI batch floor (% of compute) | 15%                               | 70%                               | 40%                            |
| **Character**                 | High variance, distinct day/night | Sustained flat peaks, minimal dip | AI base + cloud diurnal spikes |

### 3.1 Cloud-Heavy

- Enterprise SaaS, API traffic, web hosting dominate
- Strong day/night cycle with large amplitude
- AI batch jobs fill only 15% of available overnight capacity

### 3.2 AI-Heavy

- LLM training runs at 95–100% GPU utilization for days
- Minimal diurnal variation (training doesn't follow business hours)
- High off-peak floor (80% of capacity)

### 3.3 Mixed (Recommended Baseline)

- AI training provides a moderate floor (40% of compute headroom)
- Cloud/inference adds diurnal spikes on top
- Most realistic for a multi-tenant facility

## 4. Key Metrics by Phase

### Phase 1 (10 MW Gross / 7.69 MW IT)

| Scenario    | Avg IT (MW) | Peak IT (MW) | Min IT (MW) | PAR  |
| ----------- | ----------- | ------------ | ----------- | ---- |
| Cloud-Heavy | 6.49        | 8.08         | 4.97        | 1.24 |
| AI-Heavy    | 7.54        | 8.08         | 6.56        | 1.07 |
| Mixed       | 6.94        | 8.08         | 5.83        | 1.16 |

### Phase 2 (15 MW Gross / 12 MW IT)

| Scenario    | Avg IT (MW) | Peak IT (MW) | Min IT (MW) | PAR  |
| ----------- | ----------- | ------------ | ----------- | ---- |
| Cloud-Heavy | 10.13       | 12.60        | 7.75        | 1.24 |
| AI-Heavy    | 11.76       | 12.60        | 10.24       | 1.07 |
| Mixed       | 10.83       | 12.60        | 9.09        | 1.16 |

### Phase 3 (20 MW Gross / 16.67 MW IT)

| Scenario    | Avg IT (MW) | Peak IT (MW) | Min IT (MW) | PAR  |
| ----------- | ----------- | ------------ | ----------- | ---- |
| Cloud-Heavy | 14.07       | 17.50        | 10.77       | 1.24 |
| AI-Heavy    | 16.33       | 17.50        | 14.22       | 1.07 |
| Mixed       | 15.05       | 17.50        | 12.63       | 1.16 |

## 5. Deliverables

| Output               | Format | Location                                                    |
| -------------------- | ------ | ----------------------------------------------------------- |
| 9 hourly load curves | CSV    | `data/output/csv/load_profile_phase_{1,2,3}_{scenario}.csv` |
| Diurnal profiles     | PNG    | `data/output/figures/diurnal_profiles.png`                  |
| Annual profiles      | PNG    | `data/output/figures/annual_profiles.png`                   |
| Facility vs IT load  | PNG    | `data/output/figures/facility_vs_it_load.png`               |
| Phase comparison     | PNG    | `data/output/figures/phase_comparison.png`                  |

---

_Generated by `src/load_profiling/` — run `make profiles` to regenerate._
