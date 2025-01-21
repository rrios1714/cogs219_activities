from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough

#open a window
win = visual.Window([600,600],color="grey", units='pix', checkTiming=False) 

#create a blue circle
blue_circle = visual.Circle(win,lineColor="grey",fillColor="blue",size=[100,100])

#show the blue circle
#first, draw the blue circle to the back buffer of the window
#this means that the blue circle won't be displayed right away
blue_circle.draw()
#then "flip" the window to show what you just drew
win.flip()

#wait 2 seconds
core.wait(2.0)

win.close() #close the window
core.quit() #quit out of the program

