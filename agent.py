import numpy as np
import json
from utils import get_all_possible_transitions
from collections import defaultdict

class QLearningAgent:
    def __init__(self, mdp, learning_rate=0.1, discount_factor=0.95, epsilon=0.1, episodes=10000):
        self.mdp = mdp
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.episodes = episodes
        self.transitions = get_all_possible_transitions()
        
        # Initialize Q-values only for valid transitions
        self.q_values = defaultdict(lambda: defaultdict(float))
        for state in self.transitions:
            for next_state in self.transitions[state]:
                self.q_values[state][next_state] = 0.0
                
        print(f"Initialized Q-table with {sum(len(moves) for moves in self.transitions.values())} valid transitions")
    
    def choose_action(self, state, possible_moves):
        if not possible_moves:
            # If there are no possible moves, return state as a fallback or a default action
            return state
        
        # Epsilon-greedy strategy: explore with probability epsilon, otherwise exploit
        if np.random.random() < self.epsilon:
            # Randomly choose a move from possible moves
            return np.random.choice(list(possible_moves))
        
        # Get Q-values for each possible move, handling the case where state might not exist in q_values
        valid_moves = {}
        for move in possible_moves:
            # If state is not in q_values, initialize its dictionary
            if state not in self.q_values:
                self.q_values[state] = {}
            
            # If move is not in q_values[state], initialize its Q-value
            if move not in self.q_values[state]:
                self.q_values[state][move] = 0  # Default Q-value for uninitialized moves
            
            valid_moves[move] = self.q_values[state][move]
        
        # Choose the action with the highest Q-value
        return max(valid_moves.items(), key=lambda x: x[1])[0]
    
    def update_q_value(self, state, next_state, reward, done):
        if not self.transitions[next_state] and not done:
            return  # No update if no valid transitions from next state
            
        best_future_value = max(self.q_values[next_state].values()) if not done else 0
        current_q = self.q_values[state][next_state]
        self.q_values[state][next_state] += self.learning_rate * (
            reward + self.discount_factor * best_future_value - current_q
        )
    
    def save_policy(self, filename="policy.json"):
        policy = {
            str(state): min(state_values, key=state_values.get)  # Store the best action/next state
            for state, state_values in self.q_values.items()
        }
        with open(filename, 'w') as f:
            json.dump(policy, f)
        print(f"Policy saved to {filename}")
    
    def load_policy(self, filename="policy.json"):
        try:
            with open(filename, 'r') as f:
                policy_dict = json.load(f)
                # Convert the policy dictionary back to integers
                return {int(state): int(next_state) for state, next_state in policy_dict.items()}
        except FileNotFoundError:
            print("No policy file found")
            return defaultdict(lambda: defaultdict(float))
