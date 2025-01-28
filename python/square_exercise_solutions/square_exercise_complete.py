import time
import sys
from psychopy import visual,event,core # import the bits of PsychoPy we'll need for this exercise

win = visual.Window([400,400],color="black", units='pix',checkTiming=False) #open a window
left_square = visual.Rect(win,lineColor="black",fillColor="blue",size=[100,100],pos = (-100,0)) #create a Rectangle type object with certain parameters
right_square = visual.Rect(win,lineColor="black",fillColor="blue",size=[100,100],pos = (100,0)) #create a Rectangle type object with certain parameters

spinning = True
while True:
    if spinning:
        left_square.ori += 6
        left_square.draw()
        right_square.ori += -6
        right_square.draw()
        win.flip()
    if event.getKeys('s'):
        spinning = False
    if event.getKeys('r'):
        spinning = True
    if event.getKeys('q'):
        break

win.close() #close the window -- don't need this if you're running this as a separate file
core.quit() #quit out of the program -- don't need this if you're running this as a separate file