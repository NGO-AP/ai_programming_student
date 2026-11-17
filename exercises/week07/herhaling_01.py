"""
Oefening: TicTacToe met Minimax & Alpha-Beta
==============================================
"""
import copy
import random


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.computer_plays_random = False

    def possible_moves(self):
        """Geef lijst van (rij, kolom)-tupels van lege velden."""
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']

    def is_valid_move(self, x, y):
        return 0 <= x < len(self.board) and 0 <= y < len(self.board) and self.board[x][y] == ' '

    def make_move(self, x, y, player):
        self.board[x][y] = player

    def undo_move(self, x, y):
        self.board[x][y] = ' '

    def check_winner(self):
        positions = range(len(self.board))
        axes = [row for row in self.board]

        axes.append([self.board[i][i] for i in positions])
        axes.append([self.board[i][len(self.board)-i-1] for i in positions])

        cols = [[self.board[i][j] for j in positions] for i in positions]

        axes = axes + cols

        for ax in axes:
            if ax == ['X', 'X', 'X']: return 'X'
            if ax == ['O', 'O', 'O']: return 'O'

        return None

    def is_draw(self):
        return len(self.possible_moves()) == 0 and not self.check_winner()

    def minimax(self, depth, is_maximizing, alpha=None, beta=None, computer_is_random=False):
        if depth == 0: return 0
        if alpha is None: alpha = -float('inf')
        if beta is None: beta = float('inf')
        winner = self.check_winner()
        if winner == 'X': return 1
        if winner == 'O': return -1
        if self.is_draw(): return 0

        if is_maximizing and not computer_is_random:
            best = -float('inf')
            for r, c in self.possible_moves():
                self.make_move(r, c, 'X')
                best = max(best, self.minimax(depth=depth-1, is_maximizing=False, alpha=alpha, beta=beta, computer_is_random=True))
                self.undo_move(r, c)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        elif is_maximizing and computer_is_random:
            total_score = 0
            for r, c in self.possible_moves():
                self.make_move(r, c, 'X')
                total_score += self.minimax(depth=depth-1, is_maximizing=False, alpha=alpha, beta=beta, computer_is_random=False)
                self.undo_move(r, c)
            return total_score / len(self.possible_moves())
        else:
            best = float('inf')
            for r, c in self.possible_moves():
                self.make_move(r, c, 'O')
                best = min(best, self.minimax(depth=depth-1, is_maximizing=True, alpha=alpha, beta=beta, computer_is_random=computer_is_random))
                self.undo_move(r, c)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best


    def find_best_move(self):
        if self.computer_plays_random == True:
            moves = self.possible_moves()
            return random.choice(moves)
        else:
            best = -float('inf')
            best_move = None
            for r, c in self.possible_moves():
                self.make_move(r, c, 'X')
                score =  self.minimax(depth=9, is_maximizing=False, computer_is_random=True)
                self.undo_move(r, c)
                if score > best:
                    best = score
                    best_move = (r, c)
            return best_move

    
    def print_board(self):
        horizontal_line = "+---+---+---+"
        print(horizontal_line)
        for row in self.board:
            print("| {} | {} | {} |".format(row[0], row[1], row[2]))
            print(horizontal_line)

    def play(self):
        while True:
            self.print_board()
            r = int(input("Rij (0-2): "))
            c = int(input("Kolom (0-2): "))
            while not self.is_valid_move(r, c):
                print("Dat is geen geldige zet!")
                r = input("Rij (0-2): ")
                c = input("Kolom (0-2): ")
            self.make_move(r, c, 'O')
            winner = self.check_winner()
            if winner == 'X': 
                self.print_board()
                print("De computer heeft gewonnen :(.")
                break
            if winner == 'O': 
                self.print_board()
                print("Je bent gewonnen :).")
                break
            if self.is_draw(): 
                self.print_board()
                print("Gelijkspel.")
                break
            print("De computer denkt na...")
            r, c = self.find_best_move()
            self.make_move(r, c, 'X')
            self.computer_plays_random = not self.computer_plays_random
            winner = self.check_winner()
            if winner == 'X': 
                self.print_board()
                print("De computer heeft gewonnen :(.")
                break
            if winner == 'O': 
                self.print_board()
                print("Je bent gewonnen :).")
                break
            if self.is_draw(): 
                self.print_board()
                print("Gelijkspel.")
                break

if __name__ == "__main__":
    game = TicTacToe()
    game.play()