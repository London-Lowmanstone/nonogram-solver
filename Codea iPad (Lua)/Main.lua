-- July 7th, 2016
-- by Jadiker
-- Codea Nonogram Solver

--# Main
-- Use this function to perform your initial setup
function setup()
    solver = NonologixSolver()
    input = {{},{}}
    inputMode = 0
end

-- This function gets called once every frame
function draw()
    if inputMode==0 then
        showKeyboard()
        inputMode = inputMode + 1
    elseif inputMode<3 then
        tbl = input[inputMode]
        background(40,40,50)
        fill(255)
        textMode(CORNER)
        kbuff = keyboardBuffer()
        _,bufferHeight = textSize(kbuff)
        if kbuff then
            text(kbuff, 10, HEIGHT - 30 - bufferHeight )
        end
    elseif inputMode==3 then
        hideKeyboard()
        -- printStuff(input, input[1], input[2])
        ans = solver:solve(unpack(input))
        print("Answer!")
        printStuff(ans)
        inputMode = inputMode + 1
    else
        background(0, 0, 255, 255)
        -- ans = solver:solve({{1,5},{4},{1,2,2},{4,1},{4},{1,1,3},{3,1},{3},{2,3,2},{6,2}}, {{1,1,1,2},{2},{1,1},{4,5},{5,4},{2,3,3},{2,4},{1,2},{2,2},{1,2}})
        drawAnswer(ans)
    end
    -- This sets a dark background color 
    
end

function touched(t)
    if t.state == BEGAN then
        -- print("tapcount", t.tapCount)
        if t.tapCount==1 then
            -- print("kbuff", kbuff)
            if kbuff~="" then
                print("running")
                local worked = loadstring("table.insert(tbl, {"..kbuff.."})")
                if worked then
                    worked()
                    -- print("{"..kbuff.."}")
                    printStuff(tbl)
                    -- printStuff(input)
                else
                    print("failed")
                    print(worked)
                end
                -- print("done running")
                hideKeyboard()
                showKeyboard()
            end
        elseif t.tapCount==2 then
            print("Next!")
            inputMode = inputMode + 1
        end
    end
end
--[[

function touched(touch)
    --Show keyboard when the screen is touched
    showKeyboard()
end

function draw()
    background(40,40,50)
    fill(255)
    textMode(CORNER)
    buffer = keyboardBuffer()
    
    _,bufferHeight = textSize(buffer)
    
    if buffer then
        text( buffer, 10, HEIGHT - 30 - bufferHeight )
    end
end

  ]]
