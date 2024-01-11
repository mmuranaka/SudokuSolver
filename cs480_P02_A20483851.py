import sys
import csv
import copy
import timeit
class Sudoku:
    def __init__(self):
# takes full array of each sudoku block and handles
        self.board = [['X']*9 for _ in range(9)]                        # initialize as empty Sudoku board
        self.domain = [[[]]*9 for y in range(9)]
    
# setBoard is used to place what is read from the csv file into a Sudoku object
# domain is not set because that is only used for Back and Forward    
    def setBoard(self, board):
# takes board (array given by csv file and sets self's board) also changes string numbers into ints
        self.board = board
        for i in range(0,9):
            for j in range(0,9):
                try:
                    self.board[i][j] = int(self.board[i][j])                #I also recognized all the numbers as ints
                except ValueError:                                          #this is a "x"
                    continue                                                # X's are initialized on board (nothing to change)
        return self
    
# As far as I can understand, I am only supposed to use this for the backtrack and mrv search  
# this is only used on the starting board (forward checking has to manually update all other domains as it runs)  
    def setDomain(self):
        for i in range(0,9):
            for j in range(0,9):
                # print(str(i) + " " + str(j))
                if (self.board[i][j] == "X"):                               # domain is all possible (so it can be allowed for back-tracking
                    self.domain[i][j] = [1,2,3,4,5,6,7,8,9]
                else:
                    self.domain[i][j] = [self.board[i][j]]
        self.slimDomain()
        return self
    
# used only for forward checking
    def slimDomain(self):
        for i in range(0,9):                                                 # row
            for j in range(0,9):                                             # column ; goes through each space and updates domain
                if (len(self.domain[i][j]) > 1):                             # domain numbers that can be slimmed
                    for k in range(0,9):
                        if (self.board[i][k] in self.domain[i][j]):          # removes like values in row from domain   
                            self.domain[i][j].remove(self.board[i][k])
                        if (self.board[k][j] in self.domain[i][j]):
                            self.domain[i][j].remove(self.board[k][j])       # removes like values in column from domain
                    # now I gotta do each "block"
                    # i is the row, j is the column
                    # 0,3,6
                    blockrow = (i // 3)*3
                    blockcolumn = (j // 3)*3
                    for m in range(blockrow, blockrow+3):
                        for n in range(blockcolumn, blockcolumn+3):
                            if m==i and n==j:                               #we are at current spot                          
                                continue
                            else:
                                if (self.board[m][n] in self.domain[i][j]):
                                    self.domain[i][j].remove(self.board[m][n])
        # print(self.domain[4][6])
        # print(self.domain[8][7])
        # print(self.domain[8][8])
        return self

# used by foward checking to update domains
# we will be given the input board (this is where we change the domains)
# the place that the number was placed
# the current board (will have the number placed)
    def updateDomains(self, seed, row, column):
        # seed.board[row][column] contains the number that was placed down
        for i in range(0,9):                                                        #iterates through rows
            if i==row:  # current spot
                continue
            else:
                if (seed.board[row][column] in self.domain[i][column]):
                    self.domain[i][column].remove(seed.board[row][column])          #removes 
        for j in range(0,9):                                                        # iterates through columns
            if j==column:
                continue
            else:
                if (seed.board[row][column] in self.domain[row][j]):
                    self.domain[row][j].remove(seed.board[row][column])             #removes 
        blockrow = (row // 3)*3
        blockcolumn = (column // 3)*3
        for m in range(blockrow, blockrow+3):
            for n in range(blockcolumn, blockcolumn+3):
                if m==row and n==column:
                    continue
                else:
                    if (seed.board[row][column] in self.domain[m][n]):
                        try:
                            self.domain[m][n].remove(self.board[row][column])
                        except ValueError:
                            continue
        return self
    
# returns the variable placement that has the given domain size
    def findVariableDomainSize(game, size):
        for i in range(0,9):
            for j in range(0,9):
                # print(str(i) + " " + str(j) + " " + str(game.domain[i][j]))
                if (len(game.domain[i][j]) == size):        # correct size of domain for mrv
                    return i, j
        return None, None                                   # no variable with that domain size
# for printing out game
    def __str__(self):
        out = ""
        for i in range(0,9):                    # iterates through rows
            for j in range(0,9):                # iterates through columns
                if j==8:
                    if i==8:
                        out += str(self.board[i][j])
                    else:
                        out += str(self.board[i][j]) + "\n"
                else:
                    out += str(self.board[i][j]) + ","
        return out

# checks whether all the numbers on the board are between 1 and 9 (should only be called by testValidity)
    def boardInRange(self):                     # checks if all the values on the board are 1 through 9 (only filled boards)
        for i in range(0,9):
            for j in range(0,9):
                if (self.board[i][j] == "X"):   # board should only be filled
                    return False
                # print(str(i) + " " + str(j))
                # print(self.board[i][j])
                if ( (self.board[i][j] < 1) or (self.board[i][j] > 9) ):
                    return False
        return True
# tests validity of board (whether board is valid and solved)        
    def testValidity(self):
        if (self.boardInRange() == False):  #contains invalid numbers or an "x"
            return False
        for i in range (0,9):               # test rows and columns
            row = []                        # append numbers found to this list
            column = []
            for j in range(0,9):
                if self.board[i][j] in row:         # checks if number was already found (invalid)
                    return False
                if self.board[j][i] in column:
                    return False
                row.append(self.board[i][j])
                column.append(self.board[j][i])
        # now I gotta do each "block"
        for i in range(0,9,3):                      # iterates through blocks by row
            for j in range(0,9,3):                  # iterates through blocks by column
                block = []
                for k in range(j,j+3):              # iterates through the rows in a single block
                    for m in range(i,i+3):          # iterates through the columns in a single block
                        if self.board[m][k] in block:
                            return False
                        block.append(self.board[m][k])
        return True

# checks whether board is empty
# True if empty, False is full
    def findEmpty(self):
        for i in range(8, -1, -1):                      # I chose to iterate from the bottom right of the puzzle becuase I assume this finds an empty spot fastest
            for j in range(8, -1, -1):
                if (self.board[i][j] == "X"):
                    return True
        return False

# given a placement, checks if this placement inteferes with a possible previous placement 
# row and column was where the placement was
# used by backtrack to see if a placement is valid considering other placements
# (0,4)
    def checkConsistency(self, row, column):
        for i in range(0,9):                                #iterates through items in column
            if (i==row):
                continue
            if (self.board[i][column] == self.board[row][column]):
                return False
        for j in range(0,9):                                #iterates through items inm row
            if (j==column):
                continue
            if (self.board[row][j] == self.board[row][column]):
                return False
        blockrow = (row // 3)*3
        blockcolumn = (column // 3)*3
        for m in range(blockrow, blockrow+3):
            for n in range(blockcolumn, blockcolumn+3):
                # print(str(row) + " " + str(column) + " " + str(m) + " " + str(n))
                if (m==row and n==column):
                    continue
                else:
                    if (self.board[m][n] == self.board[row][column]):
                        # print("false")
                        return False
        # print("check")
        return True
# Brute Force: 
#   For a given board, checks value 1-9 for unassigned values, places value for assigned values
# Base Case: temp board has all values filled in
#            Check if valid board: return board
#            if not continue
# Recursive Step:
# game never changes (this is the input board that we compare for domains, values we can place)
def BruteForce(game, seed, row, column, count):
    # print("start\n" + str(seed))
    if not (seed.findEmpty()):                          #board is filled
        if (seed.testValidity()):                       #board works
            return seed, count
        else:                                           #board is invalid
            return None, count
    else:                                               #board is not filled
        if (game.board[row][column] == "X"):            #domain could be anything
            # print("before for\n" + str(seed))
            for i in range(1,10):                       # expand tree for all possible values
                temp = Sudoku()
                # print("in for\n" + str(seed))
                temp = copy.deepcopy(seed)
                temp.board[row][column] = i             # place value in temporary possible board
                count = count + 1
                if (column==8):                         #it's okay if invalid row because the board will find that it is full
                    temprow = row+1
                    tempcolumn = 0
                else:
                    temprow = row
                    tempcolumn = column + 1
                # print("before call\n" + str(seed))
                possible, count = BruteForce(game, temp, temprow, tempcolumn, count)
                # print("after call\n" + str(seed))
                if possible is not None:
                    return possible, count                              #possible board found
            return None, count                                          # no possible board was found

        else:
            seed.board[row][column] = game.board[row][column]           # board already has this value
            count = count + 1
            if (column==8):
                row+=1
                column=0
            else:
                column+=1
            return BruteForce(game, seed, row, column, count)


# Same as Brute force but:
#   unassigned variables have a smaller domain
#   if an assignment inteferes with another assignment, explore different
# Base Case:
#   board is 
def BackTrack(game, seed, row, column, count):
    # print("back\n" + str(seed) + "\n" + str(count))
    if not (seed.findEmpty()):                          #board is filled
        # print("here\n" + str(seed))
        if (seed.testValidity()):                       #board works
            return seed, count
        else:
            return None, count
    else:
        if (len(game.domain[row][column])==0):      # I added this for forward checking, honestly ignore this if
            if (column==8):
                row+=1
                column=0
            else:
                column+=1
            return BackTrack(game, seed, row, column, count)
        for i in game.domain[row][column]:                          #expand tree for all values in domain
            temp = copy.deepcopy(seed)
            temp.board[row][column] = i                             # place value in temporary possible board
            count = count + 1
            # print(str(row) + " " +  str(column))
            if (temp.checkConsistency(row, column)):
                # print("consistent\n" + str(temp))
                if (column==8):                             #it's okay if invalid row because the board will find that it is full
                    temprow = row+1
                    tempcolumn = 0
                else:
                    temprow = row
                    tempcolumn = column + 1
                # print("\n" + str(temp))
                possible, count = BackTrack(game, temp, temprow, tempcolumn, count)
                if possible is not None:
                    return possible, count
        return None, count

# Forward Checking:
#   needs to determine the variables with the smallest domain
#   assign those variables and update the domain of those affected
# game is input
# originally seed is also empty board (domain will be updated as values are added)
# mrv keeps track of what domain size we are looking for (starting from 1 to 9)

# correct changes will be made to game, exploration will occur in seed
def ForwardCheck(game, seed, mrv, count):
    if not (seed.findEmpty()):                          #board is filled
        if (seed.testValidity()):                       #board works
            return seed, count
        else:
            return None, count
    else:
        row, column = game.findVariableDomainSize(mrv)                      #mrv starts at 1 (domain only has one variable), and finds a variable with this sized domain
# we are not going to update domain if mrv is not 1
        if row is not None:                                                 #variable with sized domain was found
            for i in game.domain[row][column]:
                temp = copy.deepcopy(seed)
                temp.board[row][column] = i
                count+=1
                if (mrv == 1):                                              #can immediately update domain of possibly affected variables
                    game.updateDomains(temp, row, column)                   #update domains because this is correct (mrv=1)
                    game.domain[row][column] = []                           #I am going to make the domain zero for my function findVariableDomainSize                                                 
                    possible, count = ForwardCheck(game, temp, mrv, count)
                else:
                    possible, count = BackTrack(game, temp, 0, 0, count)    #I was having trouble so I just did this
                if possible is not None:
                    return possible, count
            return None, count
        else:
            mrv+=1
            return ForwardCheck(game, seed, mrv, count)
            

print("Muranaka, Matthew, A20483851 solution:")
# this part of the code concerns argument checking
# check whether wrong amount of arguments
if (len(sys.argv) != 3):
    print("ERROR: Not enough/too many/illegal input arguments.")
    exit()
# if code makes it here, correct amount of arguments
# I still need to check for invalid arguments  
mode = sys.argv[1]
filename = sys.argv[2]
game = Sudoku()
try:
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        board = [[]*9 for _ in range(9)]
        lineNumber = 0
        for lines in csvFile:
            board[lineNumber] = lines
            lineNumber+=1
except FileNotFoundError:
    print("ERROR: Not enough/too many/illegal input arguments.")
    exit()
game.setBoard(board)
# print(game.board[0][0] == "X")                       
state = Sudoku()
print("Input file: " + filename)
if (mode=='1'):
    print("Algorithm: brute force search\n")
    print("Input puzzle: \n")
    print(str(game) + "\n")
    timeStart = timeit.default_timer()
    finished, count = BruteForce(game, state, 0, 0, 0)
    timeEnd = timeit.default_timer()
    elapsedTimeInSec = timeEnd - timeStart
    print("Number of search tree nodes generated: " + str(count))
    print("Search time: " + str(elapsedTimeInSec) + " seconds\n")
    print("Solved puzzle:\n")
    print(str(finished))

    filewrite = filename[:-4]
    filewrite += "_SOLUTION.csv"
    with open(filewrite, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(finished.board)
elif (mode=='2'):
    print("Algorithm: Constraint Satisfaction Problem back-tracking search\n")
    print("Input puzzle: \n")
    print(str(game) + "\n")
    timeStart = timeit.default_timer()
    game.setDomain()
    # print(game.domain[0][0][0])
    finished, count = BackTrack(game, state, 0, 0, 0)
    timeEnd = timeit.default_timer()
    elapsedTimeInSec = timeEnd - timeStart
    print("Number of search tree nodes generated: " + str(count))
    print("Search time: " + str(elapsedTimeInSec) + " seconds\n")
    if finished is not None:
        print("Solved puzzle:\n")
        print(str(finished))

        filewrite = filename[:-4]
        filewrite += "_SOLUTION.csv"
        with open(filewrite, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(finished.board)
    else:
        print("No Solution Possible")
elif (mode=='3'):
    print("Algorithm: CSP with forward-checking and MRV heuristics\n")
    print("Input puzzle: \n")
    print(str(game) + "\n")
    timeStart = timeit.default_timer()
    game.setDomain()
    # state = copy.deepcopy(game)
    # state.domain = copy.deepcopy(game.domain)
    finished, count = ForwardCheck(game, state, 1, 0)
    timeEnd = timeit.default_timer()
    elapsedTimeInSec = timeEnd - timeStart
    print("Number of search tree nodes generated: " + str(count))
    print("Search time: " + str(elapsedTimeInSec) + " seconds\n")
    if finished is not None:
        print("Solved puzzle:\n")
        print(str(finished))

        filewrite = filename[:-4]
        filewrite += "_SOLUTION.csv"
        with open(filewrite, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(finished.board)
    else:
        print("No Solution Possible")

elif (mode=='4'):
    print("Algorithm: test if the completed puzzle is correct")
    print("Input file: " + filename)
    print("Input puzzle: ")
    print(str(game))
    if (game.testValidity()):
        print("This is a valid, solved, Sudoku puzzle.")
    else:
        print("ERROR: This is NOT a solved Sudoku puzzle.")
elif (mode=='5'):                                                               # idk if im allowed to do this but this mode lets me test the averages
    print("Enter Algo to Test: ")
    algo=str(input())
    print("Enter amount of Runs to Test: ")
    runs = int(input())
    timeslst = []
    nodeslst = []
    for i in range(0,runs):
        if algo=='1':
            timeStart = timeit.default_timer()
            finished, count = BruteForce(game, state, 0, 0, 0)
            timeEnd = timeit.default_timer()
            elapsedTimeInSec = timeEnd - timeStart
        elif algo=='2':
            timeStart = timeit.default_timer()
            game.setDomain()
            finished, count = BackTrack(game, state, 0, 0, 0)
            timeEnd = timeit.default_timer()
            elapsedTimeInSec = timeEnd - timeStart
        elif algo=='3':
            timeStart = timeit.default_timer()
            game.setDomain()
            # state = copy.deepcopy(game)
            # state.domain = copy.deepcopy(game.domain)
            finished, count = ForwardCheck(game, state, 1, 0)
            timeEnd = timeit.default_timer()
            elapsedTimeInSec = timeEnd - timeStart
        else:
            exit()
        timeslst.append(elapsedTimeInSec)
        nodeslst.append(count)
    totaltime = 0
    totalnodes = 0
    for i in timeslst:
        totaltime += i
    for i in nodeslst:
        totalnodes += i
    averagetime = totaltime/runs
    averagenodes = totalnodes/runs
    print("Average Search Time: " + str(averagetime))
    print("Average Nodes Generated: " + str(averagenodes))

else:
    print("ERROR: Not enough/too many/illegal input arguments.")
    exit()
