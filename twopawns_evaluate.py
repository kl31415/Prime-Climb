import random
import matplotlib.pyplot as plt

# Define operators and mapping
operators = ['+', '-', '*', '/']

# Operator mapping for 48 actions:
# First 16: Apply both rolls to the first pawn
# Next 16: Apply both rolls to the second pawn
# Last 16: Apply one roll to each pawn
operator_mapping = {i: divmod(i % 16, 4) for i in range(48)}

# Load policy file
def load_policy(file_path):
    policy = []
    with open(file_path, mode='r') as file:
        for line in file:
            policy.append(int(line.strip()))
    return policy

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

    except:
        return None

# Function to apply actions to the pawns based on action number
def apply_action(p1, p2, d1, d2, policy_action, remaining_actions):
    """
    Applies the given policy action first, then tries other actions without replacement.
    """
    # Try the policy action first
    op1, op2 = operator_mapping[policy_action]
    op1, op2 = operators[op1], operators[op2]

    if policy_action < 16:
        # Apply both rolls to pawn 1
        new_p1 = apply_operator(p1, d1, op1)
        if new_p1 is not None:
            new_p1 = apply_operator(new_p1, d2, op2)
            if new_p1 is not None:
                return new_p1, p2
    elif policy_action < 32:
        # Apply both rolls to pawn 2
        new_p2 = apply_operator(p2, d1, op1)
        if new_p2 is not None:
            new_p2 = apply_operator(new_p2, d2, op2)
            if new_p2 is not None:
                return p1, new_p2
    else:
        # Apply one roll to each pawn
        new_p1 = apply_operator(p1, d1, op1)
        new_p2 = apply_operator(p2, d2, op2)
        if new_p1 is not None and new_p2 is not None:
            return new_p1, new_p2

    # If the policy action failed, try remaining actions
    while remaining_actions:
        action = remaining_actions.pop(0)
        op1, op2 = operator_mapping[action]
        op1, op2 = operators[op1], operators[op2]

        if action < 16:
            new_p1 = apply_operator(p1, d1, op1)
            if new_p1 is not None:
                new_p1 = apply_operator(new_p1, d2, op2)
                if new_p1 is not None:
                    return new_p1, p2
        elif action < 32:
            new_p2 = apply_operator(p2, d1, op1)
            if new_p2 is not None:
                new_p2 = apply_operator(new_p2, d2, op2)
                if new_p2 is not None:
                    return p1, new_p2
        else:
            new_p1 = apply_operator(p1, d1, op1)
            new_p2 = apply_operator(p2, d2, op2)
            if new_p1 is not None and new_p2 is not None:
                return new_p1, new_p2

    # If no valid action is found, return None
    return None, None

# Function to run simulations for two pawns
def run_simulations(policy, num_simulations=1):
    results = []
    errors = 0

    for _ in range(num_simulations):
        p1, p2 = 0, 0  # Starting positions for both pawns
        turns = 0
        error = False
        counter = 0

        while (p1 != 101 or p2 != 101) and counter < 10:
            # Roll two dice
            d1, d2 = random.randint(1, 10), random.randint(1, 10)
            print(f"First roll: {d1}")
            print(f"Second roll: {d2}")

            # Calculate unique state
            state = p1 * 10201 + p2 * 101 + (d1 * 10 + d2)
            print(f"State: {state}")

            # Validate state and fetch action
            if state >= len(policy):
                print(f"Invalid state encountered: p1={p1}, p2={p2}, d1={d1}, d2={d2}, state={state}")
                errors += 1
                error = True
                break

            # Fetch the policy action and remaining actions
            policy_action = policy[state]
            remaining_actions = list(range(48))
            remaining_actions.remove(policy_action)
            random.shuffle(remaining_actions)
            print(f"Policy action: {policy_action}")

            # Apply the policy action first, then try other actions
            new_p1, new_p2 = apply_action(p1, p2, d1, d2, policy_action, remaining_actions)
            print(f"New p1: {new_p1}")
            print(f"New p2: {new_p2}")
            if new_p1 is None or new_p2 is None:
                errors += 1
                error = True
                break

            # Update pawns and turn count
            p1, p2 = new_p1, new_p2
            turns += 1

            # Stop if both pawns reach 101
            if p1 == 101 and p2 == 101:
                break

            counter += 1

        # If no error occurred, record the result
        if not error:
            results.append(turns)

    return results, errors

# Plot results
def plot_results(results, errors):
    plt.hist(results, bins=30, color='blue', alpha=0.7, edgecolor='black')
    plt.title("Turns to Reach Goal State (101 for Both Pawns)")
    plt.xlabel("Turns")
    plt.ylabel("Frequency")
    plt.show()

    total = len(results) + errors
    plt.bar(["Errors", "Successes"], [errors, len(results)], color=["red", "green"])
    plt.title("Simulation Outcomes")
    plt.show()

# Main
if __name__ == "__main__":
    policy_file_path = "twopawns_eps=50,gamma=1,lr=0.3.policy"
    policy = load_policy(policy_file_path)
    results, errors = run_simulations(policy)
    print(f"Average Turns: {sum(results) / len(results):.2f}")
    plot_results(results, errors)
