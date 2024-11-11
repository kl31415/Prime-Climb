import os
from mdp import PrimeClimbMDP
from agent import QLearningAgent
from train import train_agent
from evaluation import evaluate_policy

def main():
    # Initialize MDP and Agent
    mdp = PrimeClimbMDP()
    agent = QLearningAgent(mdp)
    
    # Check if the policy already exists
    policy_filename = "policy.json"
    
    if os.path.exists(policy_filename):
        # Load the existing policy if it exists
        print(f"Loading existing policy from {policy_filename}...")
        policy = agent.load_policy(filename=policy_filename)
    else:
        # Train the agent if no policy exists
        print("Training agent...")
        train_agent(agent)
        
        # Save the trained policy
        print(f"Saving trained policy to {policy_filename}...")
        agent.save_policy(filename=policy_filename)
        
        # Load the newly saved policy
        policy = agent.load_policy(filename=policy_filename)
    
    # Evaluate the policy
    print("\nEvaluating policy...")
    results = evaluate_policy(agent, num_games=100)
    
    # Print results
    print(f"\nEvaluation Results:")
    print(f"Win Rate: {results['win_rate']:.2%}")
    print(f"Average Moves per Win: {results['average_moves']:.1f}")
    print(f"Total Games: {results['total_games']}")
    print(f"Total Wins: {results['wins']}")

if __name__ == "__main__":
    main()
