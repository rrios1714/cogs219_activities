import random
import os

def generate_trials(subj_code,seed):

    separator = ","

    #do cool stuff

    #set seed
    random.seed(int(seed))

    # open a trial file
    trial_file = open(os.path.join(os.getcwd(),'trials',subj_code+'_trials.csv'),'w')
    header = separator.join(["subj_code","seed", 'image_name','item','angle','match','correct_response'])
    trial_file.write(header+'\n')

    #define key params
    angle_list = ["0","50","100","150"]
    num_items = 48
    match_list = ["same","different"]
    image_name_sep = "_"

    # create a list holding all trials
    trials = []
    for i in range(num_items):
        item = str(i+1)
        for angle in angle_list:
            for match in match_list:
                if match == "same":
                    image_name = item+image_name_sep+angle
                    correct_response = "z"
                else:
                    image_name = item+image_name_sep+angle + image_name_sep + "R"
                    correct_response = "m"

                trials.append([subj_code,seed,image_name,item, angle, match, correct_response])
    print(trials)

    #shuffle the list
    random.shuffle(trials)

    #write the trials to the trials file
    for cur_trial in trials:
        trial_file.write(separator.join(map(str,cur_trial))+'\n')

    #close the trials file
    trial_file.close()

    return True