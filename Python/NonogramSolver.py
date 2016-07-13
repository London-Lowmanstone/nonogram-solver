#7/9/2016
#Jadiker

#When written in Lua, I had encapulated the solve function in a class, but here 
#I decided to make it a function like it should be.

#puzzle is a list containing two lists, rPuz and cPuz.
#rPuz and cPuz are (also) lists which contain 
#the puzzles for the rows and columns respectively. 
#For example, if the nonogram solution was the letter H on a 3x3 grid,
#rPuz would be [[1, 1], [3], [1, 1]] and cPuz would be [[3], [1], [3]]
#Each row or column is called a band, so each list in rPuz or cPuz
#is called a band puzzle.
def solve(puzzle):
    #Takes an input, 0 or 1, and returns the opposite (1 or 0)
    #0 generally represents something to do with rows,
    #1 generally corresponds to columns.
    def oppositeRowOrCol(num):
        return (num+1)%2
    
    '''
    This is probably the most complicated part of the code.
    The idea is to generate all the possible positions
    that could exist for that band.
    
    First, I'm going to define blocks.
    Each band is comprised of blocks, connected by space.
    For example, the puzzle [1, 3, 2] has a block of 1 followed by a block of 3,
    followed by a block of 2.
    
    The main idea behind this algorithm is that each block has the same amount
    of "wiggle room", that is, different spaces it can occupy while still
    retaining the order of the blocks in the band.
    
    So, we start as far left as possible (making sure there's exactly one space
    between the blocks), and then shift the block closest to the right over one
    unit. We continue this until that block can't be shifted anymore.
    Then, we reset the entire pattern, and shift the block 2 from the right over
    one unit. Since the rightmost block still needs to maintain separation, it
    follows that the rightmost block must also be shifted over one unit whenever
    a block to the left of it is. After making this one shift, we redo shifting
    the rightmost block, and then more the second rightmost block 1 more
    (pushing the rightmost block another one further down). We continue this
    until the seecond to rightmost block can't go any further. 
    Then we move the third to the rightmost block, which will then push the
    second to the rightmost and the rightmost block over one. We keep repeating
    this process until the leftmost block can't move right any more.
    This will cover all possible positions that this band could be in.
    
    The good news is, the programming is actually quite simple because the math
    for doing what's described above is not very complicated.
    First we generate a starting position, which is stored in a list.
    Then, for each new position we want to generate, we add another list
    (element-wise) to this starting list in order to get the new position.
    It turns out that calculating the starting list and the list to add is not
    very complicated.
    
    I'm going to skip explaining how to calculate the starting list and move 
    straight to explaining how the list to add is calculated.
    
    Let's assume we have a band with 3 blocks on a 10x10 board and together with
    spaces, and the initial starting position takes up 8 units.
    Then, we know that last block can either (1) stay in its initial spot,
    (2) move right one unit, or (3) move right two units (putting its last piece
    on the 10th unit of the board).
    In other words, the first three lists to add should be:
    [0, 0, 0], [0, 0, 1], and [0, 0, 2]
    Then, we know the second block can move to the right one unit
    (since the third block can't move to the right anymore).
    So, we reset everything, and then move the second block to the right one,
    which then forces the third block to also move right one.
    Then, we continue moving the right block once more on its own.
    So the next few should be:
    [0, 1, 1], [0, 1, 2]
    And then we go back and move the second one again
    (which forces the third one to shift over):
    [0, 2, 2]
    And then we restart this whole process with the first one.
    [1, 1, 1], [1, 1, 2], [1, 2, 2], [2, 2, 2]
    And we're done!
    
    So the entire pattern looks like:
    [0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 1], [0, 1, 2], [0, 2, 2],
    [1, 1, 1], [1, 1, 2], [1, 2, 2], [2, 2, 2]
    
    (Since the initial position is counted as a part of the "wiggle room",
    "wiggle room"-1 = "extra wiggle room")
    In short, we keep on adding to the one on the right until it's equal to
    the "extra wiggle room".
    Then, when that gets too big, we go to the number to our left until we find
    one that's less than the "extra wiggle room".
    (If we can't find one, we're done)
    We then take that number, increase it by one,
    and then set all the numbers to its right to be equal to it
    (this is that "push" or "forced shift")
    and then continue increasing the rightmost number.
    
    And that's the pattern that this follows; it works for any number of blocks
    of any length in any length band.
    
    (In the Lua version, what was called blocks here is a "chain" there and what
    was called units here is "blocks" there.)
    '''
    def generatePossibilities(puzzle, length):
        def addPosition(ans, startIndexes, puzzle, length):
            position = [0]*length
            #go through each starting position
            for i, start in enumerate(startIndexes):
                #add the blocks starting at that position
                for j in range(start, start+puzzle[i]):
                    position[j] = 1
            #add the position
            ans.append(position)
            
        ans = [] #this will be the list of all the possibilities
        lastIndexOfStarts = len(puzzle)-1 #how many blocks there are
        initPosition = [0]*(lastIndexOfStarts+1) #the initial position for the blocks
        
        #set up initPosition
        #We can ignore the last block because we
        #only need to know when it starts.
        for i, puzVal in enumerate(puzzle[:-1]):
            initPosition[i+1] = initPosition[i]+puzVal+1
        
        #initiate addToInit
        addToInit = [0]*(lastIndexOfStarts+1)
        
        #extraWiggleRoom = "length of band"-"space taken up by initial position"
        extraWiggleRoom = length-(initPosition[-1]+puzzle[-1])
        
        #keep on making new positions
        while True:
            newStart = [0]*(lastIndexOfStarts+1)
            for index, val in enumerate(addToInit):
                newStart[index] = initPosition[index]+val
                
            #add the position to the list
            addPosition(ans, newStart, puzzle, length)
            
            #updateIndex is the index we're trying to add one to.
            updateIndex = lastIndexOfStarts
            #keep on trying to find the next position
            while True:
                if addToInit[updateIndex]<extraWiggleRoom:
                    addToInit[updateIndex]+=1
                    if updateIndex<lastIndexOfStarts:
                        val = addToInit[updateIndex]
                        for i in range(updateIndex+1, lastIndexOfStarts+1):
                            addToInit[i] = val
                    break
                elif updateIndex==0: #all done
                    return ans
                else:
                    updateIndex-=1

    #get a band from the board
    def getBand(rowOrCol, index):
        if rowOrCol==0: #it's a row
            return board[index]
        else: #its a column
            ans = []
            for row in board:
                ans.append(row[index])
            return ans
    
    #update which rows and columns it should check based on
    #which slots have new info
    def updateChecks(old, new, rowOrCol, toCheck):
        #all the bands on one side (all row puzzles, or all column puzzles)
        sideBands = toCheck[oppositeRowOrCol(rowOrCol)]
        for index, oldVal in enumerate(old):
            if new[index]!=oldVal:
                sideBands.append(index)
    
    #upload the new updated band to the board
    def updateBand(band, board, rowOrCol, index):
        if rowOrCol == 0: #row
            board[index] = band
        else: #column
            for i, val in enumerate(band):
                board[i][index] = val
    
    #use the information from the band to update which possibilites still exist
    #it just eliminates impossible possibilities from the list
    #by the end, this should leave one list left - the solution for that band
    def getUpdatedBand(band, posses):
        length = len(posses[0])
        
        #list of indicies and values that need to be checked
        #(info that is certain)
        watchSlots = []
        for i, val in enumerate(band):
            if val!=2: #if it's certain (either 0 or 1)
                watchSlots.append((i, val)) #add it
        
        #remove the possiblities that are impossible given the band info
        
        #store the possibilities to remove since I'm iterating through the list
        #and removing them as we go would mess up the loop
        toRemove = []
        #if we actually have some info
        if len(watchSlots)>0:
            #go through each possibility
            for index, poss in enumerate(posses):
                #go through each certain value
                for check in watchSlots:
                    #if the possibility doesn't have the needed value
                    if poss[check[0]]!=check[1]:
                        toRemove.append(index)
                        break
                        
            #the list is reversed so that when removing possibilities,
            #the indexes dont change as we traverse the loop
            for index in reversed(toRemove):
                posses.pop(index)
        
        #check to see if the new info helped
        #compare all the possibilities and see what they have in common
        #the band it returns has only the stuff they all have in common
        #and then 2s to fill the rest
        #this is the workhorse of the algorithm that actually solves it.
        info = []
        #go through each slot in each of the possibilities
        for i in range(length):
            #the value it's checking to see if all of them equal
            curVal = None
            #if all the values have matched the initial so far
            good = True
            #check to make sure each possibility has the same value at index i
            for poss in posses:
                val = poss[i]
                #set initial value to look for if one has not been set yet
                if curVal==None:
                    curVal = val
                #check to make sure it's the same as the rest
                else:
                    if val!=curVal:
                        good = False
                        break
            #actual info that can be used to solve the puzzle
            if good:
                info.append((i, curVal))
        
        #initiate it filled with 2s cause it doesn't know anything    
        updatedBand = [2]*length
        #fill in the info it knows has to be there
        for pair in info:
            updatedBand[pair[0]] = pair[1]
        
        return updatedBand
                    
    #allPosses is short for "all possibilities"
    def update(rowOrCol, toCheck, allPosses): 
        #the next band to check
        try:
            checkBandIndex =  toCheck[rowOrCol].pop()
        except IndexError:
            #If theres no band there, just return.
            #This can happen if only one of the rows or column is empty
            #(the calling function simply checks if both of them are empty)
            return
        
        
        posses = allPosses[rowOrCol][checkBandIndex]
        band = getBand(rowOrCol, checkBandIndex)
        
        #update the possibilities for the band
        updatedBand = getUpdatedBand(band, posses)
        
        #tell it to eventually check the rows and columns that now have new info
        updateChecks(band, updatedBand, rowOrCol, toCheck)
        
        updateBand(updatedBand, board, rowOrCol, checkBandIndex)
        

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
    #As the program continues, the amount of orientations will shrink until it
    #only holds one possibility per puzzle.
    #possibilities is in the same format as puzzle:
    #[[row1Possibilities, row2Possibilities, ...], [column1Possibilities, column2Possibilities, ...]]
    possibilities = []
    for rowOrCol, bandPuzzles in enumerate(puzzle):
        possesToAdd = [] #short for 'possibilities to add'
        #the length of this band
        #if its a row, we care about the width,
        #and if it's a column, we care about the height.
        #Thus, the use of oppositeRowOrCol.
        bandLength = boardDimensions[oppositeRowOrCol(rowOrCol)]
        for bandPuzzle in bandPuzzles:
            possesToAdd.append(generatePossibilities(bandPuzzle, bandLength))
        possibilities.append(possesToAdd)
    
    rCheck = [] #the indexes of the rows to look at
    cCheck = [] #the indexes of the columns to look at
    toCheck = [rCheck, cCheck]
    #make sure every row and column is looked at at least once before ending
    for i in range(boardDimensions[0]):
        rCheck.append(i)
    for i in range(boardDimensions[1]):
        cCheck.append(i)
    
    #rowOrCol is 0 if a row should be checked, 1 if column
    #it alternates because filling in a row only affects columns and vice versa
    rowOrCol = 1
    while len(cCheck)>0 and len(rCheck)>0: #there's stuff left to check
        update(rowOrCol, toCheck, possibilities)
        rowOrCol = oppositeRowOrCol(rowOrCol)
    return board

def displayBoard(board):
    import colorama as color
    '''
    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL
    '''
    color.init()
    for row in board:
        line = color.Fore.BLUE+""
        for val in row:
            if val==1:
                c = color.Back.BLACK
            elif val==0:
                c = color.Back.WHITE
            else:
                c = color.Back.RED
            line+=(c+str(val)+color.Back.RESET+" ")
        print(line+color.Style.RESET_ALL)
    
    

def GUI():
    def main():
        def getInput(recordList):
            while True:
                info = raw_input().split()
                for i, val in enumerate(info):
                    try:
                        info[i] = int(val)
                    except ValueError:
                        return
                recordList.append(info)
            
            
        puzzle = [[], []]
        
        listOrPuzzle = raw_input("Do you have a full list to type in, or a \
puzzle to type in by hand? (list/puzzle) ").strip().lower()
        if listOrPuzzle=="list":
            while True:
                print("Please enter the list. (Make sure it's only one line)")
                try:
                    import ast
                    puzzle = ast.literal_eval(raw_input())
                    break
                except:
                    print("Sorry, that list didn't work for me. Restarting...")
                    main()
                    return
        elif listOrPuzzle=="puzzle":
            print("Please enter in the rows to your puzzle, where the numbers \
are separated by spaces.\nHit enter when finished with a row.\nWhen done with \
all rows, type anything with a letter or symbol in it, then hit enter.")
            getInput(puzzle[0])
            print("Now enter in the columns to the puzzle, following the same \
pattern.")
            getInput(puzzle[1])
            print("Here's the list I was able to make:")
            print(puzzle)
        else:
            print("Sorry, I didn't quite get that.")
            main()
            return
            
        try:
            solution = solve(puzzle)
            print("Here's the solution:")
            displayBoard(solution)
        except:
            print("Sorry, I couldn't solve that. Restarting...")
            main()
            return
            
        while True:
            playAgain = raw_input("Would you like to solve another one?(y/n) ")\
                        .strip().lower()
            if playAgain == "y" or playAgain == "yes":
                main() #so it doesn't go through the intro again.
                return
            elif playAgain=="n" or playAgain=="no":
                return
            else:
                print("Sorry, I didn't quite get that.")
        
    def intro():
        print("Welcome to the nonogram solver!")
        main()
        
    intro()

GUI()
    
    

