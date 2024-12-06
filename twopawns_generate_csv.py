import random

def apply_operator(location, dice_value, operator):
    """
    Applies an operation to a location and dice value.
    Ensures the result is within bounds and follows game rules.
    """
    if location == 101:  # Already at goal
        return location

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
            return None  # Invalid operation

        # Check if the result is within the bounds of the game
        return result if 0 <= result <= 101 else None
    except:
        return None

def apply_action(p1, p2, d1, d2, action):
    op_mapping = ['+', '-', '*', '/']

    # Detailed action mapping
    if action < 16:  # Both dice to P1
        op1, op2 = divmod(action, 4)
        if p1 == 101:  # P1 already at goal
            return p1, p2
        
        p1_new = apply_operator(p1, d1, op_mapping[op1])
        if p1_new is None: 
            return None
        
        p1_new = apply_operator(p1_new, d2, op_mapping[op2])
        return (p1_new, p2) if p1_new is not None else None

    elif action < 32:  # Both dice to P2
        op1, op2 = divmod(action - 16, 4)
        if p2 == 101:  # P2 already at goal
            return p1, p2
        
        p2_new = apply_operator(p2, d1, op_mapping[op1])
        if p2_new is None: 
            return None
        
        p2_new = apply_operator(p2_new, d2, op_mapping[op2])
        return (p1, p2_new) if p2_new is not None else None

    else:  # Split dice
        op1, op2 = divmod(action - 32, 4)
        
        # Handle cases where pawns are at goal
        p1_new = apply_operator(p1, d1, op_mapping[op1]) if p1 != 101 else p1
        p2_new = apply_operator(p2, d2, op_mapping[op2]) if p2 != 101 else p2
        
        if p1_new is None or p2_new is None:
            return None
        
        return p1_new, p2_new

def generate_data(num_samples=1000000):
    """
    Generate valid samples for the two-pawn Prime Climb game.
    """
    data = []
    
    while len(data) < num_samples:
        # Randomly initialize state
        p1 = random.randint(0, 101)
        p2 = random.randint(0, 101)
        d1, d2 = random.randint(1, 10), random.randint(1, 10)
        
        # Revised state encoding
        state = p1 * 10201 + p2 * 101 + (d1 * 10 + d2)
        
        # Choose a random action
        action = random.randint(0, 47)
        next_state_result = apply_action(p1, p2, d1, d2, action)
        
        # If invalid action, skip this attempt
        if next_state_result is None:
            continue
        
        p1_new, p2_new = next_state_result
        
        # Revised reward structure
        reward = -1  # Default step penalty
        
        # Reaching 101 rewards
        if p1 != 101 and p1_new == 101:
            reward += 100
        if p2 != 101 and p2_new == 101:
            reward += 100
        
        # Big bonus for completing the game
        if p1_new == 101 and p2_new == 101:
            reward += 1000
        
        # Encode next state with new random dice roll
        sp = p1_new * 10201 + p2_new * 101 + (random.randint(1, 10) * 10 + random.randint(1, 10))
        
        # Append to data
        data.append(f"{state},{action},{reward},{sp}")
    
    return data

# Write to CSV file
data = generate_data()
with open("prime_climb_twopawns_simulation.csv", "w") as f:
    f.write("s,a,r,sp\n")  # Header
    f.write("\n".join(data))