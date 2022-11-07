import math
import sys
import time

import numpy as np

from player import GeneticAlgorithm


class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]


def play(game, x_player, o_player, print_game=True):

    if print_game:
        game.print_board_nums()

    population = []
    # initial population
    for i in range(1000):
        population.append(x_player.generate_population())

    n_population = len(population)

    # generations
    for gen in range(500):
        ranked_population = []
        for s in range(len(population) - 1):  # game simulation
            mutated, score1, score2 = x_player.simulation(
                game,
                {'letter': 'X', 'game_plan': population[s].copy(), 'score': None},
                {'letter': 'O', 'game_plan': population[s + 1].copy(), 'score': None}
            )

            counter = 0
            for mutation in mutated['X']['index']:
                population[s][mutation] = mutated['X']['new_game_plan'][counter]
                counter += 1
            counter = 0
            for mutation in mutated['O']['index']:
                population[s + 1][mutation] = mutated['O']['new_game_plan'][counter]
                counter += 1

            for j in [score1, score2]:
                ranked_population.append((j, population[s])) \
                    if j == score1 else ranked_population.append((j, population[s + 1]))

            if gen == 499:
                print(f"==Game nr {s} and {s + 1}==")
                game.print_board()

            for clear_board in range(9):
                game.board[clear_board] = ' '
            game.current_winner = None
            s += 1  # each individual only plays one time.

        ranked_population.sort(key=lambda x: x[0], reverse=True)
        ranked_population = ranked_population[:n_population]

        new_gen = []
        for s in range(len(ranked_population) - 1):
            new_gen1, new_gen2 = x_player.uniform_crossover(
                ranked_population[s][1],
                ranked_population[s + 1][1],
                np.random.rand(len(ranked_population[s][1]))
            )
            for choice in [new_gen1, new_gen2]:
                new_gen.append(choice)
            s += 1
        population = new_gen[:n_population]
        print(f" ===Gen: {gen} ===\n=== Best score: {ranked_population[0][0]} ===\n")
        theChosenOne = [population[0], population[1]]

        if gen == 499:
            for result in range(0, 9):
                if result%2 == 0:
                    game.make_move(theChosenOne[0][result], 'X')
                    game.print_board()
                    print()
                    time.sleep(0.8)

                else:
                    game.make_move(theChosenOne[1][result], 'O')
                    game.print_board()
                    print()
                    time.sleep(0.8)


    sys.exit(0)


if __name__ == '__main__':
    x_player = GeneticAlgorithm('X')
    o_player = GeneticAlgorithm('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
