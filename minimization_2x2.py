from gekko import GEKKO
import numpy as np

m = GEKKO(remote=False)

n = 2
'''
cells = []
for j in range(n):
    row = []
    for i in range(n):
        row_item = m.Array(m.Var, 1, integer=True, lb=0, ub=1)
        row.append(row_item)
    # print(row)
    cells.append(row)
print(cells[0][1])
'''

x11, x21, x12, x22 = m.Array(m.Var, 4, integer=True, lb=0)
rows = [[x11, x21], [x12, x22]]
cols = np.transpose(rows)

# objective function
f = 1 * x11 + 2 * (x12 + x21) + 3 * x22
# f1 = 1 * cells[0][0] + 2 * (cells[0][1] + cells[1][0]) + 3 * cells[1][1]
m.Minimize(f)

# add constraint equations
for i in range(n):
    # binary balance for columns
    m.Equation(sum(cols[i]) - n * (1 / 2) == 0)
    # binary balance for rows
    m.Equation(sum(rows[i]) - n * (1 / 2) == 0)

# define initial clues
m.Equation([
    # x11 == 0,
    # x12 == 0,
    # x21 == 0,
    # x22 == 0,
])

m.options.SOLVER = 1
m.solve()
print('Objective: ', -m.options.OBJFCNVAL)

# print filled out grid
print(int(x11.value[0]), int(x21.value[0]))
print(int(x12.value[0]), int(x22.value[0]))
