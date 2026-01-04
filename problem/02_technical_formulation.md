# Technical Formulation: Priority-Aware Scheduling as a Sequential Decision Problem

## Purpose of This Formulation
This document formalizes the laboratory scheduling problem at a level that enables:
- rigorous reasoning about decision quality and failure modes,
- controlled comparison between heuristic and learning-based approaches,
- translation of real operational constraints into a testable decision framework.

The goal is **not** to prescribe a specific implementation, but to make assumptions, trade-offs, and limitations explicit.

---

## Problem Overview
Laboratory scheduling is modeled as a **sequential decision-making problem** in which decisions are made repeatedly over time under uncertainty, priority constraints, and limited resources.

At each decision point, the system must decide how queued or arriving samples are assigned to available processing resources, balancing urgency, congestion, and downstream system effects.

This formulation allows us to reason not only about *what decisions are made*, but *when and why certain decisions lead to instability or failure*.

---

## Decision Process Abstraction
The problem is formulated as a **Markov Decision Process (MDP)** defined by:

- **States (S):** Observable summaries of laboratory operational status  
- **Actions (A):** Feasible scheduling or assignment decisions  
- **Transition Dynamics (P):** System evolution driven by arrivals, service completions, and assignments  
- **Rewards (R):** Scalar feedback encoding operational objectives and constraints  
- **Discount Factor (γ):** Trade-off between short-term urgency and long-term system stability  

This abstraction provides a common framework for evaluating both learned policies and classical scheduling rules under identical conditions.

---

## State Representation (High-Level)
The state representation captures information necessary for informed scheduling decisions, including:
- Queue lengths segmented by urgency class  
- Composition of urgent vs routine workload  
- Server availability and utilization  
- Temporal context reflecting demand patterns  

The design balances **informational sufficiency** with **tractability**:
- Too little information leads to unsafe or myopic decisions  
- Too much detail harms generalization and interpretability  

From an operational perspective, the state mirrors what a human scheduler implicitly reasons about when managing congestion.

---

## Action Space
Actions correspond to **assignment decisions** determining how samples are routed to available servers.

Operational constraints are enforced directly:
- Finite server capacity  
- Non-preemptive processing  
- Priority rules that restrict unsafe assignments  

By constraining the action space, the formulation ensures that all evaluated policies remain **operationally feasible**.

---

## Reward Structure (Conceptual)
The reward function encodes multiple, competing objectives:
- Incentives for meeting priority-specific SLA targets  
- Penalties for excessive waiting and tardiness  
- Implicit pressure to maintain throughput under congestion  

Rather than optimizing a single metric, the reward reflects the **multi-objective nature** of healthcare operations, where improvements in one dimension often degrade another.

From a product and governance perspective, this makes trade-offs explicit rather than hidden inside heuristics.

---

## Baseline Policies
To contextualize learning-based behavior, policies are benchmarked against classical heuristics, including:
- First-In-First-Out (FIFO)  
- Shortest Processing Time (SPT)  
- Earliest Due Date (EDD)  
- Priority-first variants  

These baselines serve as interpretable reference points for understanding:
- where learning-based policies improve upon standard practice,
- where they behave similarly,
- and where they fail in qualitatively different ways.

---

## Evaluation Logic (Conceptual)
Evaluation is structured to answer three questions:
1. **Does the policy meet critical priority guarantees?**
2. **How does behavior change under congestion and load shifts?**
3. **Are improvements stable or brittle across scenarios?**

This motivates evaluation beyond average rewards, focusing instead on:
- priority-specific outcomes,
- sensitivity to demand variation,
- and distributional behavior under stress.

---

## Constraints & Assumptions
The formulation explicitly incorporates:
- Fixed resource limits (servers, equipment)  
- Non-preemptive task execution  
- Priority constraints for urgent samples  

Key assumptions include:
- Fully observable simulated state  
- Stationary policy during evaluation windows  

These assumptions are chosen to enable controlled experimentation, while acknowledging that real-world deployments may violate them.

---

## Why a Sequential Decision Formulation Matters
Static optimization approaches struggle to capture:
- delayed effects of early scheduling decisions,  
- congestion cascades under peak load,  
- trade-offs between short-term urgency and long-term stability.  

Modeling the problem sequentially enables policies to reason over **temporal consequences**, making it possible to study not only performance, but **failure emergence over time**.

---

## Limitations of the Formulation
While expressive, this abstraction has limitations:
- Simulated dynamics cannot capture all real-world variability  
- Reward design introduces inductive bias  
- Observability assumptions may not hold in deployment  

Recognizing these limitations is essential for interpreting results responsibly and motivates stress testing and fallback strategies discussed elsewhere.

---

## Summary
This formulation provides a principled framework for studying priority-aware laboratory scheduling as a sequential decision problem. It makes explicit the assumptions, constraints, and trade-offs underlying both heuristic and learning-based approaches, enabling careful analysis of performance, robustness, and failure modes in safety-critical operational settings.
