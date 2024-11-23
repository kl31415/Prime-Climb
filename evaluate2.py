import random

# Define operators and their mapping to numbers
operators = ['+', '-', '*', '/']
operator_mapping = {
    0: ('+', '+'), 1: ('+', '-'), 2: ('+', '*'), 3: ('+', '/'),
    4: ('-', '+'), 5: ('-', '-'), 6: ('-', '*'), 7: ('-', '/'),
    8: ('*', '+'), 9: ('*', '-'), 10: ('*', '*'), 11: ('*', '/'),
    12: ('/', '+'), 13: ('/', '-'), 14: ('/', '*'), 15: ('/', '/')
}

# Load the policy file
def load_policy(file_path):
    policy = []
    with open(file_path, mode='r') as file:
        for line in file:
            action = int(line.strip())
            policy.append(action)
    return policy

# Function to apply a given operator with bounds check
def apply_operator(location, dice_value, operator):
    while True:
        try:
            # Apply the operator to the location and dice_value
            if operator == '+':
                result = location + dice_value
            elif operator == '-':
                result = location - dice_value
            elif operator == '*':
                result = location * dice_value
            elif operator == '/':
                # Check if dice_value divides location without remainder
                if location % dice_value == 0:
                    result = location // dice_value  # Perform integer division
                else:
                    result = None  # Invalid division (remainder present)

            # If the result is valid (between 0 and 101), return it
            if result is not None and 0 <= result <= 101:
                return result

            # Otherwise, select a new random operator and try again
            operator = random.choice(operators)
        except:
            return None

# def apply_operator(location, dice_value, operator):
#     try:
#         if operator == '+':
#             result = location + dice_value
#         elif operator == '-':
#             result = location - dice_value
#         elif operator == '*':
#             result = location * dice_value
#         elif operator == '/':
#             result = location // dice_value
#         return result if 0 <= result <= 101 else None
#     except:
#         return None

# Run simulations following the policy
def run_simulations(policy, num_simulations=100000):
    results = []
    errors = 0
    for _ in range(num_simulations):
        location = 0  # Starting location
        turns = 0
        error = False
        while location != 101:
            # Roll two dice
            dice1 = random.randint(1, 10)
            dice2 = random.randint(1, 10)
            state = location * 10000 + int(f"{dice1}{dice2}")

            # Look up action in policy
            action_number = policy[state]
            op1, op2 = operator_mapping[action_number]

            # Apply operators to determine new location
            new_location = apply_operator(location, dice1, op1)
            if new_location is None:
                errors += 1
                error = True
                break
            new_location = apply_operator(new_location, dice2, op2)
            if new_location is None:
                errors += 1
                error = True
                break
            # Update location and increment turn count
            location = new_location
            turns += 1

            # End simulation if goal is reached
            if location == 101:
                break
        if not error:
            results.append(turns)

    return results, errors

# Main execution
if __name__ == "__main__":
    # Load policy file (pay attention to parameters!)
    policy_file_path = "eps=1000,gamma=1,lr=0.1.policy"
    policy = load_policy(policy_file_path)
    
    # Run simulations
    results, errors = run_simulations(policy)
    print(sum(results) / len(results))

# eps = 1000, gamma = 1, lr = 0.1: 34.264
# eps = 5000, gamma = 1, lr = 0.1: 34.368
# eps = 10000, gamma = 1, lr = 0.1: 34.373