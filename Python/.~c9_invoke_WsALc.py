#7/9/2016
#Jadiker

#When written in Lua, I had encapulated the solve function in a class, but here 
#I decided to make it a fucntion like it should be.

#puzzle is a list containing two lists, rPuz and cPuz.
#rPuz and cPuz are (also) lists which contain 
#the puzzles for the rows and columns respectively. 
#For example, if the nonogram solution was the letter H on a 3x3 grid,
#rPuz would be [[1, 1], [3], [1, 1]] and cPuz would be [[3], [1], [3]]
#Each row or column is called a band, so each list in rPuz or cPuz
#is called a band puzzle.
def solve(puzzle):
    rPuz = puzzle[0]
    cPuz = puzzle[1]
    #The board is a 2-dimensional array that
    #represents the solution to the problem.
    #Inside the board, a 0 means that square should not be filled.
    #A 1 means that square should be filled, and a 2 means it's not sure yet.
    board = []
    boardDimensions = [len(rPuz), len(cPuz)] #[height, width]
    #make an empty board
    for i in range(boardDimensions[0]):
        emptyRow = []
        for j in range(boardDimensions[1]):
            emptyRow.append(2)
        board.append(emptyRow)
    
    #create a new list called possibilities that holds all the possible ways
    #a particular band could be oriented based on the puzzle.
    #As the program continues, the amount of orientations 
    #only holds one possibility per puzzle.
    #possibilities is in the same format as puzzle:
    #[[row1Possibilities, row2Possibilities, ...], [column1Possibilities, column2Possibilities, ...]]
    possibilities = []
    for rowOrCol, bandPuzzles in enumerate(puzzle):
        possesToAdd = [] #short for 'possibilities to add'
        for bandPuzzle in bandPuzzles:
            possesToAdd.append(generatePossibilities(bandPuzzle, ))
        possibilities.append(possesToAdd)
    
    
    
    
    

