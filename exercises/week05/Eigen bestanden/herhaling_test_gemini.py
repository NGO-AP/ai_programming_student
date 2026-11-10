"""
Oefening 1: Roosterplanning (Simulated Annealing)
Het probleem: Je moet 5 examens inplannen in 3 beschikbare tijdsloten (0, 1 en 2). Sommige studenten hebben overlappende vakken, dus als je twee examens in hetzelfde tijdslot zet, ontstaan er conflicten (studenten die op twee plaatsen tegelijk moeten zijn).Doel: Minimaliseer het aantal conflicten met Simulated Annealing.

Representatie: Een staat is een lijst met tijdsloten. Bijvoorbeeld [0, 1, 0, 2, 1] betekent: Examen 0 in slot 0, Examen 1 in slot 1, Examen 2 in slot 0, etc.

Stappenplan:

    1. Maak calculate_cost(state): overloop alle mogelijke paren van examens (bijv. met twee geneste loops). Als ze in hetzelfde tijdslot zitten, tel dan het aantal conflicten op (te vinden in de conflict_matrix).

    2. Maak random_neighbor(state): kies een willekeurig examen en verander het tijdslot naar een willekeurig ander tijdslot.

    3. Vul de simulated_annealing() kern aan (de logica ken je inmiddels!).
"""

import math
import random

class ExamScheduler:
    def __init__(self, conflict_matrix, num_timeslots=3, initial_temperature=100.0, cooling_rate=0.99, num_iterations=5000):
        self.conflict_matrix = conflict_matrix
        self.num_exams = len(conflict_matrix)
        self.num_timeslots = num_timeslots
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def calculate_cost(self, state: list[int]) -> int:
        """Berekent het totaal aantal conflicten in het huidige rooster."""
        # TODO
        cost = 0
        for exam1 in range(len(state)):
            for exam2 in range(exam1 + 1, len(state)):
                slot1 = state[exam1]
                slot2 = state[exam2]
                if slot1 == slot2:
                    cost += self.conflict_matrix[exam1][exam2]
        return cost

    def random_neighbor(self, state: list[int]) -> list[int]:
        """Kiest 1 willekeurig examen en wijst er een nieuw, willekeurig tijdslot aan toe."""
        # TODO
        neigbour = state.copy()
        exam = random.randint(0, len(state)-1)
        slot = random.randint(0, self.num_timeslots-1)
        neigbour[exam] = slot
        return neigbour

    def simulated_annealing(self) -> tuple[list[int], int]:
        """Zoekt het rooster met de minste conflicten."""
        # TODO: start met een willekeurige toewijzing van examens aan tijdsloten (bijv. random tussen 0 en num_timeslots-1)
        temperature = self.initial_temperature
        current_schedule = [random.randint(0, self.num_timeslots-1) for _ in range(self.num_exams)]
        current_conflicts = self.calculate_cost(current_schedule)
        best_schedule = current_schedule
        best_conflicts = current_conflicts

        for k in range(self.num_iterations):
            new_schedule = self.random_neighbor(current_schedule)
            new_conflicts = self.calculate_cost(new_schedule)
            delta = new_conflicts - current_conflicts

            if delta < 0:
                current_schedule = new_schedule
                current_conflicts = new_conflicts

            else:
                P = math.exp(-delta/temperature)
                if random.random() < P:
                    current_schedule = new_schedule
                    current_conflicts = new_conflicts

            if current_conflicts < best_conflicts:
                best_schedule = current_schedule
                best_conflicts = current_conflicts

            temperature *= self.cooling_rate

        return best_schedule, best_conflicts


if __name__ == "__main__":
    # Conflict matrix: entry (i, j) toont hoeveel studenten examen i EN examen j hebben.
    # We willen zo min mogelijk overlappende studenten in hetzelfde tijdslot.
    conflict_matrix = [
        [0, 10,  0,  5,  2],
        [10, 0,  8,  0,  4],
        [0,  8,  0, 12,  0],
        [5,  0, 12,  0,  7],
        [2,  4,  0,  7,  0]
    ]

    scheduler = ExamScheduler(conflict_matrix)
    best_schedule, min_conflicts = scheduler.simulated_annealing()

    print("Beste rooster:", best_schedule)
    print("Aantal conflicten (kosten):", min_conflicts)

"""
Oefening 2: Vrachtwagens Balanceren (Genetische Algoritmes met PyGAD)
Het probleem: Je werkt voor een koeriersbedrijf en moet 8 zware pakketten verdelen over exact 2 vrachtwagens (Vrachtwagen 0 en Vrachtwagen 1). Je wil dat het totale gewicht van beide vrachtwagens zo dicht mogelijk bij elkaar ligt.Doel: Minimaliseer het verschil in gewicht tussen de twee vrachtwagens met een GA via pygad.

Representatie: Een individu is een array met 0'en en 1'en (bijv. [0, 1, 1, 0...]), waarbij de waarde aangeeft in welke vrachtwagen het pakket zit.

Stappenplan:

    1. Maak de fitness_func. Bereken het totale gewicht in vrachtwagen 0 en vrachtwagen 1.

    2. Bepaal het absolute verschil tussen deze twee gewichten (bijv. verschil = abs(gewicht_0 - gewicht_1)).

    3. Belangrijk: PyGAD zoekt altijd de hoogste fitness. Een verschil van 0 is perfect, een verschil van 50 is slecht. Hoe zet je dit verschil om naar een fitness-score die PyGAD goed kan maximaliseren? (Tip: denk aan een minteken of een breuk).

    4. Configureer de pygad.GA instance.
"""

import pygad
import numpy as np

# Data: gewichten van de 8 pakketten
pakketten = np.array([45, 20, 35, 15, 60, 25, 10, 50])

def fitness_func(ga_instance, solution, solution_idx):
    # TODO: bereken gewicht in vrachtwagen 0 en vrachtwagen 1
    # TODO: bereken het verschil en zet dit om naar een logische fitness-score
    truck1 = 0
    truck2 = 0

    for truck, packet in zip(solution, pakketten):
        if truck == 0:
            truck1 += packet
        else: truck2 += packet

    difference = abs(truck1-truck2)

    if difference == 0: difference += 1*10e-10

    return 1/difference

# TODO: configureer pygad.GA
# Tip: vergeet niet dat we enkel vrachtwagen 0 en vrachtwagen 1 hebben!
ga_instance = pygad.GA(
    num_generations=40,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=300,
    num_genes=len(pakketten),
    mutation_percent_genes=10,
    gene_space=[0,1]
)

ga_instance.run()
solution, solution_fitness, _ = ga_instance.best_solution()
print("Ideale verdeling:", solution)
print("Fitness score:", solution_fitness)