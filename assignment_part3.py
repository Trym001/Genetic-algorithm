import string
import random
import sys

import numpy as np

letters = list(string.ascii_lowercase)
letters.append(' ')
letters.reverse()

solutionName = input("Please enter your name in lower-cases only sir/ma'am\nhere:\t")
solutionName = str(solutionName.lower())

if set(solutionName).difference(letters):
    raise Exception("Sorry, no special characters >_<")

listSolutionName = list(solutionName)
lenOfName = len(solutionName)
population = []


def matching_char_in_sequence(my_name, random_name):
    matching_char_index = []

    for i in range(lenOfName):
        if my_name[i] == random_name[i]:
            matching_char_index.append(i)

    return matching_char_index


def gen_population():
    res_name = random.choices(letters, k=lenOfName)
    return res_name


def fitness(num_char_seq: int, len_of_string: int):
    score = num_char_seq / len_of_string
    return score


def uniform_crossover(a: str, b: str, p):
    a = list(a)
    b = list(b)
    for crossover_index in range(len(p)):
        if p[crossover_index] <= 0.7:
            a[crossover_index] = b[crossover_index]
    return a


def mutation(a: list, p):
    if p < 0.05:
        a[random.choice(list(range(len(a))))] = random.choice(letters)
    return a


if __name__ == "__main__":
    # population
    for s in range(1000):
        population.append(gen_population())

    # generation
    for i in range(10000):
        matchingCharIndex = []
        numCharSeq = []
        populationScores = []

        for s in range(len(population)):
            matchingCharIndex.append(matching_char_in_sequence(listSolutionName, list(population[s])))
            numCharSeq.append(len(matchingCharIndex[s]))
            populationScores.append((fitness(num_char_seq=numCharSeq[s], len_of_string=lenOfName), ''.join(population[s])))

        populationScores.sort(key=lambda x: x[0], reverse=True)
        if populationScores[0][0] >= 1:
            print(f"=== Gen {i} found the name ===")
            print("Fitness score:", populationScores[0][0], "AI generated name:", "'" + populationScores[0][1] + "'")

            input("Press enter to quit")
            sys.exit(0)

        else:
            print(f"=== Gen {i} best solutions === ")
            print("Fitness score:", round(populationScores[0][0], 4), "AI generated name:", "'" + populationScores[0][1] + "'\n")

        bestFit = populationScores[:500]
        newGen = []
        for s in range(len(bestFit)):
            countLooper = (1 + s) % len(bestFit)
            for _ in range(2):
                newGen.append(uniform_crossover(
                    bestFit[s][1],
                    bestFit[countLooper][1],
                    np.random.rand(lenOfName)
                ))
                newGen[s] = mutation(newGen[s], np.random.rand(1))
        population = newGen

