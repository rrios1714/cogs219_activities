from psychopy import visual, event, core, sound # import the bits of PsychoPy we'll need for this walkthrough
import os

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

# add a Mouse
mouse = event.Mouse(win=win)

#positions
positions = {"left": (-200,0),"right": (200,0)}

# add a rectangular frame
# there's a lot going on here: list comprehension over the keys of a dictionary - make sure you understand how this works!
frame_list = [visual.Rect(win,fillColor="white",lineWidth=5,lineColor="black",size=[225,225],pos=positions[pos_key]) for pos_key in positions.keys()]

# add a text prompt
instruction_text = "Click on the bulbasaur."
instruction = visual.TextStim(win, text = instruction_text,color="white", height=30, pos = (0,-150))

#create images
image_path_1 = os.path.join(os.getcwd(),"stimuli","images","bulbasaur.png")
image_path_2 = os.path.join(os.getcwd(),"stimuli","images","charmander.png")

image_1 = visual.ImageStim(win,image=image_path_1,size=[200,200],pos=positions["left"])
image_2 = visual.ImageStim(win,image=image_path_2,size=[200,200],pos=positions["right"])

#add feedback
correct_feedback = visual.TextStim(win, text = "Correct!",color="white", height=30, pos = (0,0))
incorrect_feedback = visual.TextStim(win, text = "Incorrect.",color="white", height=30, pos = (0,0))

# add audio feedback
correct_feedback_sound_path = os.path.join(os.getcwd(),"stimuli","sounds","bleep.wav")
correct_feedback_sound = sound.Sound(correct_feedback_sound_path)
incorrect_feedback_sound_path = os.path.join(os.getcwd(),"stimuli","sounds","buzz.wav")
incorrect_feedback_sound = sound.Sound(incorrect_feedback_sound_path)

# draw boxes
for frame in frame_list:
    frame.draw()

#draw instruction
instruction.draw()

# draw images
image_1.draw()
image_2.draw()

#show
win.flip()

#check mouse until pressed in one of the pics
while True:
     if mouse.isPressedIn(image_1) or mouse.isPressedIn(image_2):
            response = mouse.getPos()
            break

# present feedback
if image_1.contains(response):
     #correct
     correct_feedback.draw()
     correct_feedback_sound.play() 
else:
     #incorrect
     incorrect_feedback.draw()
     incorrect_feedback_sound.play()

win.flip()

#wait 2 seconds
core.wait(2)

win.close() #close the window
core.quit() #quit out of the program

