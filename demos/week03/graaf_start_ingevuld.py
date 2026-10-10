"""De volledige stedengraaf van Antwerpen naar Parijs (startversie).

Volgt de structuur uit course-text/03_zoekalgoritmes.md: states zijn
`State`-objecten, zoekoperaties werken op `Node`-objecten met acties.
Vul zelf de functies bouw_nodes, reconstruct_pad, breadth_first_search
en depth_first_search in.
"""

from collections import deque

STEDEN_GRAAF = {
    "Antwerpen": ["Breda", "Eindhoven", "Gent"],
    "Breda": ["Antwerpen", "Rotterdam", "Eindhoven"],
    "Eindhoven": ["Antwerpen", "Breda"],
    "Rotterdam": ["Breda"],
    "Gent": ["Antwerpen", "Brugge", "Kortrijk", "Brussel"],
    "Brugge": ["Gent", "Kortrijk"],
    "Kortrijk": ["Gent", "Brugge", "Lille"],
    "Brussel": ["Gent", "Charleroi", "Namen"],
    "Charleroi": ["Brussel", "Namen"],
    "Namen": ["Brussel", "Charleroi", "Luxemburg"],
    "Luxemburg": ["Namen", "Metz"],
    "Lille": ["Kortrijk", "Arras"],
    "Arras": ["Lille", "Amiens"],
    "Amiens": ["Arras", "Saint-Quentin", "Rouen", "Beauvais"],
    "Saint-Quentin": ["Amiens", "Laon"],
    "Laon": ["Saint-Quentin", "Reims", "Soissons"],
    "Reims": ["Laon", "Metz"],
    "Soissons": ["Laon", "Compiegne"],
    "Rouen": ["Amiens"],
    "Beauvais": ["Amiens", "Compiegne", "Saint-Denis"],
    "Compiegne": ["Beauvais", "Soissons", "Saint-Denis"],
    "Saint-Denis": ["Compiegne", "Beauvais", "Parijs"],
    "Metz": ["Luxemburg", "Reims", "Dijon"],
    "Dijon": ["Metz", "Parijs"],
    "Parijs": ["Saint-Denis", "Versailles", "Orleans", "Dijon"],
    "Versailles": ["Parijs", "Le Mans"],
    "Orleans": ["Parijs", "Le Mans"],
    "Le Mans": ["Versailles", "Orleans"],
}

START = "Antwerpen"
DOEL = "Parijs"


class State:
    """Een state in de state space (hier: een stad)."""

    def __init__(self, name: str) -> None:
        self.name = name


class Node:
    """Een node in de search tree: een state plus zijn acties."""

    def __init__(self, state: State, parent: "Node | None" = None) -> None:
        self.state = state
        self.actions: list[Node] = [] # buren van een node in een graaf
        # Extra t.o.v. de cursustekst: parent-verwijzing om het pad te reconstrueren
        self.parent = parent

    def add_action(self, action: "Node") -> None:
        self.actions.append(action)

# Deze code snippet creëert nodes en maakt het gewoon eenvoudiger om te werken
def bouw_nodes(graaf: dict[str, list[str]]) -> dict[str, Node]:
    """Vertaal de adjacency-dict naar Node-objecten met acties."""
    nodes =  {stad: Node(State(stad)) for stad in graaf}
    for stad, buurnodes in graaf.items():
        # Buren toevoegen
        for buur in buurnodes:
            nodes[stad].add_action(nodes[buur])
    return nodes


def reconstruct_pad(node: Node) -> list[str]:
    """Bouw het gevonden pad op via de parent-verwijzingen."""
    pad = []

    while node is not None:
        pad.append(node.state.name)
        node = node.parent

    return pad


def breadth_first_search(
    graaf: dict[str, list[str]], start: str, doel: str, verbose: bool = False
) -> list[str] | None:
    """BFS volgens de cursustekst: openklappen niveau per niveau via een FIFO-queue.
    Vindt het pad met het minste aantal steden.
    """
    nodes = bouw_nodes(graaf)
    initial_node = nodes[start] # de NODE Antwerpen
    goal_node = nodes[doel] # de NODE Parijs

    frontier = deque([initial_node])
    visited = set([initial_node])
    niveau = 0 # geen functie, maar handig voor debugging

    while frontier: # zolang de frontier niet leeg is, doe...

        # welke node ?
        node = frontier.popleft() # Eerste node uit queue vastnemen en verwijderen uit lijst

        # check of dit de oplossing is
        if node.state.name == goal_node.state.name:
            return reconstruct_pad(node) # we zijn klaar

        # we zijn nog niet in Parijs als we op dit punt in de code komen
        visited.add(node)

        # node openklappen
        for neighbour in node.actions: # voor elk van de buren
            if (neighbour not in visited):
                frontier.append(neighbour)
                if (neighbour.parent is None):
                    neighbour.parent = node

    # wat gebeurt er hier ? 
    return None # je komt hier terecht als er geen oplossing is en alle mogelijkheden zijn uitgeput

def depth_first_search(
    graaf: dict[str, list[str]], start: str, doel: str, verbose: bool = False
) -> list[str] | None:
    """DFS volgens de cursustekst: recursief, eerst zoeken in de diepte.
    Vindt snel een pad, maar niet noodzakelijk het kortste.
    """
    pass


def naar_mermaid(graaf):
    """Exporteer de graaf als mermaid flowchart (elke rand één keer)."""
    regels = ["flowchart LR"]
    gezien = set()
    for stad, verbindingen in graaf.items():
        for buur in verbindingen:
            rand = frozenset({stad, buur})
            if rand not in gezien:
                gezien.add(rand)
                regels.append(f"    {stad} --- {buur}")
    return "\n".join(regels)
