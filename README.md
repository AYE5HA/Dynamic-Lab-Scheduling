# Dynamic Healthcare Lab Scheduling with Reinforcement Learning

## Overview
Many real-world operational systems must make sequential decisions under **priority constraints, limited capacity, and uncertainty**. Clinical laboratories are a representative example: delays directly affect patient outcomes, yet resources are finite, and demand fluctuates over time.

This project studies whether **reinforcement learning (RL)** can learn *robust, priority-aware scheduling policies* for multi-server healthcare laboratories — and, critically, **when such policies fail despite strong aggregate performance metrics**.

Rather than optimizing headline numbers alone, this work emphasizes **evaluation rigor, stress testing, and failure analysis** to assess the *trustworthiness* of learned decision policies in safety-critical, constrained environments.

---

## Problem Context & Operational Impact
Hospital laboratories operate under competing objectives:
- Enforce strict SLA guarantees for STAT (urgent) samples  
- Minimize overall turnaround time and relative tardiness  
- Maintain throughput during congestion and demand spikes  
- Operate safely under staffing and equipment constraints  

In practice, these trade-offs are handled using heuristic scheduling rules (FIFO, SPT, EDD, STAT-first). While interpretable and simple, such rules struggle when **priority, congestion, and resource constraints interact dynamically**.

From an operational perspective, poor scheduling leads to:
- Delayed diagnostics for critical patients  
- Inefficient utilization of lab resources  
- Increased downstream bottlenecks across clinical workflows  

This project formulates lab scheduling as a **sequential decision-making problem**, enabling systematic analysis of trade-offs between urgency, efficiency, and robustness.

---
## Technical Implementation Notes

**Tech Stack:** Python 3.9+, PyTorch, OpenAI Gym-style API, NumPy, Pandas, Matplotlib for visualization

**Model Architecture:** 
- RL Agent: PPO (Proximal Policy Optimization) with custom reward shaping
- State Representation: [Queue lengths, urgency mix, server utilization, time of day]
- Action Space: Discrete assignment decisions across available servers

-**Evaluation Framework:**
- Evaluation across multiple simulated demand regimes and load profiles
- Statistical comparison against heuristic baselines to assess performance consistency

  
## System Design & Engineering Overview
At a high level, the system consists of:
- A **custom discrete-event simulation** modeling:
  - Multi-server laboratory workflows  
  - STAT vs non-STAT priority handling  
  - Time-varying arrivals and congestion  
- A **reinforcement learning agent** trained to make scheduling decisions under these constraints  
- A benchmarking layer comparing learned policies against classical heuristics  

The system is designed to support:
- Controlled experimentation under varying load and constraint regimes  
- Stress testing without risking real clinical operations  
- Reproducible evaluation across policy variants and baselines  

> **Implementation note:**  
> Core environment and agent implementations are intentionally not open-sourced due to ongoing research and publication plans. This repository documents system design decisions, evaluation methodology, and observed behaviors rather than raw implementation code.

---

## Data, Modeling & Evaluation
The environment generates **fully observable, simulated operational data** representing:
- Job arrivals with urgency labels  
- Service times and server availability  
- Queue states and congestion dynamics  

Evaluation focuses on metrics aligned with real operational goals, including:
- Priority-specific SLA compliance  
- Relative tardiness and turnaround time  
- System behavior under congestion and constraint shifts  

Rather than relying solely on average performance, evaluation emphasizes **distributional behavior** and **stress scenarios**, reflecting how failures manifest in real systems.


## Engineering Considerations

While core implementations remain private, the system was designed with:
- Modular architecture separating environment, agent, and evaluation components
- Reproducible experiment tracking via configuration files and seed management
- Performance optimization to support large-scale simulation and repeated stress testing

**For Production Deployment (Conceptual):**
- Would require containerization and API-based integration
- Alignment with existing hospital information system standards
- Monitoring and governance mechanisms for model performance and drift

---

## Research Methodology & Failure Analysis
A central finding of this work is that **stable training metrics can mask brittle decision policies**.

During development, the RL agent exhibited **representation collapse and degraded decision quality** under tighter or shifted constraints, even when standard validation metrics appeared stable. These failures highlighted limitations in naïve evaluation protocols.

This motivated deeper investigation into:
- How evaluation design can induce systematic overconfidence  
- Why average metrics are insufficient in constrained, priority-aware systems  
- How stress testing reveals failure modes invisible to standard benchmarks  

These insights directly informed subsequent work on robustness analysis and evaluation tooling.

A detailed discussion is provided in `failures.md`.

---

## Reproducibility & Transparency
While implementation details remain private, this repository documents:
- The problem formulation and modeling assumptions  
- Evaluation protocols and stress-testing principles  
- Observed behaviors, limitations, and open research questions  

The intent is to support **transparent reasoning and reproducible analysis in principle**, while preserving intellectual property during active research and publication.

---

## Status
🚧 **Active research project**

Planned additions include:
- Detailed evaluation protocols  
- Stress-testing methodology  
- Aggregated result summaries  
- Diagnostic insights and research artifacts  

---
## Potential Business Impact & Product Considerations

If deployed, simulation-based estimates suggest potential to:
- Reduce STAT turnaround time by approximately 15–25% during peak operating periods
- Decrease lab operational costs through better resource utilization
- Improve patient outcomes through faster critical diagnostics

**Product Considerations:**
- Integration with existing Hospital Information Systems (HIS/LIS)
- Incremental rollout strategy: simulation → shadow mode → pilot → full deployment
- Key stakeholders: lab directors, hospital administrators, IT security teams, clinical staff


## Contact
For academic or professional discussion related to this work, feel free to reach out via email or LinkedIn.
