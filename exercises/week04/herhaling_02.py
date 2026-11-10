"""
Oefening: TSP met Simulated Annealing
======================================
"""

import math
import random

import numpy as np


class TSPSolver:
    def __init__(
        self,
        distance_matrix,
        initial_temperature=1000,
        cooling_rate=0.995,
        num_iterations=10000,
    ):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def total_distance(self, tour: list[int]) -> float:
        """Bereken de totale afstand van een tour, inclusief terugkeer
        naar de startstad.

        Args:
            tour: permutatie van steden (lijst van indices).

        Returns:
            De totale afstand: som van de afstanden tussen opeenvolgende
            steden, plus de afstand van de laatste stad terug naar de eerste.
        """
        # TODO
        distance = 0
        stops = len(tour)
        for i in range(stops):
            j = (i + 1) % (stops)
            stop1 = tour[i]
            stop2 = tour[j]
            distance += self.distance_matrix[stop1, stop2]
        return distance

    @staticmethod
    def _canonical(tour: list[int]) -> list[int]:
        """Draai de tour zodat stad 0 vooraan staat (richting blijft gelijk).

        De totale afstand is invariant onder rotatie, dus dit verandert niets
        aan de kwaliteit van de tour maar maakt het resultaat eenduidig.

        Args:
            tour: een geldige tour (permutatie van steden).

        Returns:
            Dezelfde tour als lijst, beginnend bij stad 0.
        """
        start = tour.index(0)
        return tour[start:] + tour[:start]

    def simulated_annealing(self) -> tuple[list[int], float]:
        """Simulated annealing voor TSP.

        Het algoritme start van de natuurlijke tour [0, 1, ..., n-1] en
        zoekt stap voor stap verbeteringen: elke iteratie worden twee
        willekeurige steden verwisseld. Een betere tour wordt altijd
        aanvaard; een slechtere tour wordt aanvaard met kans
        exp(-Δ / T), waarbij de temperatuur T exponential afkoelt.

        Returns:
            Een tuple (best_tour, best_distance): de beste gevonden tour
            (beginnend bij stad 0) en de bijhorende totale afstand.
        """
        # TODO
        indices = list(range(self.num_cities))
        current_tour = indices.copy()
        current_distance = self.total_distance(current_tour)
        best_tour = current_tour
        best_distance = current_distance

        T = self.initial_temperature

        for k in range(self.num_iterations):
            city1, city2 = random.sample(indices, 2)
            new_tour = current_tour.copy()
            new_tour[city1], new_tour[city2] = new_tour[city2], new_tour[city1]

            new_distance = self.total_distance(new_tour)
            delta = new_distance - current_distance

            if delta < 0:
                current_tour = new_tour
                current_distance = new_distance

            else:
                P = math.exp(-delta / T)
                if P > random.random():
                    current_tour = new_tour
                    current_distance = new_distance

            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance

            T *= self.cooling_rate

        return self._canonical(best_tour), best_distance


if __name__ == "__main__":
    distance_matrix = np.array(
        [[0, 29, 20, 21], [29, 0, 15, 18], [20, 15, 0, 25], [21, 18, 25, 0]]
    )

    tsp_solver = TSPSolver(distance_matrix)
    best_tour, best_distance = tsp_solver.simulated_annealing()

    print("Best Tour:", best_tour)
    print("Best Distance:", best_distance)
    print()

    european_cities = [
        "Paris",
        "Madrid",
        "Barcelona",
        "Berlin",
        "Rome",
        "Athens",
        "Lisbon",
        "Vienna",
        "Brussels",
        "Warsaw",
        "Budapest",
        "Stockholm",
        "Prague",
        "Helsinki",
        "Zürich",
        "Copenhagen",
        "Dublin",
        "Amsterdam",
        "Oslo",
        "Ljubljana",
    ]

    distance_array = [
        [
            0.0,
            1054.0,
            832.0,
            877.0,
            1106.0,
            2098.0,
            1453.0,
            1034.0,
            261.0,
            1366.0,
            1248.0,
            1546.0,
            885.0,
            1908.0,
            489.0,
            1026.0,
            777.0,
            428.0,
            1341.0,
            966.0,
        ],
        [
            1054.0,
            0.0,
            505.0,
            1869.0,
            1361.0,
            2368.0,
            503.0,
            1808.0,
            1315.0,
            2290.0,
            1976.0,
            2596.0,
            1774.0,
            2949.0,
            1247.0,
            2073.0,
            1451.0,
            1481.0,
            2389.0,
            1598.0,
        ],
        [
            832.0,
            505.0,
            0.0,
            1499.0,
            857.0,
            1877.0,
            1007.0,
            1348.0,
            1063.0,
            1863.0,
            1499.0,
            2281.0,
            1354.0,
            2603.0,
            836.0,
            1759.0,
            1470.0,
            1236.0,
            2143.0,
            1117.0,
        ],
        [
            877.0,
            1869.0,
            1499.0,
            0.0,
            1183.0,
            1803.0,
            2312.0,
            524.0,
            652.0,
            516.0,
            689.0,
            813.0,
            281.0,
            1105.0,
            668.0,
            355.0,
            1316.0,
            575.0,
            838.0,
            723.0,
        ],
        [
            1106.0,
            1361.0,
            857.0,
            1183.0,
            0.0,
            1052.0,
            1862.0,
            764.0,
            1172.0,
            1317.0,
            812.0,
            1979.0,
            923.0,
            2202.0,
            684.0,
            1532.0,
            1883.0,
            1294.0,
            2007.0,
            490.0,
        ],
        [
            2098.0,
            2368.0,
            1877.0,
            1803.0,
            1052.0,
            0.0,
            2852.0,
            1282.0,
            2089.0,
            1600.0,
            1123.0,
            2409.0,
            1533.0,
            2469.0,
            1617.0,
            2137.0,
            2853.0,
            2161.0,
            2605.0,
            1175.0,
        ],
        [
            1453.0,
            503.0,
            1007.0,
            2312.0,
            1862.0,
            2852.0,
            0.0,
            2298.0,
            1710.0,
            2759.0,
            2473.0,
            2991.0,
            2246.0,
            3360.0,
            1723.0,
            2477.0,
            1639.0,
            1862.0,
            2738.0,
            2097.0,
        ],
        [
            1034.0,
            1808.0,
            1348.0,
            524.0,
            764.0,
            1282.0,
            2298.0,
            0.0,
            915.0,
            557.0,
            217.0,
            1245.0,
            250.0,
            1440.0,
            590.0,
            871.0,
            1681.0,
            933.0,
            1352.0,
            276.0,
        ],
        [
            261.0,
            1315.0,
            1063.0,
            652.0,
            1172.0,
            2089.0,
            1710.0,
            915.0,
            0.0,
            1160.0,
            1132.0,
            1285.0,
            721.0,
            1649.0,
            491.0,
            767.0,
            773.0,
            173.0,
            1087.0,
            918.0,
        ],
        [
            1366.0,
            2290.0,
            1863.0,
            516.0,
            1317.0,
            1600.0,
            2759.0,
            557.0,
            1160.0,
            0.0,
            545.0,
            809.0,
            515.0,
            913.0,
            1042.0,
            670.0,
            1825.0,
            1091.0,
            1061.0,
            834.0,
        ],
        [
            1248.0,
            1976.0,
            1499.0,
            689.0,
            812.0,
            1123.0,
            2473.0,
            217.0,
            1132.0,
            545.0,
            0.0,
            1319.0,
            443.0,
            1459.0,
            791.0,
            1013.0,
            1896.0,
            1145.0,
            1482.0,
            383.0,
        ],
        [
            1546.0,
            2596.0,
            2281.0,
            813.0,
            1979.0,
            2409.0,
            2991.0,
            1245.0,
            1285.0,
            809.0,
            1319.0,
            0.0,
            1056.0,
            393.0,
            1470.0,
            524.0,
            1630.0,
            1128.0,
            417.0,
            1497.0,
        ],
        [
            885.0,
            1774.0,
            1354.0,
            281.0,
            923.0,
            1533.0,
            2246.0,
            250.0,
            721.0,
            515.0,
            443.0,
            1056.0,
            0.0,
            1301.0,
            527.0,
            635.0,
            1466.0,
            710.0,
            1118.0,
            447.0,
        ],
        [
            1908.0,
            2949.0,
            2603.0,
            1105.0,
            2202.0,
            2469.0,
            3360.0,
            1440.0,
            1649.0,
            913.0,
            1459.0,
            393.0,
            1301.0,
            0.0,
            1773.0,
            883.0,
            2023.0,
            1502.0,
            786.0,
            1712.0,
        ],
        [
            489.0,
            1247.0,
            836.0,
            668.0,
            684.0,
            1617.0,
            1723.0,
            590.0,
            491.0,
            1042.0,
            791.0,
            1470.0,
            527.0,
            1773.0,
            0.0,
            963.0,
            1237.0,
            610.0,
            1401.0,
            477.0,
        ],
        [
            1026.0,
            2073.0,
            1759.0,
            355.0,
            1532.0,
            2137.0,
            2477.0,
            871.0,
            767.0,
            670.0,
            1013.0,
            524.0,
            635.0,
            883.0,
            963.0,
            0.0,
            1238.0,
            621.0,
            483.0,
            1078.0,
        ],
        [
            777.0,
            1451.0,
            1470.0,
            1316.0,
            1883.0,
            2853.0,
            1639.0,
            1681.0,
            773.0,
            1825.0,
            1896.0,
            1630.0,
            1466.0,
            2023.0,
            1237.0,
            1238.0,
            0.0,
            757.0,
            1265.0,
            1689.0,
        ],
        [
            428.0,
            1481.0,
            1236.0,
            575.0,
            1294.0,
            2161.0,
            1862.0,
            933.0,
            173.0,
            1091.0,
            1145.0,
            1128.0,
            710.0,
            1502.0,
            610.0,
            621.0,
            757.0,
            0.0,
            914.0,
            986.0,
        ],
        [
            1341.0,
            2389.0,
            2143.0,
            838.0,
            2007.0,
            2605.0,
            2738.0,
            1352.0,
            1087.0,
            1061.0,
            1482.0,
            417.0,
            1118.0,
            786.0,
            1401.0,
            483.0,
            1265.0,
            914.0,
            0.0,
            1561.0,
        ],
        [
            966.0,
            1598.0,
            1117.0,
            723.0,
            490.0,
            1175.0,
            2097.0,
            276.0,
            918.0,
            834.0,
            383.0,
            1497.0,
            447.0,
            1712.0,
            477.0,
            1078.0,
            1689.0,
            986.0,
            1561.0,
            0.0,
        ],
    ]

    distance_matrix = np.array(distance_array)

    tsp_solver = TSPSolver(distance_matrix)
    best_tour, best_distance = tsp_solver.simulated_annealing()

    labeled_tour = [european_cities[index] for index in best_tour]
    
    print("Best Tour:", " -> ".join(labeled_tour))
    print("Best Distance:", best_distance)