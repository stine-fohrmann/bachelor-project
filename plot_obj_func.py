
'''
Script for plotting objective functions with different cost distributions
'''

# imports
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 100, 1, dtype='int64')
# generate fibonacci sequence as cost
fibonacci = np.array([1, 1], dtype='int64')
while len(fibonacci) < len(x):
    nth = fibonacci[-1] + fibonacci[-2]
    fibonacci = np.append(fibonacci, nth)

fig1 = plt.figure(1)
#plt.plot(x, fibonacci, label='Fibonacci sequence')
plt.plot(x, x, label='simple cost distribution')
plt.plot(x, 1.1**x, label='exponential cost')
plt.title('Different cost distributions')
plt.legend()

plt.show()

