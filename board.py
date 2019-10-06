import random
import sys
import copy
from operator import itemgetter


def countCombos(board):
    totalCombos = 0
    comboMap = [['o' for orb in range(6)] for row in range(5)]

    #find which orbs will be cleared
    for row in range(5):
        for col in range(6):
            if board[row][col] != '0' and isComboMember(board, row, col):
                comboMap[row][col] = 'X'

    #erase combos and increment counter
    for row in range(5):
        for col in range(6):
            if comboMap[row][col] == 'X' and board[row][col] != 'X':
                eraseCombo(board, row, col, comboMap, board[row][col])
                totalCombos += 1

    #perform skyfalls
    while xExists(board):
        for row in range(4,-1,-1):
            for col in range(5,-1,-1):
                if board[row][col] == 'X':
                    skyFall(board, row, col)
    return totalCombos


#skyfalls a orb if needed
def skyFall(board, row, col):
    pos = row
    while pos > 0:
        board[pos][col] = board[pos - 1][col] #orb moves down one
        pos -= 1
    board[0][col] = '0'



#returns true if there is an X on the board
def xExists(board):
    for row in range(5):
        for orb in range(6):
            if board[row][orb] == 'X':
                return True
    return False
            
#returns True if the orb at row,col is part of a combo
def isComboMember(board, row, col):
    #vertical current bottom
    if row > 1:
        if board[row][col] == board[row - 1][col] == board[row - 2][col]:
            return True
    #vertical current middle
    if row > 0 and row < 4:
        if board[row][col] == board[row - 1][col] == board[row + 1][col]:
            return True
    #vertical current top
    if row < 3:
        if board[row][col] == board[row + 1][col] == board[row + 2][col]:
            return True
    #horizonal current left
    if col < 4:
        if board[row][col] == board[row][col + 1] == board[row][col + 2]:
            return True
    #horizontal currrent middle
    if col < 5 and col > 0:
        if board[row][col] == board[row][col + 1] == board[row][col - 1]:
            return True
    #horizontal current right
    if col > 1:
        if board[row][col] == board[row][col - 1] == board[row][col - 2]:
            return True

#erases an entire combo
def eraseCombo(board, row, col, comboMap, comboColor):
    if board[row][col] == comboColor and comboMap[row][col] == 'X':
        board[row][col] = 'X'
        if row < 4:
            eraseCombo(board, row +1, col, comboMap, comboColor)
        
        if row > 0:
            eraseCombo(board, row -1, col, comboMap, comboColor)
        if col > 0:
            eraseCombo(board, row , col - 1, comboMap, comboColor)
        if col < 5:
            eraseCombo(board, row , col + 1, comboMap, comboColor)

#returns totalCombo including skyfalls
def performTurn(board):
    totalCombos = countCombos(board)
    temp = countCombos(board)
    while temp != 0:
        totalCombos += temp
        temp = countCombos(board)

    return totalCombos

#doesnt check if valid move (outside bounds)
def performMove(board, row, col, direction):
    if direction == 'left':
        temp = board[row][col]
        board[row][col] = board[row][col - 1]
        board[row][col - 1] = temp

    elif direction == 'right':
        temp = board[row][col]
        board[row][col] = board[row][col + 1]
        board[row][col + 1] = temp

    elif direction == 'up':
        temp = board[row][col]
        board[row][col] = board[row - 1][col]
        board[row - 1][col] = temp

    elif direction == 'down':
        temp = board[row][col]
        board[row][col] = board[row + 1][col]
        board[row + 1][col] = temp


#returns a list of move commands
def generateMoveList(startRow, startCol, numMoves):
    currentRow = startRow
    currentCol = startCol
    moves = ['left', 'right', 'up', 'down']
    moveList = []
    lastMove = ''
    while len(moveList) < numMoves:
        currentMove = moves[random.randint(0,3)]
        if currentMove == 'left' and currentCol > 0 and lastMove != 'right':
            moveList.append(currentMove)
            currentCol -= 1
            lastMove = currentMove
        elif currentMove == 'right' and currentCol < 5 and lastMove != 'left':
            moveList.append(currentMove)
            currentCol += 1
            lastMove = currentMove
        elif currentMove == 'up' and currentRow > 0 and lastMove != 'down':
            moveList.append(currentMove)
            currentRow -= 1
            lastMove = currentMove
        elif currentMove == 'down' and currentRow < 4 and lastMove != 'up':
            moveList.append(currentMove)
            currentRow += 1
            lastMove = currentMove
    
    return moveList

#Applies a move list
def performMoveList(board, moveList):
    currentRow = 0
    currentCol = 0
    for move in moveList:
        performMove(board, currentRow, currentCol, move)
        if move == 'left':
            currentCol -= 1
        elif move == 'right':
            currentCol += 1
        elif move == 'up':
            currentRow -=1
        elif move == 'down':
            currentRow += 1

#returns a tuple of the position after the movelist is executed in order
def findPosition(moveList):
    position = [0,0]
    for move in moveList:
        if move == 'left':
            position[1] -= 1
        elif move == 'right':
            position[1] += 1
        elif move == 'up':
            position[0] -=1
        elif move == 'down':
            position[0] += 1
    return position

#returns the index of the move that is at that position or -1 if it never reaches that position
def findIndexOfPosition(moveList, position):
    currentPosition = [0,0]
    index = 0
    for move in moveList:
        if currentPosition == position:
            return index
        else:
            if move == 'left':
                currentPosition[1] -= 1
                index += 1
            elif move == 'right':
                currentPosition[1] += 1
                index += 1
            elif move == 'up':
                currentPosition[0] -=1
                index += 1
            elif move == 'down':
                currentPosition[0] += 1
                index += 1
    return -1


#returns a list of movesLists of the top half of the population 
def selectBreeders(population):
    temp = population[:int((len(population) / 2))]
    returnList = []
    for x in temp:
        returnList.append(x[1])
    return returnList

#returns a random pairing of the input population
def pair(population):
    popCopy = copy.deepcopy(population)
    couples = []
    while len(popCopy) != 0:
        currentSelection = random.randint(0,len(popCopy)-1)
        dad = popCopy.pop(currentSelection)
        currentSelection = random.randint(0,len(popCopy)-1)
        mom = popCopy.pop(currentSelection)
        couples.append((dad,mom))

    return couples

def mate(couples):
    childrenMoveLists = []

    for couple in couples:
        spliceIndex = random.randint(1,numMoves -1) #random position to splice
        #first kid --------------
        boardposition = findPosition(couple[0][0:spliceIndex]) #finds where the location is at the splice move
        samePositionIndex = findIndexOfPosition(couple[1], boardposition) #index of the same pos in the second parent
    
        if samePositionIndex == -1:
            #never crosses path, make new random
            newMoveList = couple[0][0:spliceIndex]
            newMoveList += generateMoveList(boardposition[0], boardposition[1], numMoves - len(newMoveList)) #generate random moves to finish out the list
        else:
            newMoveList = couple[0][0:spliceIndex]  #add the first parent up to splice location
            newMoveList += couple[1][samePositionIndex:] #add all of the second parent starting at the same position
            if len(newMoveList) >= numMoves:
                newMoveList = newMoveList[0:numMoves]
            else:
                boardposition = findPosition(newMoveList)
                newMoveList += generateMoveList(boardposition[0], boardposition[1], numMoves - len(newMoveList)) #generate random moves to finish out the list
        childrenMoveLists.append(newMoveList)

        
        #second kid --------------
        boardposition = findPosition(couple[1][0:spliceIndex]) #finds where the location is at the splice move
        samePositionIndex = findIndexOfPosition(couple[0], boardposition) #index of the same pos in the second parent
        if samePositionIndex == -1:
            #never crosses path, make new random
            secondnewMoveList = couple[1][0:spliceIndex]
            secondnewMoveList += generateMoveList(boardposition[0], boardposition[1], numMoves - len(secondnewMoveList)) #generate random moves to finish out the list
        else:
            secondnewMoveList = couple[1][0:spliceIndex]  #add the first parent up to splice location
            secondnewMoveList += couple[0][samePositionIndex:] #add all of the second parent starting at the same position
            if len(secondnewMoveList) >= numMoves:
                secondnewMoveList = secondnewMoveList[0:numMoves]
            else:
                boardposition = findPosition(secondnewMoveList)
                secondnewMoveList += generateMoveList(boardposition[0], boardposition[1], numMoves - len(secondnewMoveList)) #generate random moves to finish out the list
        childrenMoveLists.append(secondnewMoveList)
        

    return childrenMoveLists
        

def main():
    infile = open('board.txt', 'r')
    theBoard = [[orb for orb in row] for row in infile]
    for row in theBoard: #get rid of newlines
        row.pop()

    #initialize population
    population = [] #list of moveLists
    fitness = [] #list of tuples (comboCount,moveList)
    for x in range(128): #number of starting population
        tempBoard = copy.deepcopy(theBoard)
        population.append(generateMoveList(0,0,numMoves)) #create random movelist and put in population
        performMoveList(tempBoard,population[x]) #perform the movelist on a copy board
        fitness.append((performTurn(tempBoard), population[x])) #count combos and add to fitness list
    sortedFitness = sorted(fitness, key=itemgetter(0), reverse=True) #sort chromosomes based on fitness with best first

    for x in range(500):
        breeders = selectBreeders(sortedFitness)
        couples = pair(breeders)
        children = mate(couples)
        #mutate
        population = breeders + children
        fitness.clear()
        for x in population:
            tempBoard = copy.deepcopy(theBoard)
            performMoveList(tempBoard,x)
            fitness.append((performTurn(tempBoard), x))
        sortedFitness = sorted(fitness, key=itemgetter(0), reverse=True) #sort chromosomes based on fitness with best first

    print(sortedFitness[0])
            

numMoves = int(sys.argv[1])
numInterations = int(sys.argv[2])
main()