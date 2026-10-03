"""
Oefening 3: Routeplanner (Utility-based Agent)
===============================================
Een utility-based agent maximaliseert een interne utility-functie.

Voor de route Antwerpen -> Parijs is een interessante utility:
    utility = -d(huidige stad, nieuwe stad)

De agent zoekt NIET (dit doen we in week 3): bij elke stap kiest hij greedy de
buur met de hoogste utility (kleinste afstand).
"""
from typing import Optional

CITIES = ["Antwerpen", "Brussel", "Gent", "Luik", "Doornik", "Reims", "Parijs"]

# Afstandsmatrix (onvolledig): wie met wie is er een weg?
ROADS: dict[tuple[str, str], float] = {
    ("Antwerpen", "Brussel"): 45,
    ("Antwerpen", "Gent"): 60,
    ("Brussel", "Luik"): 100,
    ("Brussel", "Gent"): 55,
    ("Brussel", "Doornik"): 90,
    ("Gent", "Doornik"): 65,
    ("Doornik", "Reims"): 130,
    ("Luik", "Reims"): 110,
    ("Reims", "Parijs"): 145,
    ("Gent", "Parijs"): 300,
}


def distance(a: str, b: str) -> Optional[float]:
    """Geef de afstand tussen twee steden, of None zonder weg."""
    if (a, b) in ROADS:
        return ROADS[(a, b)]
    if (b, a) in ROADS:
        return ROADS[(b, a)]
    return None


class RouteAgent:
    """Utility-based agent: kiest bij elke stap de dichtstbijzijnde buur."""

    def utility(self, from_city: str, to_city: str) -> float:
        """TODO: geef -d(from_city, to_city) terug."""
        return -distance(from_city, to_city)

    def neighbours(self, city: str) -> list[str]:
        """TODO: geef alle steden met een directe weg naar `city`."""
        neighbours = []
        for cities in ROADS:
            if city == cities[0]: neighbours.append(cities[1])
            if city == cities[1]: neighbours.append(cities[0])
        return neighbours

    def choose_next(self, current_city: str, visited: set[str]) -> Optional[str]:
        """TODO: kies onder de niet-bezochte buren de buur met de
        hoogste utility. Geen buren meer? -> None.
        """
        neighbouring_cities = set(self.neighbours(current_city))
        not_visited = neighbouring_cities - set(visited)
        if not_visited is None or len(not_visited) == 0: return None
        utilities = []
        for city in not_visited:
            util = self.utility(current_city, city)
            utilities.append([city, util])
        utilities = sorted(utilities, key=lambda x: x[1], reverse=True)
        return utilities[0][0]

    def plan_route(self, start_city: str, goal_city: str) -> list[str]:
        """TODO: bouw de route stad per stad via choose_next.

        Stop zodra de goal bereikt is of de agent vastzit.
        """
        cities = [start_city]
        current = start_city
        while current != goal_city:
            next_city = self.choose_next(current, set(cities))
            if next_city is None:
                break
            cities.append(next_city)
            current = next_city
        return cities


if __name__ == "__main__":
    agent = RouteAgent()
    route = agent.plan_route("Antwerpen", "Parijs")
    print("Route:", " -> ".join(route))

    totale_afstand = 0.0
    for a, b in zip(route, route[1:]):
        d = distance(a, b)
        if d is not None:
            totale_afstand += d
    print("Totale afstand:", totale_afstand, "km")

    # Vergelijk met wat we gaan doen in week 3: wat is de kortste route met de hand? (week 3: Dijkstra!)
