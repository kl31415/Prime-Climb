import matplotlib.pyplot as plt

def plot_training_rewards(rewards, title="Training Rewards over Episodes"):
    plt.figure(figsize=(10, 6))
    plt.plot(rewards, label="Episode Rewards")
    plt.xlabel("Episodes")
    plt.ylabel("Total Reward")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

def plot_path_to_goal(positions, title="Path to Goal"):
    plt.figure(figsize=(10, 6))
    plt.plot(positions, label="Position")
    plt.xlabel("Moves")
    plt.ylabel("Position on Board")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()
