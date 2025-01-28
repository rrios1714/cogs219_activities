from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#grassy field
field = visual.ImageStim(win,image="stimuli/images/GrassyField.png",size=[800,800])

#create an image
bulbie = visual.ImageStim(win,image="stimuli/images/bulbasaur.png",size=[200,200])

# create a mouse
mouse = event.Mouse(win=win)

#show the image
field.draw()
bulbie.draw()
win.flip()

#make bulbie draggable
max_time = 10
dragging_timer = core.Clock()
dragging_timer.reset()

while dragging_timer.getTime() <= max_time:
    while mouse.isPressedIn(bulbie):
        bulbie.pos = mouse.getPos()
        field.draw()
        bulbie.draw()
        bulbie.win.flip()
        if dragging_timer.getTime() > max_time:
            break

print(dragging_timer.getTime())

win.close() #close the window
core.quit() #quit out of the program

