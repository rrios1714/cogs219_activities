import time
import sys
from psychopy import visual,event,core # import the bits of PsychoPy we'll need for this exercise

win = visual.Window([400,400],color="black", units='pix',checkTiming=False) #open a window

#4- creating the figure
squares = visual.Rect(win,lineColor="grey", size = [100,100])

#list of colors, 3 is three times run through the colors
colors_set = ["blue","red"]*3
print(colors_set)

#the for loop
for present_color in colors_set:
    #present the color first
    squares.color = present_color
    squares.draw()
    core.wait(1.0)
    win.flip()
    core.wait(0.5)
    win.flip()

#square = visual.Rect(win,lineColor="black",fillColor="red",size=[100,100]) #create a Rectangle type object with certain parameters
#blue_sq = visual.Rect(win,lineColor = "black", fillColor="blue",size=[100,100]) 


#square.draw() #draw the square to the screen buffer, starting the red sq
#win.flip() #make the buffer visible, i.e., show what's been drawn to it
#core.wait(1.5) #pause for half a second (i.e., 500 ms)
#blue_sq.draw()
#win.flip()
core.wait(1.0)

win.close() #close the window -- don't need this if you're running this as a separate file
core.quit() #quit out of the program -- don't need this if you're running this as a separate file