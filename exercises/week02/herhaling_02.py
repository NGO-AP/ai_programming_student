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
        current_distance = sensor_input.DistanceTo
        if self.previous_distance is not None:
            speed = self.previous_distance - current_distance
            if speed > 0:
                time_until_collision = current_distance / speed
                if time_until_collision < 5:
                    action = Brake()
        self.previous_distance = current_distance
        return action


if __name__ == "__main__":
    sensor = LidarSensorInput(10)
    agent = SelfDrivingCar()

    for afstand in [10, 15, 13, 10, 8, 6, 4, 3]:
        sensor.DistanceTo = afstand
        action = agent.process(sensor)
        print(f"Afstand: {afstand}m -> {action}")


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

# PEAS:
# Performance: Defecte sensoren als verdacht aanduiden bij een verschil van meer dan 50m tussen sensormetingen en de hoogte corrigeren indien er zich een daling voordoet van meer dan 10 m tussen 2 metingen.
# Environment: het luchtruim
# Actuators: aansturen motoren en vleugelflappen
# Sensors: sensoren voor hoogtemetingen


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
        if self.suspected_sensor == 'a': return b
        if self.suspected_sensor == 'b' or self.previous_height is None: return a
        if abs(a-b) <= self.TOLERANCE:
            return (a+b)/2
        if abs(self.previous_height - a) < abs(self.previous_height - b):
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
        a, b = p.sensor_a, p.sensor_b
        current_height = self.reliable_value(a,b,self.previous_height)
        if self.previous_height is not None and current_height - self.previous_height < self.DESCENT_LIMIT:
            action = Correct()
        self.previous_height = current_height
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

    # Verwacht: vanaf stap 4 vertrouwt de agent sensor A, en vanaf
    # stap 6-7 vraagt hij een correctie aan.

    # Eigen reflectie:
    # Een simple reflex agent is hier gevaarlijk omdat er dan geen rekening gehouden wordt met een historiek van inputs, waardoor een defecte sensor niet kan worden gedetecteerd. Daarnaast is er gewoon een interne state nodig om te bepalen of de daling te groot is en er een correctie nodig is.
    # Dit is een model based reflex agent.


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

    def find_neighbours(self, city: str) -> list[str]:
        """TODO: geef alle steden met een directe weg naar `city`."""
        neighbours = []
        for route in ROADS:
            a, b = route
            if a == city and b not in neighbours: neighbours.append(b)
            if b == city and a not in neighbours: neighbours.append(a)
        return neighbours

    def choose_next(self, current_city: str, visited: set[str]) -> Optional[str]:
        """TODO: kies onder de niet-bezochte buren de buur met de
        hoogste utility. Geen buren meer? -> None.
        """
        utilities = {}
        neighbours = self.find_neighbours(current_city)
        for neighbour in neighbours:
            if neighbour not in visited:
                utilities[neighbour] = self.utility(current_city, neighbour)
        if not utilities: return None
        utilities_sorted = sorted(utilities.items(), key= lambda x: x[1], reverse=True)
        return utilities_sorted[0][0]

    def plan_route(self, start_city: str, goal_city: str) -> list[str]:
        """TODO: bouw de route stad per stad via choose_next.

        Stop zodra de goal bereikt is of de agent vastzit.
        """
        route = [start_city]
        visited = set(route)
        next_city = self.choose_next(start_city, visited)
        while next_city is not None and next_city != goal_city:
            route.append(next_city)
            visited.add(next_city)
            next_city = self.choose_next(next_city, visited)
        if next_city is None: 
            route.append("Einddoel niet gevonden!")
            return route
        route.append(next_city)
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

    # Eigen reflectie
    # Dit is een utility-agent. De agent zoekt geen globaal pad, maar zoekt telkens de beste tussenstap aan de hand van de utiliy-functie die hij probeert te maximaliseren. Het probleem is wel dat hij greedy is. Hij kiest altijd de stad met de hoogste utility, maar loopt daarom vast in Luik. Er zijn steden met een rechtstreekse verbinding naar Parijs, maar deze heeft dan een grotere utility waardoor dit pad nooit gekozen wordt en de agent uiteindelijk vastloopt doordat hij niet mag terugkeren naar steden die al bezocht zijn.
    # Een goal-based agent zou niet naar de kortste tussenstappen tussen steden zoeken, maar naar de kortste totale route tot parijs.
    # Dit is geen vervanging voor Dijkstra, omdat bij Dijkstra een ander pad wordt geprobeert als het algoritme vastloopt.
