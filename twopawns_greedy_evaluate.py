import random
import matplotlib.pyplot as plt

# Define operators and their mapping to numbers
operators = ['+', '-', '*', '/']
operator_mapping = {
    0: ('+', '+'), 1: ('+', '-'), 2: ('+', '*'), 3: ('+', '/'),
    4: ('-', '+'), 5: ('-', '-'), 6: ('-', '*'), 7: ('-', '/'),
    8: ('*', '+'), 9: ('*', '-'), 10: ('*', '*'), 11: ('*', '/'),
    12: ('/', '+'), 13: ('/', '-'), 14: ('/', '*'), 15: ('/', '/')
}

def apply_operator(location, dice_value, operator):
    """
    Apply an operator to a location with bounds and division checks.
    
    Args:
        location (int): Current pawn location
        dice_value (int): Value of the dice roll
        operator (str): Operator to apply (+, -, *, /)
    
    Returns:
        int or None: New location or None if move is invalid
    """
    try:
        if operator == '+':
            result = location + dice_value
        elif operator == '-':
            result = location - dice_value
        elif operator == '*':
            result = location * dice_value
        elif operator == '/':
            # Ensure division is exact
            if location % dice_value == 0:
                result = location // dice_value
            else:
                return None

        # Check bounds
        if 0 <= result <= 101:
            return result
        return None
    except:
        return None

def find_best_move(current_location, d1, d2):
    """
    Find the best move for a single pawn that maximizes progress.
    
    Args:
        current_location (int): Current pawn location
        dice1 (int): First dice roll
        dice2 (int): Second dice roll
    
    Returns:
        tuple: (best_location, operation_details)
    """
    best_location = -1
    
    # Try all 16 possible operator combinations
    for action_number in range(16):
        op1, op2 = operator_mapping[action_number]
        
        # Try first dice with first operator
        new_loc1 = apply_operator(current_location, d1, op1)
        if (new_loc1 == 101):
            return 101, True
        if new_loc1 is not None:
            # Try second dice with second operator
            new_loc = apply_operator(new_loc1, d2, op2)
            
            # Update best location if this move is better
            if new_loc is not None:
                # Prioritize moves that get closer to 101
                if new_loc > best_location:
                    best_location = new_loc
    
    return best_location, False

def two_pawn_greedy_evaluation(num_simulations=100000):
    """
    Simulate the two-pawn greedy strategy for Prime Climb.
    
    Args:
        num_simulations (int): Number of game simulations to run
    
    Returns:
        tuple: (list of turn counts, number of errors)
    """
    results = []
    errors = 0

    for _ in range(num_simulations):
        pawn1_location = 0
        pawn2_location = 0
        turns = 0
        
        # Continue the game until both pawns reach 101
        while pawn1_location != 101 or pawn2_location != 101:
            # Roll two dice
            dice1 = random.randint(1, 10)
            dice2 = random.randint(1, 10)
            
            # Check if applying dice rolls to either pawn can make them reach 101
            if pawn1_location != 101 and pawn2_location != 101:
                # Neither pawn is at 101
                pawn1_new, pawn1_oneroll = find_best_move(pawn1_location, dice1, dice2)
                pawn1_new_rev, pawn1_oneroll_rev = find_best_move(pawn1_location, dice2, dice1)
                pawn2_new, pawn2_oneroll = find_best_move(pawn2_location, dice1, dice2)
                pawn2_new_rev, pawn2_oneroll_rev = find_best_move(pawn2_location, dice2, dice1)
                
                # Check if either pawn can reach 101
                if (pawn1_new == 101) or (pawn2_new == 101):
                    # Apply rolls to the pawn that can reach 101
                    if pawn1_new == 101:
                        pawn1_location = pawn1_new
                        if pawn1_oneroll:
                            pawn2_location = find_best_move(pawn2_location, dice2, 0)[0]
                    else:
                        pawn2_location = pawn2_new
                        if pawn2_oneroll:
                            pawn1_location = find_best_move(pawn1_location, dice2, 0)[0]

                elif (pawn1_new_rev == 101) or (pawn2_new_rev == 101):
                    if pawn1_new_rev == 101:
                        pawn1_location = pawn1_new_rev
                        if pawn1_oneroll_rev:
                            pawn2_location = find_best_move(pawn2_location, dice1, 0)[0]
                    else:
                        pawn2_location = pawn2_new_rev
                        if pawn2_oneroll_rev:
                            pawn1_location = find_best_move(pawn1_location, dice1, 0)[0]

                else:
                    # Neither pawn can reach 101, proceed as normal
                    pawn1_total = pawn1_new + pawn2_location
                    pawn1_total_rev = pawn1_new_rev + pawn2_location
                    pawn2_total = pawn1_location + pawn2_new
                    pawn2_total_rev = pawn1_location + pawn2_new_rev
                    pawn1_split1_new = find_best_move(pawn1_location, dice1, 0)[0]
                    pawn1_split2_new = find_best_move(pawn1_location, dice2, 0)[0]
                    pawn2_split1_new = find_best_move(pawn2_location, dice2, 0)[0]
                    pawn2_split2_new = find_best_move(pawn2_location, dice1, 0)[0]
                    pawnsplit_total = pawn1_split1_new + pawn2_split1_new
                    pawnsplit_total_rev = pawn1_split2_new + pawn2_split2_new
                    best_total = max(pawn1_total, pawn2_total, pawn1_total_rev, pawn2_total_rev, pawnsplit_total, pawnsplit_total_rev)
                    
                    if best_total == pawn1_total:
                        pawn1_location = pawn1_new
                    elif best_total == pawn2_total:
                        pawn2_location = pawn2_new
                    elif best_total == pawn1_total_rev:
                        pawn1_location = pawn1_new_rev
                    elif best_total == pawn2_total_rev:
                        pawn2_location = pawn2_new_rev
                    elif best_total == pawnsplit_total:
                        pawn1_location = pawn1_split1_new
                        pawn2_location = pawn2_split1_new
                    elif best_total == pawnsplit_total_rev:
                        pawn1_location = pawn1_split2_new
                        pawn2_location = pawn2_split2_new

            elif pawn1_location == 101 and pawn2_location != 101:
                # Pawn 1 is at 101, apply both rolls to pawn 2
                pawn2_new = find_best_move(pawn2_location, dice1, dice2)[0]
                pawn2_new_rev = find_best_move(pawn2_location, dice2, dice1)[0]
                pawn2_location = max(pawn2_new, pawn2_new_rev)
            elif pawn2_location == 101 and pawn1_location != 101:
                # Pawn 2 is at 101, apply both rolls to pawn 1
                pawn1_new = find_best_move(pawn1_location, dice1, dice2)[0]
                pawn1_new_rev = find_best_move(pawn1_location, dice2, dice1)[0]
                pawn1_location = max(pawn1_new, pawn1_new_rev)
            else:
                # Both pawns are at 101, do nothing
                pass

            turns += 1

        results.append(turns)
    
    return results, errors

# Function to plot convergence or error rate
def plot_convergence(results, errors):
    # Plot histogram of results (number of turns to reach 101)
    plt.figure(figsize=(12, 6))
    plt.hist(results, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title("Histogram of Turns to Reach Goal State (101) - Greedy Approach, Two Pawns")
    plt.xlabel("Number of Turns")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Plot error rate over simulations
    total_simulations = len(results) + errors
    error_rate = errors / total_simulations
    plt.figure(figsize=(12, 6))
    plt.bar(["Errors", "Successes"], [errors, len(results)], color=["red", "green"])
    plt.title("Error Rate vs. Successful Simulations - Greedy Approach, Two Pawns")
    plt.ylabel("Count")
    plt.text(0, errors / 2, f"Error Rate: {error_rate:.2%}", ha="center", va="center", fontsize=12, color="white")
    plt.grid(axis='y')
    plt.show()

# Simulate the game
if __name__ == "__main__":
    results, errors = two_pawn_greedy_evaluation()
    print("Average turns for both pawns to reach 101:", sum(results) / len(results))
    plot_convergence(results, errors)
