from search.local_search_base import LocalSearchBase


class BeamSearch(LocalSearchBase):

    def run(self, initial_state = None, beam_number = 5, branch_factor = 15):

        if initial_state is None:
            initial_state = self.initialize_state()

        current_state = initial_state.copy()
        current_cost = self.evaluate(current_state)
        states_history = [current_state]
        evaluations = [current_cost]
        beams = [current_state]
        
        for _ in range(beam_number - 1):
            beam_root = self.get_neighbor(initial_state)
            beams.append(beam_root)
        
        for _ in range(self.max_iter):
            
            candidates = [] # Keeps all beams' children
            # Expand each beam branch_factor times
            for state in beams:
                for _ in range(branch_factor):
                    neighbor = self.get_neighbor(state)
                    neighbor_cost = self.evaluate(neighbor)
                    candidates.append((neighbor, neighbor_cost))

            candidates.sort(key= lambda x: x[1])

            top_candidate = candidates[0][1]

            # Check progress
            if top_candidate <= current_cost:
                beams = [state for state, _ in candidates[:beam_number]]
                current_cost = top_candidate
                evaluations.append(top_candidate)
                states_history.append(candidates[0][0])

            else:
                break
        
        best_state = states_history[-1]
        best_cost = evaluations[-1]
        return best_state, best_cost, evaluations, states_history