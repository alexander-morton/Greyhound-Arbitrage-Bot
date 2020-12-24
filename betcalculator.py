import numpy

def bet_calculator(ls, profit):
    '''takes in a list that contains max odds for each outcome and a list
    containing how much we want to make off each outcome if profit is not a list
    then makes a list assuming equal profit for each outcome'''
    i = 0
    matrix = []
    while i < len(ls):
        j = 0
        row = []
        while j < len(ls):
            if i == j:
                row.append(ls[i] - 1)
            else:
                row.append(-1)
            j += 1
        matrix.append(row)
        i += 1
    
    bet_matrix = numpy.array(matrix)
    bet_inverse = numpy.linalg.inv(bet_matrix)
    if not isinstance(profit, ls):
        i = 0
        profit_vector = []
        while i < len(ls):
            profit_vector.append(profit)
            i += 1
        profit = profit_vector


    bet_vector = numpy.dot(bet_inverse, profit)
    
    return bet_vector