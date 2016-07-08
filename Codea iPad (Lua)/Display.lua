-- July 7th, 2016
-- by Jadiker
-- Codea Nonogram Solver

--# Display
Block = class()

function Block:init(x, y, w, h, colorNum)
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    if colorNum==0 then
        self.myColor = color(255,255,255)
    elseif colorNum==1 then
        self.myColor = color(0,0,0)
    else
        self.myColor = color(255, 0, 0)
    end
end

function Block:draw()
    pushBoth()
    rectMode(CORNER)
    fill(self.myColor)
    stroke(self.myColor)
    rect(self.x, self.y, self.w, self.h)
    popBoth()
end

function drawAnswer(answer, w, h, x, y)
    w = w or 300
    h = h or 300
    x = x or WIDTH/2
    y = y or HEIGHT/2
    r = table.maxn(answer)
    c = table.maxn(answer[1])
    bh = h/r
    bw = w/c
    px = x - w/2 - bh
    py = y + h/2
    for i, row in ipairs(answer) do
        
        for j, val in ipairs(row) do
            Block(px+(j-1)*bw, py-(i-1)*bh, bw, bh, val):draw()
        end
    end
    
end