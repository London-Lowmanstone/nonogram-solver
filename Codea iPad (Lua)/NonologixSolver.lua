-- July 7th, 2016
-- by Jadiker
-- Codea Nonogram Solver

--# NonologixSolver
NonologixSolver = class()

-- rPuz is the table of tables {row1puzzle, row2puzzle, etc.} where row1puzzle is something like {1, 2, 3} describing that there should be one block followed by 2 blocks followed by 3 blocks in row 1. cPuz is the same thing but for columns.
function NonologixSolver:solve(rPuz, cPuz)
    -- printStuff("solving", "rPuz", rPuz, "cPuz", cPuz)
    self.board = {}
    self.board.width = table.maxn(cPuz)
    self.board.height = table.maxn(rPuz)
    self.board.dimensions = {self.board.height, self.board.width}
        -- setup the board (row-major)
    -- inside the board, 0 means nothing goes in this slot, 1 means a block is in the slot, and 2 means its not sure yet.
    local blankRow = {}
    for i = 1, self.board.width do
        table.insert(blankRow, 2)
    end
    for i = 1,self.board.height do
        table.insert(self.board, copyTable(blankRow))
    end
    
    self.rPuz = deepcopyTable(rPuz)
    self.cPuz = deepcopyTable(cPuz)
    self.puzzle = {self.rPuz, self.cPuz}
    -- makes it so each band puzzle (like row1puzzle above) is replaced by a table of all the possible ways the band could be. If it were a 8 by 8 and the band puzzle was {1,2,3}, after this, it would look like {{1,0,1,1,0,1,1,1}}, because there'd only be one option. the more possibilities there are, the bigger that outer table gets.
    for rOrC, puzList in pairs(self.puzzle) do
        for i, bandPuz in pairs(puzList) do
            puzList[i] = self:generatePosses(bandPuz, self.board.dimensions[self:getOpp_rOrC(rOrC)]) -- get the opposite dimension because the puzzle for the row has slots to fill equal to the width.
        end
    end
    
    -- printStuff("puzzle!",self.puzzle)
    -- the tables that store what rows and columns should be checked next
    self.rCheck = {}
    self.cCheck = {}
    self.toCheck = {self.rCheck, self.cCheck}
    -- make sure every row and column is looked at at least once before ending
    for i = 1, self.board.height do
        table.insert(self.rCheck, i)
    end
    for i = 1, self.board.width do
        table.insert(self.cCheck, i)
    end
    -- rOrC is 1 if a row should be checked, and 2 if a column should be.
    -- it alternates because filling in a row only affects columns and vice versa
    local rOrC = 1
    while table.maxn(self.cCheck)>0 and table.maxn(self.rCheck)>0 do
        self:update(rOrC)
        rOrC = self:getOpp_rOrC(rOrC) -- get the opposite one
    end
    return self.board
end

-- get the opposite rOrC
function NonologixSolver:getOpp_rOrC(rOrC)
    return rOrC%2+1
end

-- rOrC is short for "row or column" if its a 1, update a row, if its a -1, update a column
-- simple functions are defined inside this, more complicated functions I made i to methods.
function NonologixSolver:update(rOrC)
    -- printStuff("update started","puzzle",self.puzzle, "board", self.board)
    -- printStuff("update started", "board", self.board, "toCheck", self.toCheck)
    -- printStuff("update started", "self.toCheck", self.toCheck)
    -- number of the row or column being updated
    local num = table.remove(self.toCheck[rOrC])
    -- printStuff("rOrC", rOrC, "num", num)
    if not num then return end -- if theres no row or column left, just return.
    local posses = self.puzzle[rOrC][num]
    -- since i dont know whether its a row or a column, im just going to call it a band at this point
    local band = self:getBand(rOrC, num)
    -- printStuff("posses before passed", posses, "band", band, "self.puzzle[rOrC]", self.puzzle[rOrC])
    local updatedBand = self:getUpdatedBand(band, posses)
    -- printStuff("updated band", updatedBand)
    self:updateChecks(band, updatedBand, rOrC)
    self:updateBand(updatedBand, rOrC, num)
    -- printStuff("update ending", "old band", band, "new band", updatedBand, "board", self.board)
end

function NonologixSolver:getBand(rOrC, num)
    -- printStuff("getBandStarted", "rorc", rOrC, "num", num)
    if rOrC == 1 then -- its a row
        return copyTable(self.board[num]) -- don't want it to accidentally modify the board, so the table is copied before being sent. This may be removeable.
    else -- its a column
        ans = {}
        for _, row in ipairs(self.board) do
            table.insert(ans, row[num])
        end
        return ans
    end
end

-- todo test this
function NonologixSolver:updateChecks(old, new, rOrC)
    local tbl = self.toCheck[self:getOpp_rOrC(rOrC)]
    for i, val in pairs(old) do
        if new[i]~=val then
            table.insert(tbl, i)
        end
    end
end

function NonologixSolver:updateBand(band, rOrC, num)
    -- printStuff("updateBand started", "rOrC", rOrC, "num", num, "board", self.board)
    if rOrC == 1 then -- row
        self.board[num] = band
    else -- column
        for i, val in ipairs(band) do
            -- print("updating", i, num, val)
            self.board[i][num] = val
            -- printStuff(self.board[i])
            -- printStuff(self.board)
        end
    end
    -- printStuff("updateBand ending", "board", self.board)
end

-- band is the current band stored in the board.
-- posses is short for possibilities and has all the possible orientations of this band
function NonologixSolver:getUpdatedBand(band, posses)
    -- printStuff("getUpdatedBand started", "band", band, "posses", posses)
    local length = table.maxn(posses[1])
    -- first, ingest new information
    local watchSlots = {} -- table of indicies and values that need to be checked
    for i, val in pairs(band) do
        if val~=2 then
            table.insert(watchSlots, {i,val})
        end
    end
    -- printStuff("watchSlots", watchSlots)
    local toRemove = {}
    -- nts:if switching to ipairs, be careful with that remove inside the loop
    -- remove all the possibilities that dont match the new info
    if table.maxn(watchSlots)>0 then -- if this isnt at the beginning.
        for i, poss in ipairs(posses) do
            -- printStuff("poss",poss)
            for j, check in pairs(watchSlots) do
                if poss[check[1]]~=check[2] then
                    -- make the table go in reverse order so that when removing possibilities from the big table, the indexes dont switch as they're removed
                    table.insert(toRemove, 1, i)
                    break
                end
            end
        end

        -- printStuff("toremove", toRemove)
        for _, index in pairs(toRemove) do
            -- printStuff("removed table!", posses[index])
            table.remove(posses, index)
        end
    end

    
    -- printStuff("posses after removals", posses)
    -- then, check to see if the new info helped.
    -- todo figure out how to skip to bottom of loop
    local info = {}
    for i=1, length do
        local curVal = nil
        local good = true
        for _, poss in pairs(posses) do
            
            local val = poss[i]
            curVal = curVal or val -- default val
            if val~=curVal then
                good = false
                break
            end
        end
        if good then
            table.insert(info, {i, curVal})
        end
    end

    newBand = {}
    for i=1,length do
        table.insert(newBand, 2)
    end
    for _, pair in pairs(info) do
        newBand[pair[1]] = pair[2]
    end
    return newBand
end

function NonologixSolver:generatePosses(puz, length)
    function addPos(bigAns, startIndexes, puz, length)
        -- create the posibility
        -- printStuff("Start indexes:", startIndexes)
        local ans = {}
        for i=1,length do
            table.insert(ans, 0)
        end
        for i, start in pairs(startIndexes) do
            for j=start, start+puz[i]-1 do
                ans[j] = 1
            end
        end
        -- printStuff("result:", ans)
        
        -- add the posibility
        table.insert(bigAns, ans)        
    end
    
    -- printStuff("generateposses started", "puz", puz, "length", length)
    
    local ans = {}
    local start = {} -- indicies where the puzzle blocks start
    local space = 0
    local chainAmt = table.maxn(puz) -- how many chains of blocks there are
    
    -- add up the space the blocks take up on thier own
    for i, val in pairs(puz) do
        space = space + val
    end
    -- printStuff("init", space)
    -- set space to be ((the total room) - (space taken up by blocks) - (space taken up by space between the block sets) + 1 for the original slot they occupy) This means that space = amount of movement space the blocks have to move
    space = length - space - (table.maxn(puz) - 1) + 1-- how many places each block can move around
    -- print("maxn(puz)",table.maxn(puz),"length", length)
    -- print("space", space)
    
    -- set up start
    for i=1, chainAmt do
        if i==1 then
            start[1]=1
        else
            table.insert(start, start[i-1]+puz[i-1]+1)
        end
    end
    
    -- printStuff("start", start)
    
    local addToStart = {}
    
    for i=1,chainAmt do
        table.insert(addToStart, 0)
    end

    while true do
        
        -- add a new possibility to ans, whose starting indexes are start+addToStart (added element-wise)
        local newStart = {}
        -- printStuff("err", start, addToStart)
        -- print(space)
        for i=1,chainAmt do
            newStart[i] = start[i]+addToStart[i]
        end
        -- printStuff("addToStart",addToStart)
        
        addPos(ans, newStart, puz, length) -- todo w
        
        -- update addToStart. if space is 3, addToStart should follow the following pattern
        -- {0,0,0}, {0,0,1}, {0,0,2}, {0,1,1}, {0,1,2}, {0,2,2},
        -- {1,1,1}, {1,1,2}, {1,2,2},
        -- {2,2,2}
        updateIndex = chainAmt
        while true do
            if addToStart[updateIndex]<space-1 then
                addToStart[updateIndex] = addToStart[updateIndex] + 1
                if updateIndex<space then -- just a small time-saver catch
                    local val = addToStart[updateIndex]
                    for i=updateIndex+1,chainAmt do
                        addToStart[i]=val
                    end
                end
                break
            elseif updateIndex==1 then -- all done
                -- print("tried to break!")
                return ans
            else
                -- print("tried to bump up!")
                updateIndex = updateIndex - 1
            end
        end
    end
end
