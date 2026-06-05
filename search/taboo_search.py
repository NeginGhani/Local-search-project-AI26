from search.local_search_base import LocalSearchBase
from collections import deque


class TabooSearch(LocalSearchBase):

    def run(self, initial_state = None, taboo_size = 20, branch_factor = 10):

        if not initial_state:
            initial_state = self.initialize_state()

        current_state = initial_state.copy()
        current_cost = self.evaluate(initial_state)
        best_state = current_state
        best_cost = current_cost

        taboo = deque(maxlen = taboo_size)
        states_history =  [current_state]
        evaluations = [current_cost]
        

        for _ in range(self.max_iter):

            candidates = []     # Keep all children

            # Expand
            for _ in range(branch_factor):
                neighbor = self.get_neighbor(current_state)
                neighbor_cost = self.evaluate(neighbor)
                candidates.append((neighbor, neighbor_cost))

            candidates.sort(key= lambda x: x[1])

            for neighbor, neighbor_cost in candidates:

                # find the best allowed neighbor
                if not (neighbor in taboo):
                    current_state = neighbor.copy()
                    current_cost = neighbor_cost
                    states_history.append(current_state)

                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_state = current_state


                    evaluations.append(current_cost)
                    taboo.append(neighbor)
                    break


        return best_state, best_cost, evaluations, states_history
