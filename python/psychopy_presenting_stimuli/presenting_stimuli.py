from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#positions
positions = {"left": (-200,0),"right": (200,0)}

#create images
image_path_1 = os.path.join(os.getcwd(),"stimuli","images","bulbasaur.png")
image_path_2 = os.path.join(os.getcwd(),"stimuli","images","charmander.png")

image_1 = visual.ImageStim(win,image=image_path_1,size=[200,200],pos=positions["left"])
image_2 = visual.ImageStim(win,image=image_path_2,size=[200,200],pos=positions["right"])

# draw images
image_1.draw()
image_2.draw()

#show
win.flip()

#wait 5 seconds
core.wait(5)

win.close() #close the window
core.quit() #quit out of the program

