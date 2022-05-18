# “The Mathematics of Takuzu”

This repository contains the code for our 2022 Bachelor Project in Natural Sciences at Roskilde University. The topic of the project is the Takuzu puzzle, which we investigated and analyzed mathematically.

All code is written in Python. The most important file, which contains the integer linear programming (ILP) approach for solving Takuzu grids, is `integer_linear_optimization.py` .

## Short description of the files

- `integer_linear_optimization.py` → ILP for solving / generating Takuzu grids
- `ilp_with_functions.py` → an attempt to do ILP using with defining functions
- `minimization_2x2.py` → solving and generating 2x2 Takuzu grids using ILP
- `plot_obj_func.py` → a script for plotting different cost distributions
- `main.py` → an attempt to generate all row patterns for different sizes
- `rowpattern_approximation.py` → a script for plotting the number of row patterns for different sizes along with functions approximating this sequence
- `data.txt` → data sheet of the number of row patterns for different sizes of Takuzu grids (source: [https://oeis.org/A003440](https://oeis.org/A003440))

## Used packages

The `integer_linear_optimization.py` file for the ILP approach uses NumPy and the [Gekko](https://gekko.readthedocs.io/en/latest/#) module. The scripts for plotting also require Matplotlib.
