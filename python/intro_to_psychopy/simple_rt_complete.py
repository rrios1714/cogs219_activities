from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough

#open a window
win = visual.Window([600,600],color="grey", units='pix', checkTiming=False) 

#create a general circle
circle = visual.Circle(win,lineColor="grey",fillColor="blue",size=[100,100])

#create the instruction text
instruction_text = "Press b if the circle is blue and o if the circle is orange."
instruction = visual.TextStim(win, text = instruction_text,color="black", pos = (0,-100))

# trial list
color_trials = ["blue","orange"]

#loop through the trial list
for current_color in color_trials:
    #update the current color
    circle.color = current_color
    #draw the circle
    circle.draw()
    #draw the instruction
    instruction.draw()
    #flip the window
    win.flip()

    #wait until the participant presses one of the keys from the key list
    key_pressed = event.waitKeys(keyList=['b','o'])
    #once they press one of those keys, print it out and flip the window (why?)
    if key_pressed:
        print(key_pressed)
        win.flip()

    #wait one second after the response
    core.wait(1)

