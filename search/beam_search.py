from search.local_search_base import LocalSearchBase
class BeamSearch(LocalSearchBase):
    def run(self, initial_state = None, beam_number = 5, branch_factor = 10, max_iter = 1000):
        if initial_state is None:
            initial_state = self.initialize_state()

        current_cost = self.evaluate(initial_state)

        states_history = [initial_state]
        evaluations = [current_cost]

        beams = [initial_state] * beam_number

        for _ in range (max_iter):
            candidates = []
            for state in beams:
                for _ in range(branch_factor):
                    neighbor = self.get_neighbor(state)
                    neighbor_cost = self.evaluate(neighbor)
                    candidates.append(neighbor, neighbor_cost)

            candidates.sort(key= lambda x: x[1])
            beams = candidates[:beam_number]

            if candidates[0][1] < current_cost:
                current_cost = candidates[0][1]
                evaluations.append(current_cost)
                states_history.append(candidates[0][0])

            else:
                break
        
        best_state = states_history[-1]
        best_cost = evaluations[-1]
        return best_state, best_cost, evaluations, states_history