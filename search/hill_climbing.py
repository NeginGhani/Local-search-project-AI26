from search.local_search_base import LocalSearchBase

class HillClimbing(LocalSearchBase):
    def run(self, initial_state=None, max_iter=1000, branch_factor = 10):

        if initial_state is None:
            initial_state = self.initialize_state()

        current_state = initial_state.copy()
        current_cost = self.evaluate(initial_state)

        states_history = [initial_state]
        evaluations = [current_cost]


        for _ in range(max_iter):
            neighbors = [self.get_neighbor(current_state) for _ in range(branch_factor)]
            neighbor_cost = [self.evaluate(child) for child in neighbors]
            best_neighbor, best_neighbor_cost = min(zip(neighbors, neighbor_cost), key=lambda x: x[1])

            if best_neighbor_cost < current_cost:
                current_state = best_neighbor
                current_cost = best_neighbor_cost
                evaluations.append(best_neighbor_cost)
                states_history.append(current_state)

            else:

                break  # No improvement → stop climbing

        best_state = states_history[-1]
        best_cost = evaluations[-1]
        return best_state, best_cost, evaluations, states_history