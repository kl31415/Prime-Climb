import numpy as np
from collections import defaultdict

def get_all_possible_transitions():
    """
    Analyzes all possible state transitions based on dice rolls and operations.
    Returns a dictionary where keys are current states and values are sets of 
    possible next states that can be reached with any valid dice roll combination.
    """
    transitions = defaultdict(set)
    
    # For each starting position
    for pos in range(102):
        # For each possible dice roll combination (no doubles)
        for dice1 in range(1, 11):
            for dice2 in range(1, 11):  # Consider both dice independently
                # Get moves from first die
                moves1 = apply_operations(pos, dice1, 2)
                for move in moves1:
                    transitions[pos].add(move)
                    
                # Get moves from second die
                moves2 = apply_operations(move, dice2, 2)
                for move in moves2:
                    transitions[pos].add(move)
                            
    return transitions

def apply_operations(current_pos, number, applications=2):
    """Get all possible positions after applying operations to current position"""
    possible_positions = set()
    
    operations = [
        lambda x, y: x + y,  # addition
        lambda x, y: x - y,  # subtraction
        lambda x, y: x * y,  # multiplication
        lambda x, y: x // y if y != 0 and x % y == 0 else None  # division
    ]
    
    # Ensure that current_pos is a single integer, not a set
    if isinstance(current_pos, set):
        # If current_pos is a set, we will apply operations on each element of the set
        for pos in current_pos:
            for _ in range(applications):
                for op in operations:
                    result = op(pos, number)
                    if result is not None and 0 <= result <= 101:
                        possible_positions.add(result)
    else:
        # If current_pos is just a number, apply the operations directly
        for _ in range(applications):
            for op in operations:
                result = op(current_pos, number)
                if result is not None and 0 <= result <= 101:
                    possible_positions.add(result)

    # If no valid positions were found, return the initial position
    return possible_positions if possible_positions else {current_pos}

def roll_dice():
    """Roll two 10-sided dice and return the dice rolls"""
    dice1 = np.random.randint(1, 11)
    dice2 = np.random.randint(1, 11)
    return dice1, dice2  # Removed the double check
