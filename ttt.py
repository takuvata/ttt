#!/bin/python3

class Player:
    def __init__(self, character, human = True):
        self.character = character
        self.score = {}
        self.human = human

    def reset_score(self, board):
        self.score = {'h': [], 'v': [], 'd': [0, 0]}
        for idx in range(board.size):
            self.score['h'].append(0)
            self.score['v'].append(0)

    def count_score(self, board):
        self.reset_score(board)
        for y, row in enumerate(board.grid):
            for x, field in enumerate(row):
                if field == self.character:
                    self.score['h'][y] += 1
                    self.score['v'][x] += 1
                    if (x + y) % 2 == 0:
                        if x == y:
                            self.score['d'][0] += 1
                        if x + y == board.size:
                            self.score['d'][1] += 1

    def make_move(self, game):
        move = Move(game = game, player = self)
        if self.human:
            move.read()
        else:
            move.generate()

class Board:
    def __init__(self, size = 3, char = '#'):
        self.size = size
        self.char = char
        self.grid = []
        for y in range(size):
            row = []
            for x in range(size):
                row.append(char)
            self.grid.append(row)

    def display(self):
        for row in self.grid:
            for field in row:
                print(field, end='')
            print()

    def mark_field(self, move):
        self.grid[move.y][move.x] = move.player.character

class Move:
    def __init__(self, game, player, x = -1, y = -1):
        self.x = x
        self.y = y
        self.game = game
        self.player = player

    def read(self):
        valid = False
        while not valid:
            self.x = int(input('X: '))
            self.y = int(input('Y: '))
            valid = self.validate(self.game.board)
        game.board.mark_field(self)

    def generate(self):
        print("Player " + self.player.character + " smokes dope")

    def validate(self, board):
        if self.x < 0 or self.x > 2:
            print("Invalid X")
            return False
        if self.y < 0 or self.y > 2:
            print("Invalid Y")
            return False
        if board.grid[self.x][self.y] != board.char:
            print("Invalid position")
            return False
        return True

class Game:
    def __init__(self, board, players = [], winner = None):
        self.players = players
        self.winner = winner
        self.board = board

    def get_winner(self, winning_score = 3):
        for player in self.players:
            player.count_score(self.board)
        for player in self.players:
            for track, scores in player.score.items():
                for score in scores:
                    if score == winning_score:
                        self.winner = player
                        break

if __name__ == "__main__":
    turn = 0
    game = Game(
            players = [Player(character = '+'), Player(character = 'o', human = False)],
            board = Board()
            )
    game.board.display()

while game.winner is None:
    game.players[turn % len(game.players)].make_move(game)
    game.get_winner()
    game.board.display()
    turn += 1

print("Player '" + game.winner.character + "' wins!")
