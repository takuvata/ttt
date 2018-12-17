#!/bin/python3

from random import randint

class Player:
    def __init__(self, game, character, human = True):
        self.character = character
        self.game = game
        self.human = human
        self.score = {}
        self.reset_score()
        self.move = Move(player = self)

    def reset_score(self):
        self.score = {'h': [], 'v': [], 'd': [0, 0]}
        for idx in range(self.game.board.size):
            self.score['h'].append(0)
            self.score['v'].append(0)

    def count_score(self):
        self.reset_score()
        for y, row in enumerate(self.game.board.grid):
            for x, field in enumerate(row):
                if field == self.character:
                    self.score['h'][y] += 1
                    self.score['v'][x] += 1
                    if (x + y) % 2 == 0:
                        if x == y:
                            self.score['d'][0] += 1
                        if x + y == (self.game.board.size - 1):
                            self.score['d'][1] += 1

    def make_move(self):
        if self.human:
            self.move.read()
        else:
            self.move.generate()
        self.game.turn += 1

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
        print()

    def mark_field(self, move):
        self.grid[move.y][move.x] = move.player.character

class Move:
    def __init__(self, player, x = -1, y = -1):
        self.x = x
        self.y = y
        self.player = player

    def read(self):
        valid = False
        while not valid:
            self.x = int(input('X: '))
            self.y = int(input('Y: '))
            valid = self.validate(self.player.game.board)
        self.player.game.board.mark_field(self)

    def find_winning_track(self, player):
        for direction, scores in player.score.items():
            for track, score in enumerate(scores):
                if score == (self.player.game.board.size - 1):
                    for contender in self.player.game.players:
                        if contender.character != player.character:
                            if contender.score[direction][track] == 0:
                                return {direction: [track]}
        return None

    def find_lowest_scoring(self):
        lowest = self.player.game.board.size - 1
        tracks = {'h':[], 'v': [], 'd': []}
        for player in self.player.game.players:
            for direction, scores in player.score.items():
                for track, score in enumerate(scores):
                    if score <= lowest:
                        lowest = score
        for player in self.player.game.players:
            for direction, scores in player.score.items():
                for track, score in enumerate(scores):
                    if score == lowest:
                        if player.character != self.player.character:
                            tracks[direction].append(track)
        return tracks


    def position_scores(self, tracks):
        position_scores = []
        for y in range(self.player.game.board.size):
            row = []
            for x in range(self.player.game.board.size):
                row.append(0)
            position_scores.append(row)
        for y, row in enumerate(self.player.game.board.grid):
            for x, field in enumerate(row):
                if field == self.player.game.board.char:
                    for direction, track in tracks.items():
                        if direction == 'v':
                            if x in tracks['v']:
                                 position_scores[x][y] += 1
                        if direction == 'h':
                            if y in tracks['h']:
                                position_scores[x][y] += 1
                        if direction == 'd':
                            if (x + y) % 2 == 0:
                                if x == y:
                                    if 0 in tracks['d']:
                                        position_scores[x][y] += 1
                                if x + y == (self.player.game.board.size - 1):
                                    if 1 in tracks['d']:
                                        position_scores[x][y] += 1
        return position_scores

    def best_position(self, scores):
        high = 0
        for x, row in enumerate(scores):
            for y, score in enumerate(row):
                if score >= high:
                    high = score
        if high == 0:
            print("Player '" + self.player.character + "' refuses to play")
            exit(0)
        for x, row in enumerate(scores):
            for y, score in enumerate(row):
                if score == high:
                    self.x = x
                    self.y = y
                    break

    def generate(self):
        # Priority - winning move
        tracks = self.find_winning_track(self.player)
        # Priority - prevent winning move
        if tracks is None:
            for player in self.player.game.players:
                tracks = self.find_winning_track(player)
                if tracks is not None:
                    break
        # Priority - lowest scoring tracks
        if tracks is None:
            tracks = self.find_lowest_scoring()
        scores = self.position_scores(tracks)
        self.best_position(scores)
        self.player.game.board.mark_field(self)

    def validate(self, board):
        if self.x < 0 or self.x >= board.size:
            print("Invalid X")
            return False
        if self.y < 0 or self.y >= board.size:
            print("Invalid Y")
            return False
        if board.grid[self.y][self.x] != board.char:
            print("Invalid position")
            return False
        return True

class Game:
    def __init__(self, board = Board(), starting_number = 0):
        self.winner = None
        self.board = board
        self.turn = 0
        self.starting_number = starting_number
        self.players = [
                Player(game = self, character = '+'),
                Player(game = self, character = 'o', human = False)
                ]
        self.current_player = self.players[starting_number]

    def get_winner(self):
        for player in self.players:
            player.count_score()
        for player in self.players:
            for track, scores in player.score.items():
                for score in scores:
                    if score == self.board.size:
                        self.winner = player
                        break

    def play(self):
        print("X - horizontal position, Y - vertical position, top left corner is postion X = 0, Y = 0.")
        self.board.display()
        while self.winner is None:
            self.current_player = self.players[(self.starting_number + self.turn) % len(self.players)]
            self.current_player.make_move()
            self.get_winner()
            self.board.display()
        print("Player '" + self.winner.character + "' wins!")



if __name__ == "__main__":
    game = Game()
    game.starting_number = randint(0, len(game.players))
    game.play()
