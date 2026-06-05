from search.local_search_base import LocalSearchBase
from search.hill_climbing import HillClimbing
import random
import math

class SimulatedAnnealing(LocalSearchBase):
    def run(self, initial_state=None, temperature=70, min_temp=0.01, cd_rate=0.95):

        if initial_state is None:
            initial_state = self.initialize_state()

        temp = temperature  # Current temperature
        current_state = initial_state.copy()
        current_cost = self.evaluate(current_state)
        states_history = [current_state]
        evaluations = [current_cost]
        best_state = current_state
        best_cost = current_cost
        
        plateau = 0

        # Simulated Annealing
        while temp > min_temp:

            # Check if cost is plateaued
            if plateau == 30:
                break

            neighbor = self.get_neighbor(current_state)
            neighbor_cost = self.evaluate(neighbor)

            delta = neighbor_cost - current_cost

            # If better, always accept
            if delta < 0:
                current_state = neighbor
                current_cost = neighbor_cost

            # If worse/equal, accept with probability exp(-delta / temp)
            else:
                try:
                    probability = math.exp(-delta / temp)

                except OverflowError:
                    temp *= cd_rate # Cool down and skip
                    continue

                if random.random() < probability:
                    current_state = neighbor
                    current_cost = neighbor_cost

            if current_cost < best_cost:
                best_cost = current_cost
                best_state = current_state            

            # Keep track of plateaus
            last_cost = evaluations[-1]
            if last_cost == current_cost:
                plateau += 1
            else:
                plateau = 0

            states_history.append(current_state)
            evaluations.append(current_cost)

            temp *= cd_rate

        # Find region's optima using Hill Climbing
        HC = HillClimbing(self.world)
        _, _, HC_evaluations, HC_states_history = HC.run(
            initial_state=current_state)

        evaluations.extend(HC_evaluations[1:])
        states_history.extend(HC_states_history[1:])
        
        if evaluations[-1] < best_cost:
            best_cost = evaluations[-1]
            best_state = states_history[-1]
    

        return best_state, best_cost, evaluations, states_history
