from itertools import product, permutations, combinations_with_replacement, dropwhile, filterfalse
from itertools import combinations
import numpy as np


def compute_rows(num_of_rows):
    # get row patterns
    perm = product(range(2), repeat=num_of_rows)
    # print(type(perm))
    combinations = []
    # get all valid combinations
    for i in list(perm):
        twin = []
        for num in list(i):
            if num == 0:
                twin.append(1)
            elif num == 1:
                twin.append(0)
        twin = tuple(twin)
        num_of_ones = i.count(1)
        num_of_zeros = i.count(0)
        # print(num_of_ones)
        if i not in combinations and twin not in combinations and num_of_ones == num_of_zeros:
            row_as_str = ''.join(map(str, i))
            if '000' in row_as_str:
                # print('three zeros in a row :(')
                continue
            elif '111' in row_as_str:
                # print('three ones in a row :(')
                continue
            combinations.append(i)
    return combinations



def compute_rows2(num_of_rows):
    zeros = np.zeros(int(num_of_rows/2))
    ones = np.ones(int(num_of_rows/2))
    a = np.concatenate((zeros, ones), axis=None)
    #perm = permutations(a, num_of_rows)
    perm = combinations_with_replacement(a, num_of_rows)
    #return list(perm)
    # get row patterns
    #perm = product(range(2), repeat=num_of_rows)
    combinations_rows = filterfalse(lambda x: x.count(0) == x.count(1), list(perm))
    #combinations_rows = filterfalse(lambda x: '000' not in ''.join(map(str, x)), list(perm))
    '''
    # get all valid combinations
    for i in list(perm):
        twin = []
        for num in list(i):
            if num == 0:
                twin.append(1)
            elif num == 1:
                twin.append(0)
        twin = tuple(twin)
        num_of_ones = i.count(1)
        num_of_zeros = i.count(0)
        # print(num_of_ones)
        if i not in combinations_rows and twin not in combinations_rows and num_of_ones == num_of_zeros:
            row_as_str = ''.join(map(str, i))
            if '000' in row_as_str:
                # print('three zeros in a row :(')
                continue
            elif '111' in row_as_str:
                # print('three ones in a row :(')
                continue
            combinations_rows.append(i)
    '''
    return combinations_rows


combinations = compute_rows(24)
'''
print(list(combinations))
for c in combinations:
    print(c)
'''
print(len(list(combinations)))
# print(list(combinations))

