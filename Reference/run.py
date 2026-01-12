"""
Entry point for the reference experiment.

This script runs:
1. Heuristic baselines (FIFO, STAT-first)
2. PPO agent training and evaluation

The goal is not peak performance, but to reproduce
the qualitative behavior discussed in the project:
- Baselines perform similarly under pressure
- PPO differentiates only under sustained congestion
"""

import yaml
import numpy as np

from env.lab_env import LabSchedulingEnv
from policies.fifo import FIFOPolicy
from policies.stat_first import StatFirstPolicy
from policies.random_policy import RandomPolicy
from rl.ppo_agent import PPOAgent
from rl.rollout_buffer import RolloutBuffer


# --------------------------------------------------
# Utility: run one episode
# --------------------------------------------------

def run_episode(env, policy, train=False, agent=None):
    obs, _ = env.reset()
    done = False
    total_reward = 0.0

    buffer = RolloutBuffer() if train else None

    while not done:
        if agent is not None:
            action, log_prob, value = agent.select_action(obs)
        else:
            action = policy.select_action(env)
            log_prob, value = None, None

        next_obs, reward, done, _, _ = env.step(action)
        total_reward += reward

        if train:
            buffer.add(obs, action, reward, log_prob, value)

        obs = next_obs

    return total_reward, buffer


# --------------------------------------------------
# Evaluation loop
# --------------------------------------------------

def evaluate_policy(env, policy, num_episodes):
    rewards = []
    for _ in range(num_episodes):
        ep_reward, _ = run_episode(env, policy)
        rewards.append(ep_reward)
    return np.mean(rewards), np.std(rewards)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    # Load configuration
    with open("configs/base.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    env_cfg = cfg["environment"]
    exp_cfg = cfg["experiment"]
    rl_cfg = cfg["rl_agent"]
    eval_cfg = cfg["evaluation"]

    # --------------------------------------------------
    # Environment
    # --------------------------------------------------
    env = LabSchedulingEnv(env_cfg)

    print("\n=== Reference Experiment ===")
    print(f"Machines: {env_cfg['num_machines']}")
    print("High-load, tight-deadline regime\n")

    # --------------------------------------------------
    # Baseline policies
    # --------------------------------------------------
    baselines = {
        "FIFO": FIFOPolicy(),
        "STAT-first": StatFirstPolicy(),
        "Random": RandomPolicy(seed=exp_cfg["seed"]),
    }

    print("Evaluating baselines...")
    for name, policy in baselines.items():
        mean_r, std_r = evaluate_policy(
            env, policy, exp_cfg["num_episodes_eval"]
        )
        print(f"{name:12s} | mean reward: {mean_r:8.2f} ± {std_r:6.2f}")

    # --------------------------------------------------
    # PPO Agent
    # --------------------------------------------------
    print("\nTraining PPO agent...")
    obs_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    agent = PPOAgent(
        obs_dim=obs_dim,
        action_dim=action_dim,
        learning_rate=rl_cfg["training"]["learning_rate"],
        gamma=rl_cfg["training"]["gamma"],
        clip_eps=rl_cfg["training"]["clip_range"],
        seed=exp_cfg["seed"],
    )

    # Training loop (episode-based)
    for episode in range(1, rl_cfg["training"]["total_timesteps"] + 1):
        ep_reward, buffer = run_episode(
            env, policy=None, train=True, agent=agent
        )
        agent.update_from_episode(buffer)

        # Lightweight progress logging
        if episode % 50 == 0:
            print(f"PPO episode {episode:4d} | reward {ep_reward:8.2f}")

    # --------------------------------------------------
    # PPO Evaluation
    # --------------------------------------------------
    print("\nEvaluating PPO agent...")
    ppo_rewards = []

    for _ in range(exp_cfg["num_episodes_eval"]):
        ep_reward, _ = run_episode(env, policy=None, agent=agent)
        ppo_rewards.append(ep_reward)

    print(
        f"PPO         | mean reward: {np.mean(ppo_rewards):8.2f} "
        f"± {np.std(ppo_rewards):6.2f}"
    )

    print("\nExperiment complete.")


if __name__ == "__main__":
    main()
