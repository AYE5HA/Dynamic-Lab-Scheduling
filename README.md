# Dynamic Healthcare Lab Scheduling with Reinforcement Learning

## Overview
Many real-world operational systems must make sequential decisions under **priority constraints, limited capacity, and uncertainty**. Clinical laboratories are a representative example: delays directly affect patient outcomes, yet resources are finite and demand fluctuates over time.

This project studies whether **reinforcement learning (RL)** can learn *robust, priority-aware scheduling policies* for multi-server healthcare laboratories — and, critically, **when such policies fail despite strong aggregate performance metrics**.

Rather than optimizing headline numbers alone, this work emphasizes **evaluation rigor, stress testing, and failure analysis** to assess the *trustworthiness* of learned decision policies in safety-critical, constrained environments.

---

## Public Reference Scope
This repository contains a **scoped, reproducible reference implementation** that captures the *core ideas, trade-offs, and failure modes* explored in this project.

The public reference implementation is intentionally simplified to:
- isolate priority-aware scheduling dynamics
- expose learning behavior under tight capacity constraints
- make failure modes transparent and inspectable
- support reproducible experimentation without excessive complexity

More complex experimental variants explored during development
(e.g., additional state features, architectural extensions, or alternative formulations)
are **not included here by design**.

---

## Problem Context & Operational Impact
Hospital laboratories operate under competing objectives:
- Enforce strict SLA guarantees for STAT (urgent) samples  
- Minimize overall turnaround time and relative tardiness  
- Maintain throughput during congestion and demand spikes  
- Operate safely under staffing and equipment constraints  

In practice, these trade-offs are handled using heuristic scheduling rules
(e.g., FIFO, SPT, EDD, STAT-first). While interpretable and simple, such rules
struggle when **priority, congestion, and resource constraints interact dynamically**.

From an operational perspective, poor scheduling leads to:
- Delayed diagnostics for critical patients  
- Inefficient utilization of lab resources  
- Increased downstream bottlenecks across clinical workflows  

This project formulates lab scheduling as a **sequential decision-making problem**,
enabling systematic analysis of trade-offs between urgency, efficiency, and robustness.

---

## Technical Implementation Notes

**Tech Stack:**  
Python 3.9+, PyTorch, Gym-style environment API, NumPy, Pandas

**Learning Setup:**  
- RL Agent: Proximal Policy Optimization (PPO)  
- State Representation (scoped): queue length, urgency mix, machine availability  
- Action Space: discrete assignment decisions across available machines  

**Evaluation Approach:**  
- Comparison against classical heuristic baselines  
- Focus on behavior under sustained congestion rather than peak performance  
- Reporting of variability and failure cases, not just averages  

---

## System Design & Engineering Overview
At a high level, the system consists of:
- A **custom discrete-event simulation** modeling:
  - multi-server laboratory workflows  
  - STAT vs non-STAT priority handling  
  - stochastic arrivals and congestion  
- A **reinforcement learning agent** trained to make assignment decisions  
- A benchmarking layer comparing learned policies to heuristic baselines  

The system is designed to support:
- Controlled experimentation under constrained operating regimes  
- Stress testing without risk to real clinical operations  
- Transparent inspection of learning dynamics and failure modes  

> **Design note:**  
> This project intentionally does **not** pursue state-of-the-art performance
> or large-scale benchmarking. The focus is on understanding *system behavior
> under constraint and failure*, not on maximizing scores.

---

## Data, Modeling & Evaluation
The environment generates **fully observable, simulated operational data** representing:
- job arrivals with urgency labels  
- service times and machine availability  
- queue states and congestion dynamics  

Evaluation focuses on metrics aligned with real operational goals:
- priority-specific SLA compliance  
- relative tardiness and turnaround time  
- behavior under load and constraint shifts  

Rather than relying solely on average performance,
evaluation emphasizes **distributional behavior and stress scenarios**,
reflecting how failures manifest in real systems.

---

## Research Methodology & Failure Analysis
A central finding of this work is that **stable training metrics can mask brittle decision policies**.

During development, the RL agent exhibited **slow learning, representation collapse,
and degraded decision quality** under tighter or shifted constraints,
even when aggregate validation metrics appeared stable.

These observations motivated deeper investigation into:
- how evaluation design can induce systematic overconfidence  
- why average metrics are insufficient in priority-aware systems  
- how stress testing reveals failure modes invisible to standard benchmarks  

A detailed discussion of these behaviors and limitations is provided in `failures.md`.

---

## Reproducibility & Transparency
This repository documents:
- the problem formulation and modeling assumptions  
- the structure of the simulation environment  
- the learning setup and evaluation protocol  
- observed behaviors, limitations, and open questions  

The goal is to support **transparent reasoning and reproducible analysis in principle**,
while maintaining a clear and honest project scope.

---

## Potential Business Impact & Product Considerations
If deployed, simulation-based estimates suggest potential to:
- reduce STAT turnaround time during peak operating periods  
- improve resource utilization under congestion  
- support more predictable laboratory operations  

**Conceptual product considerations:**
- integration with existing hospital information systems (HIS/LIS)  
- incremental rollout (simulation → shadow mode → pilot)  
- governance mechanisms for safety, override, and monitoring  

---

## Status
📌 **Research reference artifact — current scope complete**

This repository is considered complete for its intended reference scope.
Future work would build on these insights rather than extend this implementation directly.

---

## Contact
For academic or professional discussion related to this work,
feel free to reach out via email or LinkedIn.
