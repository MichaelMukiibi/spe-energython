# AMTS Natural-Gas Data Center Power Model

## What I Have Learned + Questions for the Engineering Team

### 1. What we are ultimately building

I am approaching the aMTS challenge as a coupled:

**Physical system model → operational model → techno-economic model → project-finance model**

The basic architecture is:

**Natural gas → gas engines → electricity + waste heat → data-center electricity/cooling → PPA revenue → OPEX/CAPEX → NPV/IRR**

The goal is not simply to calculate whether a gas plant can produce 10–20 MW. We need to model **how the plant actually operates**, how reliable it is, how much gas it consumes, how much useful heat can be recovered, and how those physical outputs translate into project economics.

---

# 2. What I have established so far

## Checkpoint 1–2: Power, energy and efficiency

If the data center requires 10 MW continuously for one hour:

[
E=P\times t=10\text{ MWh}
]

If the gas engine has 40% electrical efficiency:

[
E_{fuel}=\frac{10}{0.40}=25\text{ MWh}_{fuel}
]

Therefore, the first physical relationship is:

[
\boxed{Fuel\ Input \rightarrow Electrical\ Output}
]

### Questions for the team

**Petroleum Engineer**

* What natural-gas specification should we assume?
* What is a realistic gas price in the target African market?
* Should we model gas price in $/MMBtu, $/MSCF, or another unit?
* What gas quality/composition assumptions materially affect engine performance?

**Mechanical Engineer**

* Is 40% electrical efficiency realistic for the engine size/configuration we are considering?
* How does engine efficiency vary with load?
* Should we use a fixed efficiency or an engine heat-rate curve?

**Electrical Engineer**

* What electrical output should we expect from each engine?
* What operating load range is realistic before efficiency or reliability deteriorates?

### Model outputs we need

* Engine rated MW
* Electrical efficiency / heat rate
* Minimum stable operating load
* Efficiency versus load
* Gas consumption versus MW output

---

# 3. Checkpoint 3–5: Waste heat and CHP

For 25 MWh of fuel input and 10 MWh electrical output:

[
25-10=15\text{ MWh}_{th}
]

is rejected as heat.

If 60% is recoverable:

[
15\times0.60=9\text{ MWh}_{th}
]

If an absorption chiller has COP = 0.7:

[
9\times0.7=6.3\text{ MWh}_{cooling}
]

But if the data center only requires 2 MWh of cooling, we can only displace that 2 MWh of electrical cooling demand.

The key lesson:

[
\boxed{\text{Available energy} \neq \text{Useful energy}}
]

### Questions for the team

**Mechanical Engineer**

* What fraction of engine waste heat is realistically recoverable?
* Which heat sources should we model: exhaust, jacket water, lube oil?
* What temperature levels are available?
* What type of absorption chiller would be appropriate?
* What COP should we realistically use?
* Does chiller performance vary significantly with temperature/load?
* Are there thermal losses between the engine and chiller?

**Electrical Engineer**

* What is a realistic data-center cooling electricity demand relative to IT load?
* What cooling architecture should we assume?
* What PUE target is technically realistic?

**Petroleum Engineer**

* Does the engine technology affect the thermal recovery profile significantly?
* Are there gas-composition effects on combustion/engine heat output that should enter the model?

### Model outputs we need

* Waste heat available
* Recoverable heat fraction
* Heat-recovery efficiency
* Heat temperature
* Chiller COP
* Cooling load profile
* Electrical cooling demand displaced

---

# 4. Checkpoint 6: Natural-gas cost

We converted:

[
25\text{ MWh}_{fuel}\times3.412
=85.3\text{ MMBtu}
]

At $8/MMBtu:

[
Fuel\ Cost=85.3\times8
\approx$682
]

Therefore the physical model needs to produce **fuel consumption**, which the financial model converts into fuel expenditure.

### Questions for the Petroleum Engineer

* What is a realistic delivered natural-gas price for the project location?
* What is the expected gas price escalation over 15 years?
* Should we model a fixed gas price, indexed price, or a range?
* What gas supply infrastructure would be required?
* What pipeline/transport/compression costs should be considered?
* Is gas availability itself a reliability risk?
* What happens economically if gas supply is interrupted?
* Should we model gas composition and calorific value explicitly or use a standard MMBtu basis?

### Model outputs

[
Gas\ Consumption=f(MW,\ load,\ efficiency,\ gas\ quality)
]

and:

[
Gas\ Cost=Gas\ Consumption\times Gas\ Price
]

---

# 5. Checkpoint 7–10: Electricity value and operating margin

At $0.15/kWh:

[
10\text{ MWh}\rightarrow$1,500
]

We then considered:

* $1,500 electricity value
* $682 gas cost
* $200 avoided cooling electricity cost

giving a simplified:

[
$1,500-$682+$200
=\boxed{$1,018/hour}
]

This is **not project profit**. It is a simplified operating contribution before many costs.

### Questions for the Electrical Engineer

* What voltage level should the plant generate at?
* What step-up/down transformer configuration is required?
* What electrical losses should we assume?
* What auxiliary electrical consumption do the engines, pumps, controls, chillers, etc. require?
* What reserve margin should we maintain?
* What happens electrically when an engine trips?
* How quickly can another engine pick up the load?
* Do we need UPS/battery systems in addition to the gas generation?

### Model outputs

* Gross generation
* Auxiliary consumption
* Net generation
* Electrical losses
* Exported/delivered electricity
* Spinning/reserve capacity

---

# 6. Checkpoint 11: Availability

We used 8,000 operating hours instead of 8,760:

[
Availability=\frac{8,000}{8,760}
\approx91.3%
]

This introduces the idea that a real plant experiences:

* Planned maintenance
* Forced outages
* Derating
* Other downtime

### Questions for the Mechanical Engineer

* What planned maintenance schedule would these engines require?
* How many operating hours between major overhauls?
* How long does a typical maintenance outage last?
* What is realistic forced-outage availability?
* How does engine degradation affect efficiency over time?
* Should engine efficiency decline with age?
* What major components drive maintenance costs?

### Questions for the Electrical Engineer

* What electrical equipment creates additional planned/forced outage risk?
* Can engines be maintained individually while the remaining engines operate?
* What redundancy is required for transformers, switchgear and cooling systems?

### Model outputs

* Planned outage hours
* Forced outage rate
* Availability
* Degradation rate
* Maintenance schedule

---

# 7. Checkpoint 12–16: N+1 redundancy and reliability

We considered:

**5 × 3 MW engines = 15 MW installed**

For a 10 MW data-center load:

* 5 engines → 15 MW
* 4 engines → 12 MW
* 3 engines → 9 MW

Therefore losing one engine still allows the plant to meet the 10 MW load.

This is the basic N+1 concept.

With each engine having 95% availability:

[
P(success)
==========

0.95^5+
5(0.05)(0.95)^4
]

[
P(success)\approx97.74%
]

### Questions for the Electrical Engineer

* Is 5 × 3 MW actually a sensible configuration for a 10 MW critical load?
* Would fewer/larger engines be better?
* What N+1/N+2 architecture would you recommend?
* Should redundancy apply only to generation or also transformers, switchgear and cooling?
* What happens during an engine trip?
* How much spinning reserve should be maintained?
* What electrical protection and synchronization architecture is required?

### Questions for the Mechanical Engineer

* How independent are the engines mechanically?
* Are there common cooling/fuel systems that could create common-mode failures?
* Could one failure affect multiple engines?
* What redundancy is required in pumps, cooling systems and auxiliaries?

### Questions for the Petroleum Engineer

* Can gas supply interruption affect all engines simultaneously?
* What gas-storage or backup-fuel strategy is realistic?
* Should gas-supply reliability be modeled separately from engine reliability?

### Model outputs

* Number of engines
* Engine size
* N+1/N+2 configuration
* Forced outage probability
* Common-mode failure assumptions
* Probability of insufficient capacity
* Expected unserved load

---

# 8. Checkpoint 17–18: Expected revenue

If successful operation generates $1,500/hour:

[
E[Revenue]
==========

P(success)\times$1,500
]

[
=0.9774\times1,500
\approx$1,466
]

This introduces **probabilistic cash flow**.

However, plant failure does not necessarily mean customer outage if the data center can switch to the grid.

Therefore:

[
\boxed{Plant\ Failure\neq Customer\ Outage}
]

### Questions for the Electrical Engineer

* Is grid backup assumed?
* How quickly can the data center transfer to grid supply?
* Is there UPS/battery ride-through?
* What happens during simultaneous gas + grid failure?
* What reliability target should the system achieve?
* What percentage of annual load should realistically be served by the gas plant?

### Model outputs

* Probability of plant failure
* Probability of customer outage
* Expected unserved energy
* Grid backup energy
* Grid backup cost
* Reliability/availability metrics

---

# 9. Checkpoint 19–20: PPA revenue structure

We introduced a hypothetical PPA:

### Energy payment

[
$0.15/kWh
]

This is variable with electricity actually delivered.

### Capacity payment

[
$20,000/month
]

This can be relatively fixed if contractual availability requirements are satisfied.

Therefore:

[
Revenue =
Energy\ Revenue+
Capacity\ Revenue
]

The critical lesson:

[
\boxed{\text{Revenue is determined by both physics AND the contract}}
]

### Questions for the whole team

* What PPA structure makes sense for a dedicated data-center power plant?
* Should the customer pay for energy, capacity, or both?
* What availability guarantee should be offered?
* What penalties apply when the plant fails?
* Does grid backup allow us to maintain the customer's service commitment?
* Should the PPA include fuel-price pass-through?
* Should electricity pricing be fixed or indexed?
* How should inflation/escalation be handled?
* Is there a minimum-take commitment from the data center?

### Model outputs

* Energy tariff
* Capacity payment
* PPA escalation
* Availability requirement
* Outage penalties
* Contract duration
* Minimum-take assumptions
* Revenue formula

---

# 10. The questions I want us to answer before building the final model

Rather than everyone independently researching the entire problem, I think we should divide the technical assumptions.

## Petroleum Engineering

**Focus: Fuel system**

1. What gas composition/calorific value should we assume?
2. What delivered gas price is realistic?
3. What gas supply infrastructure is required?
4. What is realistic gas-price escalation?
5. What gas-supply reliability should we assume?
6. How does gas quality affect engine efficiency?
7. What backup-fuel/gas-storage strategy is realistic?

**Main model contribution:**

[
\boxed{Gas\ Price,\ Gas\ Quality,\ Gas\ Availability,\ Fuel\ Consumption}
]

---

## Mechanical Engineering

**Focus: Engines + thermodynamics + cooling**

1. What engine technology/configuration should we use?
2. What MW rating per engine?
3. What electrical efficiency/heat rate?
4. How does efficiency vary with load?
5. How much waste heat is recoverable?
6. What temperatures are available?
7. What absorption-chiller COP is realistic?
8. What maintenance schedule is required?
9. What engine degradation should we model?
10. What CAPEX and maintenance assumptions are reasonable?

**Main model contribution:**

[
\boxed{Efficiency,\ Heat,\ Cooling,\ Maintenance,\ Degradation}
]

---

## Electrical Engineering

**Focus: Power system + reliability**

1. What generation configuration should we use?
2. What N+1 architecture is appropriate?
3. What reserve margin is required?
4. What electrical losses should we assume?
5. What auxiliary loads should be included?
6. What grid connection/backup architecture is required?
7. What UPS/BESS capacity is appropriate?
8. What reliability/availability can we realistically achieve?
9. What happens during an engine trip?
10. What electrical CAPEX should be included?

**Main model contribution:**

[
\boxed{Dispatch,\ Reliability,\ Redundancy,\ Grid,\ Electrical\ CAPEX}
]

---

# 11. What I will handle on the modeling/finance side

Once the engineering assumptions are established, I can translate them into the techno-economic model:

[
\boxed{
Engineering\ Inputs
\rightarrow
Physical\ Simulation
\rightarrow
Annual\ Operating\ Profile
\rightarrow
Revenue/OPEX
\rightarrow
Project\ Cash\ Flow
\rightarrow
NPV/IRR
}
]

The financial model should ultimately answer:

* How much does the plant cost?
* How much gas does it consume?
* How much electricity does it actually deliver?
* How much cooling value does CHP create?
* What are annual revenues?
* What are annual OPEX costs?
* How does reliability affect revenue?
* What financing structure works?
* What is the project NPV?
* What is the IRR?
* What electricity/PPA price is required for viability?
* Which assumptions are the biggest risks?

## The principle I want us to follow

**Don't start by guessing financial numbers.**

First establish:

> **What does the physical plant actually do?**

Then:

> **How does it operate under different loads and failures?**

Then:

> **What does that operation cost and produce?**

Finally:

> **Does the resulting project make financial sense?**

That gives us a defensible techno-economic model rather than a spreadsheet built around arbitrary assumptions.
