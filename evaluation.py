from utils import roll_dice, apply_operations

def evaluate_policy(agent, num_games=100):
    wins = 0
    moves_per_game = []
    
    for game in range(num_games):
        state = agent.mdp.reset()  # Reset MDP state at the start of each game
        moves = 0
        
        while state != 101 and moves < 100:  # Limit the number of moves to prevent infinite games
            moves += 1
            dice1, dice2, is_double = roll_dice()  # Get dice rolls
            
            # Apply the first die roll
            possible_moves1 = apply_operations(state, dice1, 4 if is_double else 2)
            
            # Choose an action for the first die roll
            action1 = agent.choose_action(state, possible_moves1)  # Pass possible moves for the first die
            
            # Get the next state and reward based on the action
            next_state, reward, done = agent.mdp.step(action1)
            state = next_state
            
            if done:
                wins += 1  # Increment win count if done
                break
            
            # If it's not a double, apply the second die roll
            if not is_double:
                possible_moves2 = apply_operations(state, dice2, 2)
                action2 = agent.choose_action(state, possible_moves2)  # Pass possible moves for the second die
                next_state, reward, done = agent.mdp.step(action2)
                state = next_state
            
            if done:
                wins += 1  # Increment win count if done
                break
        
        if state == 101:  # Only record moves for winning games
            moves_per_game.append(moves)
    
    avg_moves = sum(moves_per_game) / len(moves_per_game) if moves_per_game else float('inf')
    win_rate = wins / num_games  # Calculate win rate
    
    return {
        'win_rate': win_rate,
        'average_moves': avg_moves,
        'total_games': num_games,
        'wins': wins
    }
