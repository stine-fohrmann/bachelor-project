import matplotlib.pyplot as plt
import numpy as np

with open('data.txt') as f:
    lines = f.readlines()
n_data = np.array([])
patterns_data = np.array([])
for i in lines:
    splitted = i.split(' ')
    n_data = np.append(n_data, int(splitted[0]))
    patterns_data = np.append(patterns_data, int(splitted[1]))

#n = np.arange(0, 600, 1)
n = n_data[0:600]
phi = (1+5**(1/2))/2
rowpatterns_formula = phi**(2*n+2)/(5**(1/4) * np.sqrt(np.pi*n))
#rowpatterns_formula = n * 2**(n-1) + 2

ratio = patterns_data[0:600]/rowpatterns_formula

fig1 = plt.figure(1)
plt.plot(n_data[0:600], patterns_data[0:600], label='# of patterns from data')
plt.plot(n, rowpatterns_formula, label='# of patterns from formula')
plt.title('Number of row patterns')
plt.legend()

fig2 = plt.figure(2)
plt.axhline(y=1, xmin=0, xmax=600, label='ideal ratio', color='r')
plt.plot(n, ratio, label='actual ratio')
plt.title('Ratio of how close the formula approximates the values')
plt.legend()

plt.show()
