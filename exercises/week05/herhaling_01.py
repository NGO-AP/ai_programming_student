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
        characters = []
        for _ in range(length):
            characters.append(random.sample(string.printable,1)[0])
        return "".join(characters)

    def calculate_fitness(self, phrase):
        score = 0
        for char, correct in zip(phrase, self.target_phrase):
            if char == correct: score += 1
        return score / len(self.target_phrase)

    def generate_population(self, size, phrase_length):
        population = []
        for _ in range(size):
            individual = self.generate_phrase(phrase_length)
            population.append(individual)
        return population

    def crossover(self, phrase1, phrase2):
        point = random.randint(1, len(phrase1) - 1)
        return phrase1[:point] + phrase2[point:]

    def mutate(self, phrase, rate):
        new_phrase = []
        for character in phrase:
            if random.random() < rate:
                new_phrase.append(random.sample(string.printable, 1)[0])
            else: new_phrase.append(character)
        return "".join(new_phrase)


    def select_best(self, population):
        best = sorted(population, key=self.calculate_fitness, reverse=True)
        return best[0], best[1]

    def genetic_algorithm(self):
        population = self.generate_population(self.population_size, len(self.target_phrase))
        for generation in range(self.num_generations):
            parents = self.select_best(population)
            if generation % 100 == 0:
                print(f"Beste zin na {generation} generaties: {parents[0]}")
            if parents[0] == self.target_phrase:
                return parents[0] + f" (na {generation} generaties)"
            new_generation = []
            for _ in range(self.population_size):
                child = self.crossover(parents[0], parents[1])
                child = self.mutate(child, self.mutation_rate)
                new_generation.append(child)
            population = new_generation
        return self.select_best(population)[0]



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
    score = np.sum(solution*waarden)
    if np.sum(solution*gewichten) > capaciteit:
        score -= 1000
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
