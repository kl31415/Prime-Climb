import csv
import random

# Define operators and map each pair to a unique number between 0 and 15
operators = ['+', '-', '*', '/']
operator_mapping = {
    ('+', '+'): 0, ('+', '-'): 1, ('+', '*'): 2, ('+', '/'): 3,
    ('-', '+'): 4, ('-', '-'): 5, ('-', '*'): 6, ('-', '/'): 7,
    ('*', '+'): 8, ('*', '-'): 9, ('*', '*'): 10, ('*', '/'): 11,
    ('/', '+'): 12, ('/', '-'): 13, ('/', '*'): 14, ('/', '/'): 15
}

def apply_operator(location, dice_value, operator):
    """Applies a single operator to a location and dice value."""
    try:
        if operator == '+':
            result = location + dice_value
        elif operator == '-':
            result = location - dice_value
        elif operator == '*':
            result = location * dice_value
        elif operator == '/' and dice_value != 0 and location % dice_value == 0:
            result = location // dice_value
        else:
            return None

        # Ensure result is within bounds
        return result if 0 <= result <= 101 else None
    except:
        return None

def generate_data_one_pawn(num_samples=1000000):
    """Generate simulation data for one-pawn Prime Climb considering dice in any order."""
    data = []
    location = 0  # Starting location

    for _ in range(num_samples):
        dice1 = random.randint(1, 10)
        dice2 = random.randint(1, 10)
        state = location * 10000 + (dice1 * 10 + dice2)

        best_action = None
        best_location = None
        best_reward = float('-inf')

        # Consider both dice orders
        dice_orders = [(dice1, dice2), (dice2, dice1)]
        for d1, d2 in dice_orders:
            for op1 in operators:
                loc1 = apply_operator(location, d1, op1)
                if loc1 is None:
                    continue

                for op2 in operators:
                    loc2 = apply_operator(loc1, d2, op2)
                    if loc2 is None:
                        continue

                    # Determine reward
                    reward = 100 if loc2 == 101 else -1
                    if reward > best_reward:  # Prioritize better rewards
                        best_action = operator_mapping[(op1, op2)]
                        best_location = loc2
                        best_reward = reward

        if best_action is None:  # Skip invalid actions
            continue

        # Next state with new dice roll
        next_dice1, next_dice2 = random.randint(1, 10), random.randint(1, 10)
        next_state = best_location * 10000 + (next_dice1 * 10 + next_dice2)

        # Append data
        data.append([state, best_action, best_reward, next_state])

        # Update location
        location = 0 if best_location == 101 else best_location

    return data

# Generate and save to CSV
output_path = 'rollagain_anyorder_simulation.csv'
data = generate_data_one_pawn()

with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['s', 'a', 'r', 'sp'])
    writer.writerows(data)

print(f"Simulation data saved to {output_path}")
