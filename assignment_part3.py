import string
import random

solutionName = input("Please enter your name in only lower-cases sir/ma'am\nhere:\t")
solutionName = str(solutionName)
population = []


def matching_char_in_sequence(my_name, random_name):
    num_char_seq = 0

    for i in range(len(my_name)):
        if my_name[i] == random_name[i]:
            num_char_seq += 1

    return num_char_seq


def gen_population(my_name) -> population:
    res_first_name = ''.join(random.choices(string.ascii_lowercase, k=my_name.find(' ')))
    res_last_name = ''.join(random.choices(string.ascii_lowercase, k=(len(my_name) - my_name.find(' ') - 1)))
    res_name = str(res_first_name + " " + res_last_name)

    return res_name


def fitness(num_char_seq: int, len_of_string: int):
    score = num_char_seq / len_of_string
    return score


if __name__ == "__main__":  # Might not need the main loop!
    numCharSeq = []
    lenOfName = len(solutionName)

    # population
    for i in range(1000):
        population.append(gen_population(solutionName))
        numCharSeq.append(matching_char_in_sequence(solutionName, population[i]))

    #print(population)

    # generation
    for i in range(10000):
        populationScores = []
        for s in range(len(population)):
            populationScores.append( (fitness(num_char_seq=numCharSeq[s], len_of_string=lenOfName), population[s]) )
        populationScores.sort(key=lambda x: x[0], reverse=True)
        print(f"=== Gen {i} best solutions === ")
        print(populationScores[0])

        bestGuesses = populationScores[:100]
        elements = []
        counter = 1
        halfFirstName = int(solutionName.find(" ") - solutionName.find(" ")/2)
        wholeFirstName = solutionName.find(" ")
        wholeLastName = len(solutionName)
        halfLastName = len(solutionName)-int(wholeFirstName*2)
        for s in bestGuesses:
            elements.append(s[1][:halfFirstName] + bestGuesses[counter][1][halfFirstName:wholeFirstName]
                            + s[1][wholeFirstName:halfLastName] +
                            bestGuesses[counter][1][halfLastName:wholeLastName])
            counter += 1
            counter %= 100

        newGen = []
        for _ in range(1000):
            e1 = random.choices(elements)

            newGen.append(e1)

        population = newGen
