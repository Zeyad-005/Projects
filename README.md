# 🧭 Welcome to "Reinforcement Learning - Grid World Navigation" Project (Value Iteration)

## Overview
This project addresses a reinforcement learning problem using a 5×5 stochastic grid world. The goal is to implement value iteration from scratch to find optimal policies under different reward configurations and analyze how reward structures influence agent behavior.

## Objectives
- **Environment Modeling**: Implement the 5×5 grid world with stochastic transitions
- **Value Iteration Algorithm**: Implement value iteration from scratch for discounted rewards
- **Policy Extraction**: Derive optimal policies from computed value functions
- **Reward Sensitivity Analysis**: Test four different reward configurations
- **Policy Explanation**: Provide intuitive explanations for resulting policies
- **Bonus Implementation**: Implement policy iteration with random initial policies

## Environment Details
- **Grid Size**: 5×5 world
- **Actions**: Up, Down, Left, Right
- **Transition Model**: 70% intended action, 10% each other direction
- **Wall Collisions**: No movement when hitting boundaries
- **Reward Configurations**:
  1. R1 = 100, R2 = 110
  2. R1 = 10, R2 = 100
  3. R1 = 1, R2 = 10
  4. R1 = 10, R2 = 15
- **Discount Factor**: γ = 0.95

## Key Steps
1. Environment Implementation with Stochastic Transitions
2. Value Iteration Algorithm Implementation
3. Convergence Testing with Different Reward Configurations
4. Policy Extraction from Value Functions
5. Visualization of Value Functions and Policies
6. Intuitive Analysis of Policy Differences
7. Bonus: Policy Iteration Implementation

## Implementation Requirements
- ✅ Implement value iteration from scratch
- ✅ Handle stochastic transitions correctly
- ✅ Test all four reward configurations
- ✅ Extract and display optimal policies
- ✅ Provide intuitive explanations for policy differences
- ✅ Bonus: Implement policy iteration with random initialization
