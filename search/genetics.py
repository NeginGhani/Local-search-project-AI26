from search.local_search_base import LocalSearchBase
import random
import statistics

class Genetics(LocalSearchBase):
    def run(self, initial_state = None, population_size = 20):

        if not initial_state:
            initial_state = self.initialize_state()

        population = [self.mutation(initial_state) for _ in range(population_size)]

        best_state = min(population, key= self.evaluate)
        best_cost = self.evaluate(best_state)

        states_history = [best_state]
        evaluations = [best_cost]

        plateau = 0
        
        for _ in range(self.max_iter):
            
            # Check if cost is plateaued
            if plateau > 14:
                break

            next_generation = []    # Keep all childern

            for _ in range(population_size * 2):
                parent1, parent2 = random.sample(population, 2)
                new_child = self.cross_over(parent1, parent2)
                new_child = self.mutation(new_child)
                next_generation.append(new_child)
        
            
            population = self.fitness(next_generation)  # exclude roughly half of the generation
            current = min(population, key= self.evaluate)
            current_cost = self.evaluate(current)

            # Keep track of plateaus
            last_cost = evaluations[-1]
            if last_cost == current_cost:
                plateau += 1
            else:
                plateau = 0

            evaluations.append(current_cost)
            states_history.append(current)

        best_cost = evaluations[-1]
        best_state = states_history[-1]
        return best_state, best_cost, evaluations, states_history






    def cross_over(self, parent1, parent2):
        # random combination of parents' features
        combine = list(set(parent1 + parent2))
        random.shuffle(combine)
        lengths = sorted([len(parent1), len(parent2)])
        l = random.randint(lengths[0], lengths[1])
        return sorted(combine[:l])

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