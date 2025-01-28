from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough

## Serial RT task - in progress

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#create a list of pokemon
pokemon = ["bulbasaur","charmander","mew","dratini"]

#### present each pokemon above a box

#create four boxes
box_positions = [(-300,-100),(-100,-100),(100,-100),(300,-100)]
box_list = [visual.Rect(win,fillColor="white",lineWidth=5,lineColor="black",size=[100,100],pos=box_position) for box_position in box_positions]
print(box_list)

#draw boxes
for box in box_list:
    box.draw()

#add labels
box_labels = ["1","2","3","4"]
text_position = {"1":(-300,-100),"2":(-100,-100),"3":(100,-100),"4":(300,-100)}
text_list = [visual.TextStim(win,text = box_label, color="black",height=75,pos=text_position[box_label]) for box_label in box_labels]
#draw labels
for text in text_list:
    text.draw()

# add Pokemon

#show
win.flip()

#wait 5 seconds
core.wait(5)

