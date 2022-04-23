from gekko import GEKKO
import numpy as np

# m = GEKKO(remote=False)
m = GEKKO(remote=True, server='https://byu.apmonitor.com')

# define grid size
n = 4

# create n*n cells
cells = np.array([])
for i in range(n * n):
    x = m.Var(integer=True, lb=0, ub=1)
    cells = np.append(cells, x)
# print(cells)
cols = np.array_split(cells, n)
# print(cols)
rows = np.transpose(cols)

# creating 16 cells manually (old)
# x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34, x41, x42, x43, x44 = m.Array(m.Var, 16, integer=True, lb=0, ub=1)
# cols = np.array([[x11, x12, x13, x14], [x21, x22, x23, x24], [x31, x32, x33, x34], [x41, x42, x43, x44]])

# define objective function (needs to be generalized)
# f = 1 * x11 + 2 * (x12 + x21) + 3 * (x13 + x22 + x31) + 4 * (x14 + x23 + x32 + x41) + 5 * (x24 + x33 + x42) + 6 * (x34 + x43) + 7 * x44
f = 1 * cols[0][0] + 2 * (cols[0][1] + cols[1][0]) + 3 * (cols[0][2] + cols[1][1] + cols[2][0]) \
    + 4 * (cols[0][3] + cols[1][2] + cols[2][1] + cols[3][0]) + 5 * (cols[1][3] + cols[2][2] + cols[3][1]) \
    + 6 * (cols[2][3] + cols[3][2]) + 7 * cols[3][3]

m.Minimize(f)

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
            m.Equation(sum(abs(cols[i] - cols[j])) > 1)  # examine this
            # uniqueness for rows
            m.Equation(sum(abs(rows[i] - rows[j])) > 1)


# constraint 3: no triplets
# for i in range(int(n)):
#     # i = 0
#     for j in range(n - 2):
#         # print(j)
#         m.Equation(abs(rows[i][j] + rows[i][j + 1] + rows[i][j + 2] - 3 / 2) == 1 / 2)
#         # m.Equation(abs(cols[i][j] + cols[i][j + 1] + cols[i][j + 2] - 3 / 2) == 1 / 2)
#         m.Equation(abs(rows[j][i] + rows[j + 1][i] + rows[j + 2][i] - 3 / 2) == 1 / 2)

# method for defining clues / cell values
def set_cell_value(row_index, col_index, value):
    m.Equation(rows[row_index][col_index] == value)


# define clues / cell values
set_cell_value(0, 0, 1)
set_cell_value(0, 1, 1)
set_cell_value(1, 0, 1)
# set_cell_value(1, 1, 1)

m.options.SOLVER = 1
# m.solve()

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


# print constraint equations to test whether they are satisfied
# print(sum(abs(rows[0] - rows[1])))
# print(sum(abs(rows[0] - rows[2])))
# print(sum(abs(rows[0] - rows[3])))
# print(sum(abs(rows[1] - rows[2])))
# print(sum(abs(rows[1] - rows[3])))
# print(sum(abs(rows[2] - rows[3])))
