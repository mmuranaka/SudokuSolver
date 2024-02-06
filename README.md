# SudokuSolver
A user-interactive program that is passed a Sudoku puzzle through a CSV file, completing the puzzle and checking for validity.

Files:
Sudoku_Solver_Writeup.pdf
Documentation of the objective of the project; includes the types of algorithms implemented, usage of the program, expectations of output, and evaluation of the various algorithms.
TestCases
Folder containing seven unsolved sudoku puzzles of varying difficulties, the test cases are csv files with exactly eight rows and columns to be read by the python program where 'X' notes an empty block of the puzzle; note testcase3 does not have a valid solution.
TestCaseSolutions
Folder containing the solutions for the six sudoku puzzles (excluding testcase3), the solutions are of the csv format.
cs480_P02_A20483851.py
Python program that takes unsolved Sudoku puzzles and solves them if there is a valid solution, tests if a Sudoku board is valid, or performs evaluation of the algorithms.

Usage
python cs480_P02_AXXXXXXXX.py MODE FILENAME
Mode specifies the mode in which in the program will run
1 - brute force search; checks values 1-9 for each unsolved blocks in the board and tests the validity of filled board, repeating until the filled in board is solved
2 - Constraint Satisfaction Problem back-tracking search; reduces domain by eliminating values that cannot be considered (already in row, column, or square), and performs the brute force search through those values in the domain
3 - CSP with forward-checking and MRV heuristics, reduces domain similarly, and solves for cells that have the smallest domain first, updating the domain of affected variables
4 - tests if the completed puzzle is correct
5 - Evaluates the time needed for a given algorithm to solve the given test case, the user can determine the amount of the tests to average.
Following the initial command, the program will prompt the user for an integer input to determine the amount of tests to run and average over.

Filename specifies the test case to be input into the program


