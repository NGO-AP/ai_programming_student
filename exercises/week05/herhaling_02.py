"""
Oefening 1: Word Generator (Genetisch Algoritme)
==================================================
Evolueer een populatie van willekeurige zinnen naar een doelzin.
"""
import random
import string


class WordPuzzle:
    def __init__(self, target_phrase, population_size=100, mutation_rate=0.01, num_generations=10000):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length):
        return "".join([random.sample(string.printable,1)[0] for _ in range(length)])

    def calculate_fitness(self, phrase):
        return sum([1 for a, b in zip(phrase, self.target_phrase) if a==b]) / len(self.target_phrase)

    def generate_population(self, size, phrase_length):
        return [self.generate_phrase(phrase_length) for _ in range(size)]

    def crossover(self, phrase1, phrase2):
        crosspoint = random.randint(1, len(phrase1) - 1)
        return phrase1[:crosspoint] + phrase2[crosspoint:]

    def mutate(self, phrase, rate):
        mutation = []
        for character in phrase:
            if random.random() < rate:
                mutation.append(random.sample(string.printable,1)[0])
            else: mutation.append(character)
        return "".join(mutation)

    def select_best(self, population):
        return tuple(sorted(population, key=self.calculate_fitness, reverse=True)[0:2])

    def genetic_algorithm(self):
        current_population = self.generate_population(self.population_size, len(self.target_phrase))
        for generation in range(self.num_generations):
            parent1, parent2 = self.select_best(current_population)
            if parent1 == self.target_phrase:
                return parent1 + f" (na {generation} generaties)"
            if generation % 100 == 0: print(f"Na {generation} generaties: {parent1}")
            offspring = []
            for _ in range(self.population_size):
                child = self.crossover(parent1, parent2)
                child = self.mutate(child, self.mutation_rate)
                offspring.append(child)
            current_population = offspring
        return f"Geen perfecte match gevonden. Beste resultaat na {self.num_generations}: {self.select_best(current_population)[0]}"



def main():
    target_phrase = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzle = WordPuzzle(target_phrase)
    best_phrase = puzzle.genetic_algorithm()
    print(f"Beste zin: {best_phrase}")


if __name__ == "__main__":
    main()

"""
Oefening 2: Knapsack Probleem met pygad
=========================================
Los het knapsack probleem op met een genetisch algoritme.
"""
import pygad
import numpy as np

# Data
capaciteit = 10
gewichten = np.array([5, 4, 6, 3])
waarden = np.array([10, 40, 30, 50])
n_voorwerpen = len(gewichten)


def fitness_func(ga_instance, solution, solution_idx):
    # TODO: bereken totale waarde, straf als gewicht > capaciteit
    score = sum(solution * waarden)
    if sum(solution * gewichten) > capaciteit: score -= 1000
    return score

# TODO: configureer pygad.GA (zie OneMax.py uit de cursus)
ga_instance = pygad.GA(
    num_generations=40,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=300,
    num_genes=n_voorwerpen,
    mutation_percent_genes=10,
    gene_space=[0, 1]
)
ga_instance.run()

# Oplossing tonen
solution, solution_fitness, _ = ga_instance.best_solution()
print("Gekozen voorwerpen:", solution)
print("Totale waarde:", solution_fitness)