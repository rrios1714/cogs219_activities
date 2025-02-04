from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#positions
positions = {"center": (0,0)}

#create image
image_path = os.path.join(os.getcwd(),"stimuli","images","1_0_R.jpg")
image = visual.ImageStim(win,image=image_path,size=[400,214],pos=positions["center"])

# draw image
image.draw()

#show
win.flip()

#wait until the participant presses one of the keys from the key list
key_pressed = event.waitKeys(keyList=['z','m'])
#once they press one of those keys, print it out and flip the window (why?)
if key_pressed:
    print(key_pressed)
    win.flip()

#trial-end wait seconds
core.wait(0.5)

win.close() #close the window
core.quit() #quit out of the program

