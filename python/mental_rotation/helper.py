from psychopy import visual, event, core, gui 
import os
import glob

#runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="experiment_code_for_reference"):
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

def import_trials (trial_filename, col_names=None, separator=','):
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

def load_files(directory,extension,fileType,win='',restriction='*',stim_list=[]):
    """ Load all the pics and sounds. Uses pyo or pygame for the sound library (see prefs.general['audioLib'])"""
    path = os.getcwd() #set path to current directory
    if isinstance(extension,list):
        file_list = []
        for curExtension in extension:
            file_list.extend(glob.glob(os.path.join(path,directory,restriction+curExtension)))
    else:
        file_list = glob.glob(os.path.join(path,directory,restriction+extension))
    files_data = {} #initialize files_data  as a dict because it'll be accessed by file names (picture names, sound names)
    for num,curFile in enumerate(file_list):
        fullPath = curFile
        fullFileName = os.path.basename(fullPath)
        stimFile = os.path.splitext(fullFileName)[0]
        if fileType=="image":
            try:
                surface = pygame.image.load(fullPath) #gets height/width of the image
                stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
                (width,height) = (surface.get_width(),surface.get_height())
            except: #if no pygame, image dimensions may not be available
                pass
            stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
            (width,height) = (stim.size[0],stim.size[1])
            files_data[stimFile] = {'stim':stim,'fullPath':fullFileName,'filename':stimFile,'num':num,'width':width, 'height':height}
        elif fileType=="sound":
            files_data[stimFile] = {'stim':sound.Sound(fullPath), 'duration':sound.Sound(fullPath).getDuration()}
 
    #optionally check that the stimuli we *need* to load are actually available in the directory; return error if there is a discrepancy
    if stim_list and set(files_data.keys()).intersection(stim_list) != set(stim_list):
        popupError(str(set(stim_list).difference(list(files_data.keys()))) + " does not exist in " + path+'\\'+directory) 
    return files_data


#get keyboard response
def get_keyboard_response(validResponses,duration=0):
    event.clearEvents()
    responded = False
    done = False
    rt = '*'
    responseTimer = core.Clock()
    while True: 
        if not responded:
            responded = event.getKeys(keyList=validResponses, timeStamped=responseTimer) 
        if duration>0:
            if responseTimer.getTime() > duration:
                break
        else: #end on response
            if responded:
                break
    if not responded:
        return ['NA','NA']
    else:
        return responded[0] #only get the first resp
    
#write to file
def write_to_file(fileHandle,trial,separator=',', sync=True,add_newline=False):
    """Writes a trial (array of lists) to a previously opened file"""
    trial = map(str,trial)
    line = separator.join([str(i) for i in trial]) #join with separator
    if add_newline:
        line += '\n' #add a newline
    try:
        fileHandle.write(line)
    except:
        print('file is not open for writing')
    if sync:
        fileHandle.flush()
        os.fsync(fileHandle)


