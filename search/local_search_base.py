import random
import copy
import math

class LocalSearchBase:
    def __init__(self, world):
        self.world = world
        self.targets = world.get_targets()
        self.r = world.sensor_range
        self.N = world.max_sensors

        # Pre compute which targets are in range for each tile
        self.coverage = {}
        for i in range(world.rows):
            for j in range(world.cols):
                if world.is_valid_position(i, j):
                    covered = {(tx, ty) for tx, ty in self.targets 
                              if abs(i - tx) + abs(j - ty) <= self.r}
                    self.coverage[(i, j)] = covered

        self.valid_pos = []
        self.pos_chance = []
        for pos, cover_num in self.coverage.items():
            if cover_num:
                self.valid_pos.append(pos)
                self.pos_chance.append(len(cover_num))
        

    def evaluate(self, state):
        # cost = 10 * uncovered + num_sensors
        covered = set()
        for pos in state:
            covered.update(self.coverage.get(pos, set()))
        uncovered = len(self.targets) - len(covered)
        return 10 * uncovered + len(state)


    def initialize_state(self):
        # Generate a random start
        sensor_num = min(self.N, 10)
        state = []
        for _ in range(sensor_num):
            pos = self.get_weighted_random_position(state)
            if pos:
                state.append(pos)
        return sorted(state)

    def get_neighbor(self, state, op = None):

        # one neighbor with move/add/remove operations
        # 40% chance to add, 35% chance to move and 25% chance to remove
        
        new_state = copy.deepcopy(state)

        if not new_state:  # must add
            new_pos = self.get_weighted_random_position(new_state)
            if new_pos:
                new_state.append(new_pos)
            return sorted(new_state)

        if not op:
            op = random.random()

        # Add
        if op < 0.45 and len(new_state) < self.N:
            new_pos = self.get_weighted_random_position(new_state)
            if new_pos:
                new_state.append(new_pos)
        # Move              
        elif op < 0.90 and new_state:                    
            idx = random.randrange(len(new_state))
            new_pos = self.get_weighted_random_position(new_state)
            if new_pos:
                new_state[idx] = new_pos

        # Remove        
        elif new_state:                                 
            idx = random.randrange(len(new_state))
            del new_state[idx]

        return sorted(new_state)
    

    def get_weighted_random_position(self, current_state):
        occupied = set(current_state)        
        candidates = []
        weights = []
        
        for pos, weight in zip(self.valid_pos, self.pos_chance):
            if pos not in occupied:
                candidates.append(pos)
                weights.append(weight)                
        if not candidates:
            return None
        
        return random.choices(candidates, weights=weights, k=1)[0]

