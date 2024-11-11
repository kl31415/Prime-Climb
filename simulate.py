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

# Function to apply operator with bounds check, retrying until a valid result is obtained
def apply_operator(location, dice_value):
    result = None
    while result is None:
        operator = random.choice(operators)
        try:
            if operator == '+':
                result = location + dice_value
            elif operator == '-':
                result = location - dice_value
            elif operator == '*':
                result = location * dice_value
            elif operator == '/':
                if dice_value != 0 and location % dice_value == 0:
                    result = location // dice_value

            # Ensure result is within the bounds
            if not (0 <= result <= 101):
                result = None  # Retry if result is out of bounds
        except:
            result = None  # Retry on any exception

    return result, operator

# Generate simulation data
data = []
location = 0  # Starting location for a new game
for _ in range(1000000):
    dice1 = random.randint(1, 11)
    dice2 = random.randint(1, 11)
    state = location * 100 + int(f"{dice1}{dice2}")

    # Apply the operators, retrying as needed for valid operators
    new_location, op1 = apply_operator(location, dice1)
    new_location, op2 = apply_operator(new_location, dice2)
    action = operator_mapping[(op1, op2)]

    # Determine reward and next state
    reward = 10000 if new_location == 101 else -1
    next_state = new_location * 100 + int(f"{dice1}{dice2}")

    # Append data
    data.append([state, action, reward, next_state])

    # Update location for the next game cycle
    location = 0 if new_location == 101 else new_location

# Save to CSV file
output_path = 'prime_climb_simulation.csv'
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['s', 'a', 'r', 'sp'])
    writer.writerows(data)

output_path
