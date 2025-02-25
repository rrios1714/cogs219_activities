from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os

#open a window
win = visual.Window([600,600],color="white", units='pix', checkTiming=False) 

#create a blue circle
circle = visual.Circle(win,lineColor="black",fillColor="white",size=[300,300],autoDraw=True)


#show the blue circle
circle.draw()
#then "flip" the window to show what you just drew
win.flip()

# create a mouse
mouse = event.Mouse(win=win)

#make bulbie draggable
max_time = 10
dragging_timer = core.Clock()
dragging_timer.reset()
paint_circle_list = []

while dragging_timer.getTime() <= max_time:
    while mouse.isPressedIn(circle):
        paint_circle = visual.Circle(win,lineColor=None,fillColor="red",size=[10,10],opacity=0.5,autoDraw=True)
        paint_circle.pos = mouse.getPos()
        paint_circle.draw()
        win.flip()
        paint_circle_list.append(paint_circle)

print(paint_circle_list)
#take a screenshot and save it
win.getMovieFrame()
cur_dir = os.path.dirname(os.path.abspath(__file__))
win.saveMovieFrames(os.path.join(cur_dir,'frames','drawing.png'))

#showing how to turn off autodraw and clear the screen
for cur_circle in paint_circle_list:
    cur_circle.autoDraw = False
win.flip()
core.wait(2.0)

win.close() #close the window
core.quit() #quit out of the program