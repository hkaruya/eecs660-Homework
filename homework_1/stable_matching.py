import sys
import pdb as debugger
import numpy as np

#Main stable matching algorithm
def stableMatching(mens_preference, womens_preference, population):
    womens_rank = _generateRankMatrix(womens_preference, population)
    mens_planned_engagement = -1**(np.ones(population).astype(int))
    mens_engagement = -1**(np.ones(population).astype(int))
    womens_engagement = -1**(np.ones(population).astype(int))

    free_count = population

    while(free_count > 0):
        for i in range(0, population):
            if -1 == mens_engagement[i]:
                mens_planned_engagement[i] += 1
                mans_next_engagement = mens_planned_engagement[i]
                potential_spouse = mens_preference[i][mans_next_engagement]
                if -1 == womens_engagement[potential_spouse-1]:
                    mens_engagement[i] = potential_spouse
                    womens_engagement[potential_spouse - 1] = i + 1
                    free_count -= 1
                else:
                    current_spouse = womens_engagement[potential_spouse - 1]

                    current_spouse_rank = womens_rank[potential_spouse - 1][current_spouse - 1]
                    potential_spouse_rank = womens_rank[potential_spouse - 1][i]

                    if potential_spouse_rank < current_spouse_rank:
                        mens_engagement[current_spouse - 1] = -1

                        mens_engagement[i] = potential_spouse
                        womens_engagement[potential_spouse - 1] = i + 1


    return mens_engagement


#Generates a rank matrix given input
def _generateRankMatrix(preference, size):
    rank_matrix = np.zeros((size, size))
    rank_matrix = rank_matrix.astype(int)

    for i in range(0, size):
        for j in range(0, size):
            item = preference[i][j]
            #print(item, ' is ', j+1)
            rank_matrix[i][item-1] = j+1

    return rank_matrix

#Reads file and generates to preference arrays, mens and women
def readPreferences(filename):
    with open(filename, 'r') as reader:
        array_size = int(reader.readlines()[0])

    #Assume the first two lines are insignificant
        #First line is array size, second line is empty
    men_array = np.loadtxt(fname=filename, dtype='int', delimiter=',', skiprows=2, max_rows=array_size)
    women_array = np.loadtxt(fname=filename, dtype='int', delimiter=',', skiprows=(2+array_size), max_rows=array_size)

    return array_size, men_array, women_array

#Writes engagements in specified way: men, women
def writeEngagements(engagements):
   for i in range(1, len(engagements)):
       print(i+1,engagements[i], sep=', ')


#Returns number of arguements
number_of_args = len(sys.argv)

if 0 != number_of_args:
    #Iterates through all arguements under the assumption they are all file names
    for i in range(1, number_of_args):
        (size, mens_pref, womens_pref) = readPreferences(sys.argv[i])
        writeEngagements(stableMatching(mens_pref, womens_pref, size))
