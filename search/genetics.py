from search.local_search_base import LocalSearchBase
import random
import statistics
from search.hill_climbing import HillClimbing

class Genetics(LocalSearchBase):
    def run(self, initial_state = None, population_size = 20):

        if not initial_state:
            initial_state = self.initialize_state()

        current_state = initial_state.copy()
        current_cost = self.evaluate(current_state)
        best_state = current_state
        best_cost = current_cost

        population = [self.mutation(current_state) for _ in range(population_size)]
        states_history = [current_state]
        evaluations = [current_cost]
        
        plateau = 0
        
        for _ in range(self.max_iter):
            
            # Check if cost is plateaued
            if plateau == 30:
                break

            next_generation = []    # Keep all childern

            for _ in range(population_size * 2):
                parent1, parent2 = random.sample(population, 2)
                new_child = self.cross_over(parent1, parent2)
                new_child = self.mutation(new_child)
                next_generation.append(new_child)
        
            
            population = self.fitness(next_generation)  # exclude roughly half of the generation
            current_state = min(population, key= self.evaluate)
            current_cost = self.evaluate(current_state)

            if current_cost < best_cost:
                best_cost = current_cost
                best_state = current_state

            # Keep track of plateaus
            last_cost = evaluations[-1]
            if last_cost == current_cost:
                plateau += 1
            else:
                plateau = 0

            evaluations.append(current_cost)
            states_history.append(current_state)

        last_state = states_history[-1]
        HC = HillClimbing(self.world)
        _, _, HC_evaluations, HC_states_history = HC.run(
        initial_state=last_state)

        evaluations.extend(HC_evaluations[1:])
        states_history.extend(HC_states_history[1:])

        if evaluations[-1] < best_cost:
            best_cost = evaluations[-1]
            best_state = states_history[-1]
    

        return best_state, best_cost, evaluations, states_history



    def cross_over(self, parent1, parent2):
        # random combination of parents' features
        gene_pool = list(set(parent1 + parent2))
        weight_map = dict(zip(self.valid_pos, self.pos_chance))
        gene_weights = [weight_map[pos] for pos in gene_pool]

        length = min(self.N, len(gene_pool))
        l = random.randint(0, length)
        child = []
        while len(child) < l and gene_pool:
            s = random.choices(population=gene_pool, weights=gene_weights, k=1)[0]

            idx = gene_pool.index(s)
            child.append(s)

            del gene_pool[idx]
            del gene_weights[idx]

        return sorted(child)

    def mutation(self, state):
        # 45% no mutation, 45% move a sensor, 10% delete a sensor 
        action = random.random()
        if action >= 0.45:
            state = self.get_neighbor(state, action)
        return state
    
    def fitness(self, generation):
        # Keep states that are better than cost median
        costs = [self.evaluate(state) for state in generation]
        threshold = statistics.median(costs)
        fit_children = [sorted(child) for child, cost in zip(generation, costs) if cost <= threshold]
        return fit_children