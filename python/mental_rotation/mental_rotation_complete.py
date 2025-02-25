from psychopy import visual, event, core, sound, gui # import the bits of PsychoPy we'll need for this walkthrough
import os
from generate_trials import generate_trials
from helper import get_runtime_vars, import_trials, load_files, get_keyboard_response
#generate trials

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#get runtime variables
order =  ['subj_code','seed','test_mode']
runtime_vars= get_runtime_vars({'subj_code':'mr_101', 'seed':10, 'test_mode':['Choose', 'practice','real']}, order)
print(runtime_vars)

# generate trials
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['test_mode'])

#positions
positions = {"center": (0,0)}
separator=","

#preload
cur_dir = os.path.dirname(os.path.abspath(__file__))
print(cur_dir)
images_dictionary = load_files(os.path.join(cur_dir,"stimuli","images"),'.jpg',fileType="image",win=win)

#add feedback
correct_feedback = visual.TextStim(win, text = "Correct!",color="white", height=30, pos = (0,0))
incorrect_feedback = visual.TextStim(win, text = "Incorrect.",color="white", height=30, pos = (0,0))

# add a fixation cross
fixation_cross = visual.TextStim(win, text = "+",color="black", height=40, pos = (0,0))
fixation_cross_duration = .3

# add audio feedback
correct_feedback_sound_path = os.path.join(os.getcwd(),"stimuli","sounds","bleep.wav")
correct_feedback_sound = sound.Sound(correct_feedback_sound_path)
incorrect_feedback_sound_path = os.path.join(os.getcwd(),"stimuli","sounds","buzz.wav")
incorrect_feedback_sound = sound.Sound(incorrect_feedback_sound_path)

#read in trials
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)

#open file to write data to and store a header
data_file = open(os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv'),'w')
header = separator.join(["subj_code","seed", 'image_name','item','angle','match','correct_response','response','rt'])
data_file.write(header+'\n')

#show instructions
instruction_text = "Welcome to the experiment!\n\nPress the space bar to continue."
instruction = visual.TextStim(win, text = instruction_text,color="white", height=30, pos = (0,0))
instruction.draw()
win.flip()
#wait for the space key
event.waitKeys(keyList=['space'])
win.flip()
core.wait(.5)

# trial loop
responseTimer = core.Clock()
for cur_trial in trial_list:

    #define current image
    cur_image_name = cur_trial['image_name']
    cur_image = images_dictionary[cur_image_name]['stim']

    #set size
    print(cur_image.size)
    cur_image.size = cur_image.size * 0.5
    #cur_image.size = [400,214]
    
    #draw fixation cross
    fixation_cross.draw()
    
    #show
    win.flip()
    core.wait(fixation_cross_duration)
    
    #draw image
    cur_image.draw()
    
    #show
    win.flip()

    #wait until the participant presses one of the keys from the key list
    event.clearEvents()
    responseTimer.reset()
    key_pressed = event.waitKeys(keyList=['z','m'],timeStamped=responseTimer)
    #once they press one of those keys, print it out and flip the window (why?)
    if key_pressed:
        print(key_pressed)
        response=key_pressed[0][0]
        rt = key_pressed[0][1]*1000
        win.flip()

    # present feedback
    cur_correct_response = cur_trial['correct_response']
    if response == cur_correct_response:
        #correct
        correct_feedback.draw()
        win.flip()
        correct_feedback_sound.play() 
        core.wait(0.3)
        correct_feedback_sound.stop() 
    else:
        #incorrect
        incorrect_feedback.draw()
        
        win.flip()
        incorrect_feedback_sound.play()
        core.wait(0.3)
        incorrect_feedback_sound.stop() 
    
    #writing a response
    print([_ for _ in cur_trial])
    response_list=[cur_trial[_] for _ in cur_trial]
    print(response_list)
	#write dep variables
    response_list.extend([
			response,rt])
    responses = map(str,response_list)
    print(response_list)
    line = separator.join([str(i) for i in response_list])
    data_file.write(line+'\n')
    
    #trial-end wait seconds
    core.wait(0.5)
    
    win.flip()

data_file.close()
win.close() #close the window
core.quit() #quit out of the program

