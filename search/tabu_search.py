from search.local_search_base import LocalSearchBase
from collections import deque


class TabuSearch(LocalSearchBase):

    def run(self, initial_state = None, tabu_size = 20, branch_factor = 10):

        if not initial_state:
            initial_state = self.initialize_state()

        current = initial_state
        current_cost = self.evaluate(initial_state)
        best_state = initial_state.copy()
        best_cost = current_cost

        tabu = deque(maxlen = tabu_size)
        states_history =  [current]
        evaluations = [current_cost]

        plateau = 0

        for _ in range(self.max_iter):

            # Check if cost is plateaued
            if plateau > 14:
                break

            candidates = []     # Keep all children

            # Expand
            for _ in range(branch_factor):
                neighbor = self.get_neighbor(current)
                neighbor_cost = self.evaluate(neighbor)
                candidates.append((neighbor, neighbor_cost))

            candidates.sort(key= lambda x: x[1])

            for neighbor, neighbor_cost in candidates:

                # find the best allowed neighbor
                if not (neighbor in tabu):
                    current = neighbor.copy()
                    current_cost = neighbor_cost
                    states_history.append(current)
                    
                    # Keep track of plateaus
                    last_cost = evaluations[-1]
                    if last_cost == current_cost:
                        plateau += 1
                    else:
                        plateau = 0

                    evaluations.append(current_cost)
                    tabu.append(neighbor)
                    break

        best_cost = evaluations[-1]
        best_state = states_history[-1]

        return best_state, best_cost, evaluations, states_history
