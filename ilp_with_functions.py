from gekko import GEKKO
import numpy as np

# start gekko
# m = GEKKO(remote=False)
m = GEKKO(remote=True, server='https://byu.apmonitor.com')

''' METHODS '''
# method for creating a grid of size n x n
def create_grid(n):
    cells = np.array([])
    for i in range(n * n):
        x = m.Var(integer=True, lb=0, ub=1)
        cells = np.append(cells, x)
    cols = np.array_split(cells, n)
    rows = np.transpose(cols)
    return cols, rows


# method for defining the objective function
def define_objective_function(cols, n):
    # global f, i, j
    f = 0
    cost = 0
    for i in range(n):
        for j in range(n):
            # print(1.1**cost)
            f += 1.1 ** cost * cols[i][j]
            cost += 1
            # f += cost * cols[i][j]
    return f


# method for adding equations for constraint 1
def add_binary_balance(rows, cols, n):
    for i in range(n):
        m.Equation(sum(cols[i]) - n * (1 / 2) == 0)
        m.Equation(sum(rows[i]) - n * (1 / 2) == 0)


# method for adding equations for constraint 2
def add_uniqueness(rows, cols, n):
    for i in range(n):
        for j in range(1, n - 1):
            if i != j:
                m.Equation(sum(abs(cols[i] - cols[j])) > 1)
                m.Equation(sum(abs(rows[i] - rows[j])) > 1)


# method for adding equations for constraint 3
def add_no_triplets(rows, cols, n):
    for i in range(n):
        for j in range(n - 2):
            m.Equation(abs(rows[i][j] + rows[i][j + 1] + rows[i][j + 2] - 3 / 2) == 1 / 2)
            # m.Equation(abs((rows[i][j] - 1 / 2) + (rows[i][j + 1] - 1 / 2) + (rows[i][j + 2] - 1 / 2)) == 1 / 2)
            m.Equation(abs(cols[i][j] + cols[i][j + 1] + cols[i][j + 2] - 3 / 2) == 1 / 2)
            # m.Equation(abs(rows[j][i] + rows[j + 1][i] + rows[j + 2][i] - 3 / 2) == 1 / 2)


# method for defining clues / cell values
def set_cell_value(rows, row_index, col_index, value):
    m.Equation(rows[row_index][col_index] == value)


# method for testing constraint 3
def test_constraint3(rows, cols, n):
    expected_value = 1/2
    for i in range(int(n)):
        #print(f'row {i+1}')
        for j in range(n - 2):
            true_value = abs(rows[i][j].value[0] + rows[i][j + 1].value[0] + rows[i][j + 2].value[0] - 3 / 2)
            #print(true_value)
            if true_value != expected_value:
                print(f"Constraint 3 is not fulfilled in row {i+1}")
    for i in range(int(n)):
        #print(f'column {i+1}')
        for j in range(n - 2):
            true_value = abs(cols[i][j].value[0] + cols[i][j + 1].value[0] + cols[i][j + 2].value[0] - 3 / 2)
            #print(true_value)
            if true_value != expected_value:
                print(f"Constraint 3 is not fulfilled in column {i+1}")


def run_solver(dims, minimize=True, maximize=False, constraint1=True, constraint2=True, constraint3=True):
    # define grid size
    n = dims
    # create grid of n*n cells
    cols, rows = create_grid(n)
    # define objective function
    f = define_objective_function(cols, n)
    # minimize/maximize objective function
    if minimize == True:
        m.Minimize(f)
    elif maximize == True:
        m.Maximize(f)
    # add constraint equations
    if constraint1 == True:
        add_binary_balance(rows, cols, n)
    if constraint2 == True:
        add_uniqueness(rows, cols, n)
    if constraint3 == True:
        add_no_triplets(rows, cols, n)
    # define clues / cell values
    #set_cell_value(rows, 0, 0, 1)
    # additional constraint based on objective value
    # m.Equation(f > 140.6)
    # change solver setting/options
    m.options.SOLVER = 1
    # m.solver_options = ['minlp_maximum_iterations 10000', 'minlp_max_iter_with_int_sol 500']
    # try solving and display solution if found
    try:
        m.solve(disp=False)  # solve
        # print filled out grid
        for row in rows:
            print([int(cell.value[0]) for cell in row])
        # testing
        # test_constraint3(rows, cols, n)
        print('Objective: ', -m.options.OBJFCNVAL)

    except:
        print('Not successful')
        '''
        from gekko.apm import get_file

        print(m._server)
        print(m._model_name)
        f = get_file(m._server, m._model_name, 'infeasibilities.txt')
        f = f.decode().replace('\r', '')
        with open('infeasibilities.txt', 'w') as fl:
            fl.write(str(f))
        '''
    else:
        print('solution found :)')

run_solver(dims=4, constraint3=False, minimize=True, maximize=False)
# run_solver(dims=4, constraint3=False, minimize=False, maximize=True)
