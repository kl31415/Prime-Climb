import numpy as np
import random
import time

start = time.time()
gamma = 1
Q = np.zeros((1011011, 16))
policy = np.zeros(1011011)
for _ in range(1000):
    print(_)
    with open("prime_climb_simulation.csv") as f:
        for index, line in enumerate(f):
            if index != 0:
                s, a, r, sp = map(int, line.strip().split(","))
                Q[s, a] = Q[s, a] + 0.3 * (r + gamma * Q[sp, np.argmax(Q[sp])] - Q[s, a])
for i in range(1011011):
    if not np.any(Q[i]):
        policy[i] = random.randint(0, 15)
    else:
        policy[i] = np.argmax(Q[i])
print("time:", time.time() - start)

def save_policy(P, path):
    with open(path, "w") as f:
        for i, p in enumerate(P):
            f.write(str(int(p)))
            if i != P.size - 1:
                f.write("\n")

save_policy(policy, "prime_climb.policy")