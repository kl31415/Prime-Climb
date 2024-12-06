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

# Load the policy file
def load_policy(file_path):
    policy = []
    with open(file_path, mode='r') as file:
        for line in file:
            action = int(line.strip())
            policy.append(action)
    return policy

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

# Run simulations with the "roll again" rule for primes
def run_simulations_with_rollagain(policy, num_simulations=1):
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
            print(f"Location: {location}")
            print(f"Dice 1: {dice1}, Dice 2: {dice2}")

            # Consider both dice orders
            dice_permutations = [(dice1, dice2), (dice2, dice1)]
            best_result = None

            for d1, d2 in dice_permutations:
                state = location * 10000 + int(f"{d1}{d2}")
                action_number = policy[state]
                op1, op2 = operator_mapping[action_number]

                # Apply operators to determine new location
                new_location = apply_operator(location, d1, op1)
                if new_location is None:
                    continue
                new_location = apply_operator(new_location, d2, op2)
                if new_location is not None and (best_result is None or new_location > best_result):
                    best_result = new_location

            if best_result is None:
                errors += 1
                error = True
                break

            # Update location and increment turn count
            location = best_result
            turns += 1
            print(f"New location: {location}")

            # Check if the pawn lands on a prime and apply "roll again"
            while location in primes:
                extra_dice1 = random.randint(1, 10)
                extra_dice2 = random.randint(1, 10)
                print(f"Extra dice 1: {extra_dice1}, Extra dice 2: {extra_dice2}")
                dice_permutations = [(extra_dice1, extra_dice2), (extra_dice2, extra_dice1)]
                extra_best_result = None

                for d1, d2 in dice_permutations:
                    state = location * 10000 + int(f"{d1}{d2}")
                    action_number = policy[state]
                    op1, op2 = operator_mapping[action_number]

                    # Apply extra dice rolls
                    new_location = apply_operator(location, d1, op1)
                    if new_location is None:
                        continue
                    new_location = apply_operator(new_location, d2, op2)
                    if new_location is not None and (extra_best_result is None or new_location > extra_best_result):
                        extra_best_result = new_location

                if extra_best_result is None:
                    errors += 1
                    error = True
                    break

                location = extra_best_result  # Update location after extra rolls
                print(f"Extra location: {location}")

            if error:
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
    # Load policy file
    policy_file_path = "eps=10000,gamma=1,lr=0.1,reward_type=nonlinear.policy"
    policy = load_policy(policy_file_path)
    
    # Run simulations with "roll again" rule
    results, errors = run_simulations_with_rollagain(policy)
    if results:
        print(f"Average Turns to Reach Goal: {sum(results) / len(results):.2f}")
    plot_convergence(results, errors)
