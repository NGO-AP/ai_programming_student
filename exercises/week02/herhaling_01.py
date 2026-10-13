"""
Oefening 1: Self-Driving Car (Model-based Reflex Agent)
========================================================
Implementeer een agent die zijn voorligger volgt.
"""


class LidarSensorInput:
    def __init__(self, distance=0.0):
        self.DistanceTo = distance


class Brake:
    def __str__(self):
        return "BRAKE"


class Nothing:
    def __str__(self):
        return "NOTHING"


class SelfDrivingCar:
    def __init__(self):
        # TODO: interne state — welke variabele heb je nodig?
        self.previous_distance = None

    def process(self, sensor_input):
        # TODO: bereken relatieve snelheid en tijd tot botsing; 
        #       rem als tijd < 5 seconden
        action = Nothing()
        if self.previous_distance is None:
            self.previous_distance = sensor_input.DistanceTo
            return action
        speed = self.previous_distance - sensor_input.DistanceTo
        if speed > 0:
            time = sensor_input.DistanceTo / speed
            if time < 5:
                action = Brake()
        self.previous_distance = sensor_input.DistanceTo
        return action


if __name__ == "__main__":
    sensor = LidarSensorInput(10)
    agent = SelfDrivingCar()

    for afstand in [10, 15, 13, 10, 8, 6, 4, 3]:
        sensor.DistanceTo = afstand
        action = agent.process(sensor)
        print(f"Afstand: {afstand}m -> {action}")
    print()

"""
Oefening 2: Foute sensor — Boeing 737 MAX (Model-based Reflex Agent)
=====================================================================
Een vliegtuig heeft twee hoogtemeters (redundantie). Eén sensor kan
stukgaan en onzin meten (denk aan de AoA-sensor van de Boeing 737 MAX).

De agent moet:
1. Beide sensoren lezen (sensors).
2. Beoordelen of ze het met elkaar eens zijn (plausibiliteitscheck).
3. Bij discrepantie vertrouwen op de sensor die consistent is met de
   vorige waarde (sensor model + interne state).
4. Als de betrouwbare hoogtemeter daalt: een correctie aanvragen
   (actuator).
"""
from typing import Optional


class Reading:
    """Eén meetslag van beide hoogtemeters."""

    def __init__(self, sensor_a, sensor_b):
        self.sensor_a = sensor_a
        self.sensor_b = sensor_b


class Correct:
    def __str__(self):
        return "CORRECTIE AANVRAGEN"


class Nothing:
    def __str__(self):
        return "NOTHING"


class FaultTolerantAgent:
    """Model-based reflex agent met redundante sensoren.

    Interne state:
    - vorige hoogte (voor de trend)
    - welke sensor verdacht is (None, 'a' of 'b')
    """

    TOLERANCE = 50.0  # meter; meer verschil = minstens één sensor is fout
    DESCENT_LIMIT = -10.0  # meter per meetslag; meer dalen = correctie

    def __init__(self):
        # TODO: interne state — welke variabelen heb je nodig?
        self.previous_height = None
        self.suspected_sensor = None

    def read_all(self, p: Reading) -> tuple[float, float]:
        """Sensors: geef beide metingen terug."""
        return p.sensor_a, p.sensor_b

    def reliable_value(self, a: float, b: float, previous: Optional[float]) -> float:
        """Sensor model: bepaal de meest betrouwbare hoogtemeting.

        Regels:
        - Verschil <= TOLERANCE -> gemiddelde is betrouwbaar.
        - Anders: kies de sensor die het dichtst bij de vorige waarde
          ligt (interne state!).
        - Is er geen vorige waarde (eerste meetslag)? -> kies
          bij voorkeur sensor a.
        """
        # TODO: implementeer dit
        if previous is None: return a
        if self.suspected_sensor == b: return a
        if self.suspected_sensor == a: return b
        delta = abs(a - b)
        if delta <= self.TOLERANCE: return (a + b) / 2
        if abs(previous - a) < abs(previous - b): 
            self.suspected_sensor = 'b'
            return a
        self.suspected_sensor = 'a'
        return b

    def process(self, p: Reading):
        # TODO: kies de betrouwbare meting, bepaal de trend (delta t.o.v.
        #       de vorige waarde) en vraag correctie aan als de daling
        #       sneller is dan DESCENT_LIMIT. Vergeet de interne state
        #       niet bij te werken.
        action = Nothing()
        a,b = self.read_all(p)
        value = self.reliable_value(a, b, self.previous_height)
        if self.previous_height is not None and value - self.previous_height < self.DESCENT_LIMIT:
            action = Correct()
        self.previous_height = value
        return action


if __name__ == "__main__":
    # Vluchtprofiel: klim, cruise, daal. Sensor A valt uit bij stap 4.
    vlucht = [
        Reading(1000, 1000),   # beide ok
        Reading(1020, 1025),   # beide ok, stijgende trend
        Reading(1050, 1048),   # beide ok
        Reading(1055, 600),    # sensor B stuk (of is het A?)
        Reading(1040, 100),    # sensor B blijft onzin
        Reading(1020, 50),     # daling wordt nu zichtbaar via A
        Reading(1000, 30),     # dalende trend -> correctie nodig
    ]

    agent = FaultTolerantAgent()
    for i, p in enumerate(vlucht, start=1):
        actie = agent.process(p)
        print(f"Stap {i}: a={p.sensor_a:6.0f} b={p.sensor_b:6.0f} -> {actie}")
    print()

    # Verwacht: vanaf stap 4 vertrouwt de agent sensor A, en vanaf
    # stap 6-7 vraagt hij een correctie aan.

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
        # nodes = []
        # for (current, neighbour) in ROADS:
        #     if current == city: nodes.append(neighbour)
        #     if neighbour == city: nodes.append(current)
        return [neighbour for (current, neighbour) in ROADS if current == city]

    def choose_next(self, current_city: str, visited: set[str]) -> Optional[str]:
        """TODO: kies onder de niet-bezochte buren de buur met de
        hoogste utility. Geen buren meer? -> None.
        """
        utilities = {}
        nodes = self.neighbours(current_city)
        if not nodes: return None
        for neighbour in nodes:
            if neighbour not in visited:
                utilities[neighbour] = self.utility(current_city, neighbour)
        if not utilities: return None
        sorted_neighbours = sorted(utilities.items(), key=lambda x:x[1], reverse=True)
        return sorted_neighbours[0][0]

    def plan_route(self, start_city: str, goal_city: str) -> list[str]:
        """TODO: bouw de route stad per stad via choose_next.

        Stop zodra de goal bereikt is of de agent vastzit.
        """
        route = [start_city]
        visited = set(route)
        current = start_city
        next = self.choose_next(current, visited)
        while next is not None and next != goal_city:
            route.append(next)
            current = next
            visited.add(current)
            next = self.choose_next(current, visited)
        if next == goal_city:
            route.append(goal_city)
        else:
            route.append(f"vastgelopen in {current}!")
        return route


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
