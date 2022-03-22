import matplotlib.pyplot as plt
import numpy as np
#from main import compute_rows

#dims = np.arange(2, 18, 2)
dims = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
#rowpatterns = [len(compute_rows(d)) for d in dims]
rowpatterns = np.array([1, 3, 7, 17, 42, 104, 259, 648, 1627, 4098])
cells = dims**2

#n = dims/2
n = np.arange(0, 20)
#rowpatterns_formula = n * 2**(n-1) + 2
rowpatterns_formula = 0.45652400866460263*0.4397988366769935**n
print(rowpatterns_formula)

print(dims, rowpatterns)

#differences = rowpatterns_formula-rowpatterns

plt.figure()
plt.plot(dims, rowpatterns, '.', label='number of row patterns from code')
plt.plot(n, rowpatterns_formula, label='number of row patterns from formula')
#plt.plot(dims, differences)
plt.legend()
plt.show()

''' Exponential fit '''
# Define new variables
x = dims#/2
y = rowpatterns
X = x
Y = np.log(y)

# Fit a first degree polynomial
p = np.polyfit(X, Y, 1)
a=p[0]  # Exponent of powerlaw
B=p[1]  # Logarithm of prefactor
b=np.exp(B)  # Prefactor
# Print the result

print(f"Best fit to a exponential function: y = {a}*{b}^x")

# Plot the fit
plt.figure()
Xfit = np.arange(0, 20, 0.1)
Yfit = np.polyval(p, Xfit)
plt.plot(X,Y,'.',label="data")
plt.plot(Xfit, Yfit, '-', label="fit")
plt.legend()
plt.xlabel("X=log(x)")
plt.ylabel("Y=log(y)")
plt.show()


'''
# Fit a first degree polynomial
p = np.polyfit(x, y, 5)

# Print the result
a=p[0]  # Slope
b=p[1]  # Intersection at x=0
print("Best fit to a polynomial: y = %f*x + (%f)" % (a,b))

# Plot the fit
plt.figure()
xfit = np.arange(0, 10, 0.5)
yfit = np.polyval(p, xfit)
plt.plot(x,y,'.',label="data")
plt.plot(xfit, yfit, '-', label="fit")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.show()
'''
