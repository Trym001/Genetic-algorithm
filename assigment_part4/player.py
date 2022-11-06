import math
import random
import sys

import numpy as np


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class GeneticAlgorithm(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = self.ga_main(game)
        return square

    @staticmethod
    def generate_population():
        game_plan = []
        possible_moves = [0,1,2,3,4,5,6,7,8]
        # prepare move-list for simulation
        for i in range(9):
            game_plan.append(random.choice(possible_moves))
            possible_moves.remove(game_plan[i])
        return game_plan

    @staticmethod
    def fitness(state, player, other_player):
        if state.current_winner == player['letter']:
            player['score'] = 1 * state.num_empty_squares()
            other_player['score'] = -1 * state.num_empty_squares()
            return player['score'], other_player['score']

        elif state.current_winner == other_player['letter']:
            player['score'] = -1 * state.num_empty_squares()
            other_player['score'] = 1 * state.num_empty_squares()
            return player['score'], other_player['score']

        elif not state.empty_squares():
            player['score'] = 0
            other_player['score'] = 0
            return player['score'], other_player['score']

    def simulation(self, state, player, other_player):    # Simulate the whole game for two individuals in population
        mutation = {'X': {'new_game_plan': [], 'index': []}, 'O': {'new_game_plan': [], 'index': []}}
        for i in range(len(player['game_plan'])):
            for s in range(2):
                if s % 2 == 0:
                    # X player
                    player_chosen_square = player['game_plan'][i]

                    if player_chosen_square not in state.available_moves():
                        player_chosen_square = self.mutate(state.available_moves())
                        mutation['X']['index'].append(i)
                        mutation['X']['new_game_plan'].append(player_chosen_square)

                    state.make_move(player_chosen_square, player['letter'])
                    player['game_plan'].pop(i)

                else:
                    # O player
                    other_player_chosen_square = other_player['game_plan'][i]

                    if other_player_chosen_square not in state.available_moves():
                        other_player_chosen_square = self.mutate(state.available_moves())
                        mutation['O']['index'].append(i)
                        mutation['O']['new_game_plan'].append(other_player_chosen_square)

                    state.make_move(other_player_chosen_square, other_player['letter'])
                    other_player['game_plan'].pop(i)

                if state.current_winner != None or not state.empty_squares():    # Check if x win
                    score1, score2 = self.fitness(state, player, other_player)
                    return mutation, score1, score2

    # got some help from the interwebs:
    # https://medium.com/@samiran.bera/crossover-operator-the-heart-of-genetic-algorithm-6c0fdcb405c0
    @staticmethod
    def uniform_crossover(a, b, p):
        for i in range(len(p)):
            if p[i] < 0.5:
                temp = a[i]
                a[i] = b[i]
                b[i] = temp
        return a, b

    @staticmethod
    def mutate(available_moves):
        return random.choice(available_moves)

    def ga_main(self, state):
        population = []
        # initial population
        for i in range(1000):
            population.append(self.generate_population())

        n_population = len(population)

        # generations
        for gen in range(500):
            print(f"Gen: {gen}")
            ranked_population = []
            for s in range(len(population)-1):  # game simulation
                mutated, score1, score2 = self.simulation(
                    state,
                    {'letter': 'X', 'game_plan': population[s].copy(), 'score': None},
                    {'letter': 'O', 'game_plan': population[s+1].copy(), 'score': None}
                )

                counter = 0
                for mutation in mutated['X']['index']:
                    population[s][mutation] = mutated['X']['new_game_plan'][counter]
                    counter += 1
                counter = 0
                for mutation in mutated['O']['index']:
                    population[s+1][mutation] = mutated['O']['new_game_plan'][counter]
                    counter += 1

                for j in [score1, score2]:
                    ranked_population.append((j, population[s])) \
                        if j == score1 else ranked_population.append((j, population[s+1]))
                for clear_board in range(9):
                    state.board[clear_board] = ' '
                state.current_winner = None
                s += 1  # each individual only plays one time.

            ranked_population.sort(key=lambda x: x[0], reverse=True)
            ranked_population = ranked_population[:n_population]

            new_gen = []
            for s in range(len(ranked_population)-1):
                new_gen1, new_gen2 = self.uniform_crossover(
                    ranked_population[s][1],
                    ranked_population[s + 1][1],
                    np.random.rand(len(ranked_population[s][1]))
                )
                for choice in [new_gen1, new_gen2]:
                    new_gen.append(choice)
                s += 1
            population = new_gen[:n_population]
