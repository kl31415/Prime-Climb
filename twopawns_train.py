import numpy as np
import random
import time

# Sparse Q-table as a dictionary of dictionaries
Q = {}
policy = {}

# State encoding
def encode_state(p1, p2, d1, d2):
    return p1 * 10000000 + p2 * 10000 + d1 * 100 + d2 + 1

# HYPERPARAMETERS
eps = 1000
gamma = 1  # Keep gamma at 1 as specified
lr = 0.1

start = time.time()

# Training loop
for _ in range(eps):
    print(_)
    with open("prime_climb_twopawns_simulation.csv") as f:
        for index, line in enumerate(f):
            if index != 0:
                s, a, r, sp = map(int, line.strip().split(","))
                
                # Ensure states exist in Q
                if s not in Q:
                    Q[s] = {}
                if a not in Q[s]:
                    Q[s][a] = 0

                # Ensure next state exists in Q
                if sp not in Q:
                    Q[sp] = {}

                # Get max Q-value for next state
                max_q_sp = max(Q[sp].values(), default=0)

                # Update Q-value
                Q[s][a] += lr * (r + gamma * max_q_sp - Q[s][a])

# Derive policy
for s in Q:
    if Q[s]:
        policy[s] = max(Q[s], key=Q[s].get)
    else:
        policy[s] = random.randint(0, 47)

# Fill in missing states with random policy
for p1 in range(101):
    for p2 in range(101):
        for d1 in range(1, 11):
            for d2 in range(1, 11):
                s = encode_state(p1, p2, d1, d2)
                if s not in policy:
                    policy[s] = random.randint(0, 47)

print("Training complete. Time elapsed:", time.time() - start)

# Save policy
def save_policy(policy, path):
    with open(path, "w") as f:
        for s in sorted(policy.keys()):
            f.write(f"{s},{policy[s]}\n")

save_policy(policy, f"twopawns_eps={eps},gamma={gamma},lr={lr}.policy")
