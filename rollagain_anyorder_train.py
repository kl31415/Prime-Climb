import numpy as np
import random
import time

primes = {11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

# Custom reward functions
def prime_bonus(location, next_location, reward_type = "linear"):
    if location != next_location and next_location in primes:
        if reward_type == "linear":
            return 0.5
        elif reward_type == "nonlinear":
            return next_location / 100
    return 0

start = time.time()
Q = np.zeros((1011011, 16))
policy = np.zeros(1011011)

# HYPERPARAMETERS
eps = 10000
gamma = 1
lr = 0.1
reward_type = "linear"

for _ in range(eps):
    print(f"Episode {_ + 1}")
    with open("rollagain_anyorder_simulation.csv") as f:
        for index, line in enumerate(f):
            if index != 0:
                s, a, r, sp = map(int, line.strip().split(","))
                cur_loc = s // 10000
                next_loc = sp // 10000
                # Switch between linear and nonlinear bonus
                r += prime_bonus(cur_loc, next_loc)
                Q[s, a] = Q[s, a] + lr * (r + gamma * Q[sp, np.argmax(Q[sp])] - Q[s, a])
for i in range(1011011):
    if not np.any(Q[i]):
        policy[i] = random.randint(0, 15)
    else:
        policy[i] = np.argmax(Q[i])

print("Training complete. Time elapsed:", time.time() - start)

def save_policy(P, path):
    with open(path, "w") as f:
        for i, p in enumerate(P):
            f.write(str(int(p)))
            if i != P.size - 1:
                f.write("\n")

save_policy(policy, f"anyorder_eps={eps},gamma={gamma},lr={lr},reward_type={reward_type}.policy")
