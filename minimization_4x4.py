from gekko import GEKKO
import numpy as np

m = GEKKO(remote=False)

n = 4
'''
cols = []
for j in range(n):
    row = []
    for i in range(n):
        row_item = m.Array(m.Var, 1, integer=True, lb=0, ub=1)
        row.append(row_item)
    # print(row)
    cols.append(row)
print(cols[0][0])
'''

x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34, x41, x42, x43, x44 = m.Array(m.Var, 16, integer=True, lb=0,
                                                                                         ub=1)
cols = np.array([[x11, x12, x13, x14], [x21, x22, x23, x24], [x31, x32, x33, x34], [x41, x42, x43, x44]])
rows = np.transpose(cols)

# objective function
f = 1 * x11 + 2 * (x12 + x21) + 3 * (x13 + x22 + x31) + 4 * (x14 + x23 + x32 + x41) + 5 * (x24 + x33 + x42) + 6 * (
        x34 + x43) + 7 * x44
m.Minimize(f)

# add constraint equations
for i in range(n):
    # binary balance for columns
    m.Equation(sum(cols[i]) - n * (1 / 2) == 0)
    # binary balance for rows
    m.Equation(sum(rows[i]) - n * (1 / 2) == 0)

for i in range(n-1):
    for j in range(1, n-1):
        if i != j:
            # uniqueness for columns
            m.Equation(sum(abs(cols[i] - cols[j])) > 0)
            # uniqueness for rows
            m.Equation(sum(abs(rows[i] - rows[j])) > 0)

# define initial clues
m.Equation([
    # x11 == 0,
    # x12 == 0,
    # x13 == 0,
    # x21 == 0,
    # x22 == 0,
    # x33 == 0,
    # x32 == 0,
    # x23 == 0,

])

m.options.SOLVER = 1
m.solve()
print('Objective: ', -m.options.OBJFCNVAL)

# print filled out grid
# print using individual cells
# print(int(x11.value[0]), int(x21.value[0]), int(x31.value[0]), int(x41.value[0]))
# print(int(x12.value[0]), int(x22.value[0]), int(x32.value[0]), int(x42.value[0]))
# print(int(x13.value[0]), int(x23.value[0]), int(x33.value[0]), int(x43.value[0]))
# print(int(x14.value[0]), int(x24.value[0]), int(x34.value[0]), int(x44.value[0]))

# print using array of rows
for row in rows:
    print([int(cell.value[0]) for cell in row])

# print constraint equations to test whether they are satisfied
# print(sum(abs(rows[0] - rows[1])))
# print(sum(abs(rows[0] - rows[2])))
# print(sum(abs(rows[0] - rows[3])))
# print(sum(abs(rows[1] - rows[2])))
# print(sum(abs(rows[1] - rows[3])))
# print(sum(abs(rows[2] - rows[3])))

f_value = 1 * x11.value[0] \
          + 2 * (x12.value[0] + x21.value[0]) \
          + 3 * (x13.value[0] + x22.value[0] + x31.value[0]) \
          + 4 * (x14.value[0] + x23.value[0] + x32.value[0] + x41.value[0]) \
          + 5 * (x24.value[0] + x33.value[0] + x42.value[0]) \
          + 6 * (x34.value[0] + x43.value[0]) \
          + 7 * (x44.value[0])
print(f'Objective function value: {f_value}')
