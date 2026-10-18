"""
Oefening 1: Insertion Sort
===========================
Implementeer insertion sort volgens het stappenplan in opgave_week1.md.
"""


def insertion_sort(sequence):
    """
    Sorteer een lijst van klein naar groot met behulp van insertion sort.

    Parameters:
        sequence (list): De lijst om te sorteren.

    Returns:
        list: De gesorteerde lijst.
    """
    # TODO: implementeer insertion sort
    ordered = sequence[:]
    for i in range(1, len(ordered)):
        key = ordered[i]
        j = i - 1
        while j >= 0 and ordered[j] > key:
            ordered[j+1] = ordered[j]
            j -= 1
        ordered[j+1] = key
    return ordered


if __name__ == "__main__":
    # Test je implementatie met deze voorbeelden
    test_lijsten = [
        [],
        [42],
        [1, 2, 3, 4],
        [5, 4, 3, 2, 1],
        [3, 1, 2, 1, 3],
        [5, 2, 4, 6, 1, 3],
    ]

    for lijst in test_lijsten:
        origineel = lijst.copy()
        gesorteerd = insertion_sort(lijst)
        print(f"Origineel: {origineel} -> Gesorteerd: {gesorteerd}")

    # Stap 5 (uitbreiding): vergelijk met bubble sort en merge sort
    # Kopieer bubble_sort en merge_sort uit de cursus en test hier:
    # import random
    # import time
    # ...

"""
Oefening 2: Floor Cleaning Agent (Model-based Reflex Agent)
=============================================================
Implementeer een model-based reflex agent voor een robotstofzuiger.
Volg het stappenplan in opgave_week1.md.
"""


class FloorCleaningAgent:
    """
    Een model-based reflex agent die een kamer proper maakt.

    De kamer is een grid van `rows` × `cols` tegels.
    De robot start in de linkerbovenhoek (rij 0, kolom 0).
    """

    def __init__(self, rows=5, cols=10):
        """
        Initialiseer de robot met een lege kamer van `rows` × `cols`.

        Tip: gebruik een 2D-lijst om de status van elke tegel bij te houden.
        """
        self.rows = rows
        self.cols = cols

        # TODO: interne state initialiseren
        # - huidige positie (rij, kolom)
        # - grid met proper/vuil status per tegel (bv. True = proper, False = vuil)

        self.row = 0  # startrij (bovenaan)
        self.col = 0  # startkolom (links)

        # Voorbeeld: grid aanmaken (alle tegels beginnen vuil)
        # self.grid = [[False for _ in range(cols)] for _ in range(rows)]
        self.grid = [[False for _ in range(cols)] for _ in range(rows)]

    # ---------- Basisbewegingen ----------

    def move_up(self):
        """Verplaats de robot één tegel omhoog (rij -1)."""
        if self.row > 0:
            self.row -= 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet omhoog: rand bereikt")

    def move_down(self):
        """Verplaats de robot één tegel omlaag (rij +1)."""
        # TODO: implementeer
        if self.row < self.rows-1:
            self.row += 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet omlaag: rand bereikt")

    def move_left(self):
        """Verplaats de robot één tegel naar links (kolom -1)."""
        # TODO: implementeer
        if self.col > 0:
            self.col -= 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet naar links: rand bereikt")

    def move_right(self):
        """Verplaats de robot één tegel naar rechts (kolom +1)."""
        # TODO: implementeer
        if self.col < self.cols-1:
            self.col += 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet naar rechts: rand bereikt")

    # ---------- Stofzuigen ----------

    def clean_tile(self):
        """Stofzuig de huidige tegel (maak hem proper)."""
        # TODO: markeer huidige tegel als proper
        # print(f"Tegel ({self.row}, {self.col}) is nu proper!")
        self.grid[self.row][self.col] = True
        print(f"Tegel ({self.row}, {self.col}) is nu proper!")

    # ---------- Strategie ----------

    def clean_room(self):
        """
        Laat de robot de volledige kamer proper maken.
        Gebruik een systematische strategie (bv. zigzag-patroon).
        """
        # TODO: implementeer een strategie
        # Tip: je kan een move_to(row, col) hulpmethode gebruiken
        self.move_to(0,0)
        self.clean_tile()
        for r in range(self.rows):
            self.move_to(r, self.col)
            if self.col == 0:
                self.move_to(r, self.cols-1)
                continue
            if self.col == self.cols-1:
                self.move_to(r, 0)


    # ---------- Helper om naar een specifieke tegel te gaan ----------

    def move_to(self, target_row, target_col):
        """
        Verplaats de robot van huidige positie naar (target_row, target_col).
        Gebruik de basisbewegingen move_up/down/left/right.
        """
        # TODO: implementeer
        # Beweeg eerst verticaal, dan horizontaal (of omgekeerd)
        if self.row < target_row:
            while self.row != target_row:
                self.move_down()
                self.clean_tile()
        if self.row > target_row:
            while self.row != target_row:
                self.move_up()
                self.clean_tile()
        if self.col < target_col:
            while self.col != target_col: 
                self.move_right()
                self.clean_tile()
        if self.col > target_col:
            while self.col != target_col:
                self.move_left()
                self.clean_tile()


    # ---------- Weergave ----------

    def print_status(self):
        """Toon de huidige status van de kamer."""
        print("\nKamer status (V = vuil, P = proper, R = robot):")
        for r in range(self.rows):
            rij_str = ""
            for c in range(self.cols):
                if r == self.row and c == self.col:
                    rij_str += " R "
                else:
                    # TODO: toon 'V' of 'P' op basis van interne grid
                    rij_str += ' V ' if not self.grid[r][c] else ' P '
            print(rij_str)
        print()


if __name__ == "__main__":
    # Test je agent
    robot = FloorCleaningAgent()

    print("Beginstatus:")
    robot.print_status()

    # TODO: roep clean_room() aan
    robot.clean_room()

    print("Eindstatus:")
    robot.print_status()