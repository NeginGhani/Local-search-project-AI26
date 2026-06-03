from search.local_search_base import LocalSearchBase
from search.hill_climbing import HillClimbing
import random
import math

class SimulatedAnnealing(LocalSearchBase):
    def run(self, initial_state = None, temperature = 1000, min_temp = 0.01, cd_rate = 0.9):
        if initial_state is None:
            initial_state = self.initialize_state()

        temp = temperature
        current_state = initial_state.copy()
        current_cost = self.evaluate(current_state)

        states_history = [initial_state]
        evaluations = [current_cost]

        # Simulated Annealing
        while temp > min_temp:

            pick = 1
            delta = 1
            probability = 0

            while delta > 0 and pick > probability:                
                neighbor = self.get_neighbor(current_state)
                neighbor_cost = self.evaluate(neighbor)
                delta = neighbor_cost - current_cost
                pick = random.random()
                temp *= cd_rate
                probability = math.exp(max(-delta/temp, -500))
                if temp < min_temp:
                    break

            current_state = neighbor
            current_cost = neighbor_cost
            
            states_history.append(current_state)
            evaluations.append(current_cost)
            temp *= cd_rate

        # Find region's optima using Hill Climbing
        HC = HillClimbing(self.world)
        best_state, best_cost, HC_evaluations, HC_states_history = HC.run(initial_state = current_state, max_iter = 500)
        evaluations.extend(HC_evaluations[1:])
        states_history.extend(HC_states_history[1:])

        return best_state, best_cost, evaluations, states_history
        
