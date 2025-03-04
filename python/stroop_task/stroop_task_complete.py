import time
import sys
import os
import random
from psychopy import visual,event,core,gui
from generate_trials import generate_trials

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
valid_response_keys = ['r', 'o', 'y', 'g', 'b']
trial_types = ['congruent','incongruent']

def popupError(text):
    errorDlg = gui.Dlg(title="Error", pos=(200,400))
    errorDlg.addText('Error: '+text, color='Red')
    errorDlg.show()

def open_data_file(filename):
    """
    Open data file, creating data/ directory as necesasry
    """
    if os.path.isfile(filename):
        popupError(f'Error {filename} already exists')
        return False
    else:
        try:
            data_file = open(filename,'w')
        except FileNotFoundError:
            print(f'Could not open {filename} for writing')
    return data_file

#function for collecting runtime variables
#now throws an error if the data file already exists
def get_runtime_vars(vars_to_get,order,exp_version="Exercise 3"):
    """
    Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    Return filled in runtime variables and an opened data file
    """
    while True:
        infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order,copyDict=True) 
        populated_runtime_vars = infoDlg.dictionary 
        data_file = open_data_file(os.path.join(os.getcwd(),'data',populated_runtime_vars['subj_code']+'_data.csv'))
        if 'Choose' in list(populated_runtime_vars.values()):
            popupError('Need to choose a value from each dropdown box')
        elif infoDlg.OK and data_file:
            return populated_runtime_vars
        elif not infoDlg.OK:
            print('User Cancelled')
            sys.exit()

#function for reading in trials
def import_trials(trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names) # make sure the number of column names = number of columns
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
#add fixation cross
fixation = visual.TextStim(win,height=40,color="black",text="+")
# add a new feedback TextStim before the while loop
feedback_incorrect = visual.TextStim(win,text="INCORRECT", height=40, color="black",pos=[0,0])
feedback_too_slow = visual.TextStim(win,text="TOO SLOW", height=40, color="black",pos=[0,0])

# get the runtime variables
order =  ['subj_code','seed','num_reps']
runtime_vars = get_runtime_vars({'subj_code':'stroop_101','seed': 101, 'num_reps': 25}, order)
print(runtime_vars)

# generate a trial list
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['num_reps'])

#read in trials
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)
print(trial_list)

#open data file and write header
try:
    os.mkdir('data')
    print('Data directory did not exist. Created data/')
except FileExistsError:
    pass 
separator=","
data_file = open(os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv'),'w')
header = separator.join(['subj_code','seed', 'word','color','trial_type','orientation','trial_num','response','is_correct','rt'])
data_file.write(header+'\n')

response_timer = core.Clock() # set response timer clock
# trial loop
# add a trial number
trial_num = 1
for cur_trial in trial_list:

    cur_word = cur_trial['word']
    cur_color = cur_trial['color']
    trial_type = cur_trial['trial_type']
    cur_ori = cur_trial['orientation']

    word_stim.setText(cur_word) #set text
    word_stim.setColor(cur_color) #set color

    if cur_ori=='upside_down':
        word_stim.setOri(180)
    else:
        word_stim.setOri(0)

    #show fixation
    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(.5)

    #short inter stimulus interval
    placeholder.draw()
    win.flip()
    core.wait(.5)

    #draw word stimulus
    placeholder.draw()
    word_stim.draw()
    win.flip()

    #get response
    response_timer.reset() # immediately after win.flip(), reset clock to measure RT
    key_pressed = event.waitKeys(keyList=valid_response_keys,maxWait=2) # maximum wait time of 2 s
    rt = round(response_timer.getTime()*1000,0)

    # add feedback
    # if key_pressed is still FALSE/ no response was registered, present too slow feedback
    if not key_pressed:
        is_correct = 0
        response = "NA"
        feedback_too_slow.draw()
        win.flip()
        core.wait(1)
    elif key_pressed[0] == cur_color[0]: 
        is_correct = 1
        response = key_pressed[0]
        #correct response
        pass
    else:
        is_correct = 0
        response = key_pressed[0]
        feedback_incorrect.draw()
        win.flip()
        core.wait(1)
    
    #writing a response
    response_list=[cur_trial[_] for _ in cur_trial]
    print(response_list)
	#write dependent variables
    response_list.extend([trial_num,response,is_correct,rt])
    responses = map(str,response_list)
    print(response_list)
    line = separator.join([str(i) for i in response_list])
    data_file.write(line+'\n')

    # increment trial number
    trial_num += 1

#close the data file at the end of the experiment
data_file.close()