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

# Define primes between 11 and 100
primes = {11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

# Function to apply operator with bounds check
def apply_operator(location, dice_value, operator):
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
        return result if 0 <= result <= 101 else None
    except:
        return None

# Function to attempt all operator pairs as a fallback
def fallback_operations(location, dice1, dice2):
    remaining_actions = list(operator_mapping.values())
    random.shuffle(remaining_actions)  # Randomize the order of actions
    for op1, op2 in remaining_actions:
        new_location = apply_operator(location, dice1, op1)
        if new_location is None:
            continue
        new_location = apply_operator(new_location, dice2, op2)
        if new_location is not None:
            return new_location
    return None  # If no valid operation pair is found

# Greedy strategy with the "roll again" rule for primes
def greedy_evaluation_with_rollagain(num_simulations=100000):
    results = []
    errors = 0

    for _ in range(num_simulations):
        location = 0  # Starting location
        turns = 0
        error = False
        while location != 101:
            roll_again = False  # Assume no reroll unless conditions are met

            # Roll two dice
            dice1 = random.randint(1, 10)
            dice2 = random.randint(1, 10)

            # Generate all possible actions (combinations of operators)
            best_location = -1

            for action_number in range(16):
                op1, op2 = operator_mapping[action_number]

                # Try both dice orders
                new_location1 = apply_operator(location, dice1, op1)
                if new_location1 is not None:
                    new_location1 = apply_operator(new_location1, dice2, op2)

                new_location2 = apply_operator(location, dice2, op1)
                if new_location2 is not None:
                    new_location2 = apply_operator(new_location2, dice1, op2)

                # Update the best location found
                if new_location1 is not None and new_location1 > best_location:
                    best_location = new_location1
                if new_location2 is not None and new_location2 > best_location:
                    best_location = new_location2

            # Apply the best action found
            if best_location != -1:
                location = best_location
                turns += 1

            # Check if the next position is a prime number between 11 and 97
            while location in primes and location != 101:
                # If it's a prime, roll again and move again
                dice1 = random.randint(1, 10)  # Reroll the dice
                dice2 = random.randint(1, 10)

                # Generate all possible actions (combinations of operators)
                best_location = -1

                for action_number in range(16):
                    op1, op2 = operator_mapping[action_number]

                    # Try both dice orders
                    new_location1 = apply_operator(location, dice1, op1)
                    if new_location1 is not None:
                        new_location1 = apply_operator(new_location1, dice2, op2)

                    new_location2 = apply_operator(location, dice2, op1)
                    if new_location2 is not None:
                        new_location2 = apply_operator(new_location2, dice1, op2)

                    # Update the best location found
                    if new_location1 is not None and new_location1 > best_location:
                        best_location = new_location1
                    if new_location2 is not None and new_location2 > best_location:
                        best_location = new_location2

                # Apply the best action again after reroll
                if best_location != -1:
                    location = best_location

            # If no valid location was found and it's not a prime, break
            if best_location == -1:
                errors += 1
                error = True
                break

            # If we've reached 101, stop
            if location == 101:
                break

        if not error:
            results.append(turns)

    return results, errors

# Function to plot convergence or error rate
def plot_convergence(results, errors):
    # Plot histogram of results (number of turns to reach 101)
    plt.figure(figsize=(12, 6))
    plt.hist(results, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title("Histogram of Turns to Reach Goal State (101)")
    plt.xlabel("Number of Turns")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Plot error rate over simulations
    total_simulations = len(results) + errors
    error_rate = errors / total_simulations
    plt.figure(figsize=(12, 6))
    plt.bar(["Errors", "Successes"], [errors, len(results)], color=["red", "green"])
    plt.title("Error Rate vs. Successful Simulations")
    plt.ylabel("Count")
    plt.text(0, errors / 2, f"Error Rate: {error_rate:.2%}", ha="center", va="center", fontsize=12, color="white")
    plt.grid(axis='y')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Run greedy evaluation simulations with "roll again" rule
    results, errors = greedy_evaluation_with_rollagain()
    if results:
        print(f"Average Turns to Reach Goal: {sum(results) / len(results):.2f}")
    plot_convergence(results, errors)
