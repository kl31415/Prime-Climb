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

# Function to apply a given operator with bounds check
def apply_operator(location, dice_value, operator):
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
        return None
    except:
        return None

# Greedy strategy evaluation
def greedy_evaluation(num_simulations=100000):
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

            # Check if either dice roll can reach 101 with any operator
            if any(apply_operator(location, dice, op) == 101 for dice in [dice1, dice2] for op in operators):
                location = 101
                turns += 1
                break

            # Generate all possible actions (combinations of operators)
            best_location = -1

            for action_number in range(16):  # Iterate over all 16 actions
                op1, op2 = operator_mapping[action_number]

                # Try both dice orders (dice1 with op1 and dice2 with op2 OR vice versa)
                new_location1 = apply_operator(location, dice1, op1)
                if new_location1 is not None:
                    new_location1 = apply_operator(new_location1, dice2, op2)

                new_location2 = apply_operator(location, dice2, op1)
                if new_location2 is not None:
                    new_location2 = apply_operator(new_location2, dice1, op2)

                # Check if the location is valid and better than the current best location
                if new_location1 is not None and new_location1 > best_location:
                    best_location = new_location1

                if new_location2 is not None and new_location2 > best_location:
                    best_location = new_location2

            # Apply the best operation found
            if best_location != -1:
                location = best_location
                turns += 1
            else:
                errors += 1
                error = True
                break

            # End simulation if goal is reached
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
    plt.title("Histogram of Turns to Reach Goal State (101) - Greedy Evaluation")
    plt.xlabel("Number of Turns")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Plot error rate over simulations
    total_simulations = len(results) + errors
    error_rate = errors / total_simulations
    plt.figure(figsize=(12, 6))
    plt.bar(["Errors", "Successes"], [errors, len(results)], color=["red", "green"])
    plt.title("Error Rate vs. Successful Simulations - Greedy Evaluation")
    plt.ylabel("Count")
    plt.text(0, errors / 2, f"Error Rate: {error_rate:.2%}", ha="center", va="center", fontsize=12, color="white")
    plt.grid(axis='y')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Run greedy evaluation simulations
    results, errors = greedy_evaluation()
    print("Average turns to reach 101:", sum(results) / len(results))
    plot_convergence(results, errors)
