import numpy as np
from utils import roll_dice, apply_operations
from tqdm import tqdm
from visualization import plot_training_rewards

class QLearningAgent:
    def __init__(self, mdp, alpha=0.1, gamma=0.9, epsilon=0.1, episodes=1000):
        self.mdp = mdp
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate (epsilon-greedy)
        self.episodes = episodes
        self.q_table = {}  # Q-table to store state-action values
    
    def initialize_q_table(self):
        """Initialize Q-table with zeros for all states and actions."""
        # We have 101 possible states (0 to 100), and 100 possible dice roll actions (1,1) to (10,10)
        for state in range(0, 101):  # States are from 0 to 100
            self.q_table[state] = {(i, j): 0 for i in range(1, 11) for j in range(1, 11)}  # Actions: (1,1) to (10,10)

    def choose_action(self, state, possible_moves):
        """Choose an action using epsilon-greedy policy based on possible moves."""
        if np.random.rand() < self.epsilon:
            # Explore: Choose a random action from possible moves
            return np.random.choice(possible_moves)
        else:
            # Exploit: Choose the action with the highest Q-value among possible moves
            q_values = {move: self.q_table[state].get(move, 0) for move in possible_moves}
            return max(q_values, key=q_values.get)

    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value using the Q-learning update rule."""
        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
        self.q_table[state][action] += self.alpha * (reward + self.gamma * self.q_table[next_state][best_next_action] - self.q_table[state][action])

def train_agent(agent):
    episode_rewards = []
    progress_bar = tqdm(range(agent.episodes), desc="Training")
    
    for episode in progress_bar:
        state = agent.mdp.reset()  # Start at the initial state
        total_reward = 0
        done = False
        
        while not done:
            dice1, dice2, is_double = roll_dice()
            
            # Determine the possible moves based on the dice roll
            possible_moves1 = apply_operations(state, dice1, 4 if is_double else 2)
            if possible_moves1:
                action1 = agent.choose_action(state, possible_moves1)
                next_state, reward, done = agent.mdp.step(action1)
                agent.update_q_value(state, action1, reward, next_state)
                total_reward += reward
                state = next_state
            
            if done:
                break
                
            # Second die (if not doubles)
            if not is_double:
                possible_moves2 = apply_operations(state, dice2, 2)
                if possible_moves2:
                    action2 = agent.choose_action(state, possible_moves2)
                    next_state, reward, done = agent.mdp.step(action2)
                    agent.update_q_value(state, action2, reward, next_state)
                    total_reward += reward
                    state = next_state
        
        episode_rewards.append(total_reward)
        progress_bar.set_postfix({'reward': total_reward})
    
    return episode_rewards