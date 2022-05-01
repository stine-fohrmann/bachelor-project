import random

from gekko import GEKKO
import numpy as np

# m = GEKKO(remote=False)
m = GEKKO(remote=True, server='https://byu.apmonitor.com')

# define grid size
n = 6

# create grid of n*n cells
cells = np.array([])
for i in range(n * n):
    x = m.Var(integer=True, lb=0, ub=1)
    cells = np.append(cells, x)
# print(cells)
cols = np.array_split(cells, n)
# print(cols)
rows = np.transpose(cols)

# define objective function
f = 0
cost = 0
for i in range(n):
    for j in range(n):
        # print(1.1**cost)
        f += 1.1 ** cost * cols[i][j]
        cost += 1
        # f += cost * cols[i][j]
# minimize objective function
m.Minimize(f)
# m.Maximize(f)

# add constraint equations
# constraint 1: binary balance
for i in range(n):
    # binary balance for columns
    m.Equation(sum(cols[i]) - n * (1 / 2) == 0)
    # binary balance for rows
    m.Equation(sum(rows[i]) - n * (1 / 2) == 0)

# constraint 2: uniqueness
for i in range(n):
    for j in range(1, n - 1):
        if i != j:
            # uniqueness for columns
            m.Equation(sum(abs(cols[i] - cols[j])) > 1)
            # uniqueness for rows
            m.Equation(sum(abs(rows[i] - rows[j])) > 1)

# constraint 3: no triplets
# for i in range(n):
#     for j in range(n - 2):
#         # no triplets in rows
#         m.Equation(abs((rows[i][j] - 1 / 2) + (rows[i][j + 1] - 1 / 2) + (rows[i][j + 2] - 1 / 2)) == 1 / 2)
#         # m.Equation(abs(rows[i][j] + rows[i][j + 1] + rows[i][j + 2] - 3 / 2) == 1 / 2)
#         # m.Equation(abs(cols[j][i] + cols[j + 1][i] + cols[j + 2][i] - 3 / 2) == 1 / 2)
#         # no triplets in columns
#         m.Equation(abs((cols[i][j] - 1 / 2) + (cols[i][j + 1] - 1 / 2) + (cols[i][j + 2] - 1 / 2)) == 1 / 2)
#         # m.Equation(abs(rows[j][i] + rows[j + 1][i] + rows[j + 2][i] - 3 / 2) == 1 / 2)
#         # m.Equation(abs(cols[i][j] + cols[i][j + 1] + cols[i][j + 2] - 3 / 2) == 1 / 2)


# additional constraint based on objective value
# m.Equation(f > 140.6)

# method for defining clues / cell values
def set_cell_value(row_index, col_index, value):
    m.Equation(rows[row_index][col_index] == value)


# define clues / cell values
# set_cell_value(0, 0, 1)
# set_cell_value(0, 1, 1)
# set_cell_value(1, 0, 1)
# set_cell_value(1, 1, 1)
# set_cell_value(3, 0, 1)

m.options.SOLVER = 1
# m.solver_options = ['minlp_maximum_iterations 10000', 'minlp_max_iter_with_int_sol 500']

try:
    m.solve(disp=True)  # solve
    # print filled out grid
    for row in rows:
        print([int(cell.value[0]) for cell in row])
except:
    print('Not successful')
    from gekko.apm import get_file

    print(m._server)
    print(m._model_name)
    f = get_file(m._server, m._model_name, 'infeasibilities.txt')
    f = f.decode().replace('\r', '')
    with open('infeasibilities.txt', 'w') as fl:
        fl.write(str(f))

print('Objective: ', -m.options.OBJFCNVAL)

# print value of objective function
'''
f_value = 0
cost = 0
for i in range(n):
    for j in range(n):
        # print(1.1**cost)
        f_value += 1.1**cost * cols[i][j].value[0]
        cost += 1
print(f_value)
'''

# testing if constraint 3 is fulfilled
'''
for i in range(int(n)):
    # i = 0
    print(f'row {i}')
    for j in range(n - 2):
        # print(j)
        print(abs(rows[i][j].value[0] + rows[i][j + 1].value[0] + rows[i][j + 2].value[0] - 3 / 2))

for i in range(int(n)):
    # i = 0
    print(f'column {i}')
    for j in range(n - 2):
        # print(j)
        print(abs(cols[i][j].value[0] + cols[i][j + 1].value[0] + cols[i][j + 2].value[0] - 3 / 2))
'''
