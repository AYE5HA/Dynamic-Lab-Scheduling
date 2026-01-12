# ==========================================================
# Reference Configuration: Priority-Aware Lab Scheduling
# ==========================================================
# This configuration defines a single controlled experiment
# used to study scheduling behavior under capacity pressure.
# ==========================================================

experiment:
  name: "tight_capacity_priority_reference"
  seed: 42
  episode_length: 500
  num_episodes_eval: 25

# ----------------------------------------------------------
# Environment Definition
# ----------------------------------------------------------
environment:
  description: >
    Single-stage laboratory scheduling environment with
    explicit STAT vs non-STAT priorities and limited capacity.
    Designed to induce congestion and deadline pressure.

  num_machines: 2            # intentionally tight capacity
  arrival_process:
    type: "poisson"
    rate: 0.9                # high load to induce pressure

  job_types:
    stat:
      fraction: 0.2
      service_time_mean: 10
      deadline: 15
      priority_weight: 5.0
    routine:
      fraction: 0.8
      service_time_mean: 10
      deadline: 40
      priority_weight: 1.0

# ----------------------------------------------------------
# State Representation (Explicitly Scoped)
# ----------------------------------------------------------
state_representation:
  features:
    - queue_length
    - stat_fraction_in_queue
    - free_machine_count
  notes: >
    Reduced state chosen to isolate the effect of
    priority encoding rather than state complexity.

# ----------------------------------------------------------
# Reward Definition
# ----------------------------------------------------------
reward:
  type: "tardiness_penalty"
  formulation: >
    Negative reward proportional to job tardiness.
    STAT jobs incur a higher penalty multiplier.
  normalize: false

# ----------------------------------------------------------
# Baseline Policies
# ----------------------------------------------------------
baselines:
  - name: "FIFO"
    description: "First-in-first-out scheduling"

# ----------------------------------------------------------
# RL Agent Configuration
# ----------------------------------------------------------
rl_agent:
  algorithm: "PPO"
  network:
    type: "MLP"
    hidden_layers: [64, 64]
    activation: "relu"

  training:
    total_timesteps: 200000
    gamma: 0.99
    learning_rate: 3.0e-4
    clip_range: 0.2

  notes: >
    Hyperparameters chosen for stability rather than
    optimality. No extensive tuning performed.

# ----------------------------------------------------------
# Evaluation Protocol
# ----------------------------------------------------------
evaluation:
  comparison_metric: "average_episode_reward"
  report:
    include_variance: true
    include_failure_cases: true

  notes: >
    Evaluation focuses on behavior under sustained
    congestion rather than peak performance alone.
