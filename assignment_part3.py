import string
import random

solutionName = 'trym brabrand'
population = []


def matching_char_in_sequence(my_name, random_name):
    num_char_seq = 0
    len_of_string = len(my_name)

    for i in my_name:
        if "my_name[i]" == "random_name[i]":
            num_char_seq += 1

    return num_char_seq, len_of_string


def gen_population(my_name) -> population:
    res_first_name = ''.join(random.choices(string.ascii_lowercase, k=my_name.find(' ')))
    res_last_name = ''.join(random.choices(string.ascii_lowercase, k=(len(my_name) - my_name.find(' '))))
    res_name = str(res_first_name + " " + res_last_name)

    return res_name


def fitness(num_char_seq: int, len_of_string: int):
    score = num_char_seq / len_of_string

    return score


if __name__ == "__main__":  # Might not need the main loop!

    # population
    for i in range(1000):
        population.append(gen_population(solutionName))
        numCharSeq, lenOfName = matching_char_in_sequence(solutionName, population[i])

    # generation
    for s in range(10000):
        break

    # print(int(numCharSeq))
