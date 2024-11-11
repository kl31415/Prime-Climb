from utils import apply_operations

class PrimeClimbMDP:
    def __init__(self):
        self.goal = 101
        self.max_position = 101
        self.min_position = 0
        self.state = 0
    
    def reset(self):
        self.state = 0
        return self.state
    
    def get_possible_moves(self, current_position, dice_rolls, is_double):
        applications = 4 if is_double else 2
        move_set = set()
        for dice in dice_rolls:
            move_set.update(apply_operations(current_position, dice, applications, self.min_position, self.max_position))
        return move_set if self.goal not in move_set else {self.goal}
    
    def step(self, action):
        self.state = action
        reward = 100 if self.state == self.goal else -1
        done = self.state == self.goal
        return self.state, reward, done
