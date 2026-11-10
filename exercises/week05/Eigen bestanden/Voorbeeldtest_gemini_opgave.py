"""
Oefening: Kaartkleuren (Graph Coloring) met Simulated Annealing
================================================================
Het probleem: Je krijgt een lijst van 'buren' (regio's die aan elkaar grenzen). 
Je moet elke regio een kleur geven (voorgesteld door een getal 0, 1, 2, ...).
Regio's die een grens delen, mogen NIET dezelfde kleur hebben.

Doel: Minimaliseer het aantal grensconflicten met Simulated Annealing.

Representatie: 
Een staat is een lijst van integers, waarbij de index de regio is en de 
waarde de toegekende kleur. 
Voorbeeld: [0, 1, 0, 2] betekent regio 0 heeft kleur 0, regio 1 heeft kleur 1, etc.

Stappenplan:
    1. Maak calculate_cost(state): loop over alle grenzen (edges) in self.adjacencies. 
       Een 'edge' is een tuple (regio_A, regio_B). Controleer of de kleur van regio_A 
       gelijk is aan de kleur van regio_B in je huidige staat. Zo ja, tel 1 conflict op.
    2. Maak random_neighbor(state): kies een willekeurige regio en geef deze 
       een NIEUWE willekeurige kleur (zorg dat het niet toevallig dezelfde kleur blijft).
    3. Vul de simulated_annealing() kern in (met koeling en de math.exp acceptatiekans).
"""

import math
import random

class MapColoring:
    def __init__(self, num_regions, adjacencies, num_colors=3, initial_temperature=100.0, cooling_rate=0.99, num_iterations=3000):
        self.num_regions = num_regions
        self.adjacencies = adjacencies  # Lijst van tuples: bijv. (0, 1) betekent regio 0 en 1 grenzen aan elkaar.
        self.num_colors = num_colors
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def calculate_cost(self, state: list[int]) -> int:
        """Berekent het aantal grensconflicten (buurlanden met dezelfde kleur)."""
        # TODO
        pass

    def random_neighbor(self, state: list[int]) -> list[int]:
        """Kiest 1 willekeurige regio en geeft deze een nieuwe willekeurige kleur."""
        # TODO
        pass

    def simulated_annealing(self) -> tuple[list[int], int]:
        """Zoekt de inkleuring met de minste conflicten."""
        # TODO: start met een willekeurige toewijzing van kleuren (0 tot num_colors-1) aan elke regio.
        pass


if __name__ == "__main__":
    # Testdata: Een fictieve kaart met 7 regio's (0 t/m 6)
    # We proberen dit in te kleuren met slechts 3 kleuren!
    num_regions = 7
    adjacencies = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 4),
        (2, 3), (2, 4), (2, 5),
        (3, 5), (3, 6),
        (4, 5),
        (5, 6)
    ]

    map_solver = MapColoring(num_regions, adjacencies, num_colors=3)
    best_coloring, min_conflicts = map_solver.simulated_annealing()

    print("Beste inkleuring (kleur per regio):", best_coloring)
    print("Aantal conflicten (0 is perfect):", min_conflicts)