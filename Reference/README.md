# Reference Experiment: Priority-Aware Lab Scheduling

This folder contains a **scoped, reproducible reference implementation**
derived from the full Dynamic Lab Scheduling project.

## Purpose

The goal of this reference experiment is to demonstrate one core insight:

> Under low system pressure, heuristic and learning-based scheduling
> policies behave similarly. Under tight capacity constraints,
> **problem formulation (state + reward design) matters more than
> model complexity**.

This implementation is intentionally **not a full hospital system**.
It isolates the intellectual core of the project so that results can be
understood, reproduced, and critiqued.

## What This Reference Includes
- A discrete-event laboratory scheduling environment
- Explicit STAT vs non-STAT priority handling
- Heuristic baselines (e.g., FIFO)
- A PPO-based learning agent
- Controlled high-load evaluation regime

## What This Reference Excludes (By Design)
- Time-varying arrival rates
- Multi-department resource coupling
- Attention or transformer architectures
- Extensive hyperparameter sweeps

These components are part of ongoing research and are deliberately
excluded here to maintain clarity and reproducibility.

## Reproducibility Goal

A single command should reproduce the main comparison
between a heuristic baseline and a learning-based policy
under a tight-capacity regime.

