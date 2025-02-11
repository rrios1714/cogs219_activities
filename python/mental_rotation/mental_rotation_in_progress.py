from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os
from helper import load_files, get_runtime_vars
from gen_trials import generate_trials

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False,screen=1) 

# get runtime variables
order = ["subj_code","seed","gender"]
runtime_vars = get_runtime_vars({'subj_code':'mr_101','seed': 10, 'gender':['Choose','male',"gender","nonbinary","other"]},order)
print(runtime_vars)

# generate trials
generate_trials(runtime_vars["subj_code"],runtime_vars["seed"])

#positions
positions = {"center": (0,0)}

#preload
images_dictionary = load_files(os.path.join(os.getcwd(),"stimuli","images"),".jpg",fileType="image",win=win)
print(images_dictionary)
print(images_dictionary["1_0_R"])

#draw image
cur_image = images_dictionary["16_150_R"]['stim']
cur_image.size = cur_image.size * 0.5
cur_image.draw()

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

