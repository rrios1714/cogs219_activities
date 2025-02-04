import random
import os

def generate_trials(subj_code,seed):
	separator=","
	
	#set seed
	random.seed(int(seed))
	
	#open trial file and write header
	trial_file = open(os.path.join(os.getcwd(),'trials',subj_code+'_trials.csv'),'w')
	header = separator.join(["subj_code","seed", 'image_name','item','angle','match','correct_response'])
	trial_file.write(header+'\n')
	
	#define trial parameters
	angle_list = ["0","50","100"]
	num_items = 48
	match_list = ["same","different"]
	image_name_sep = "_"
	#image_ext = ".jpg"
	
	#create trials
	trials = []
	for i in range(num_items):
		item = str(i+1)
		for angle in angle_list:
			for match in match_list:
				if match == "same":
					image_name = item+image_name_sep+angle
					correct_response = "z"
				else:
					image_name = item+image_name_sep+angle+image_name_sep+"R"
					correct_response = "m"
				trials.append([subj_code,seed,image_name,item,angle,match,correct_response])
	print(trials)
	random.shuffle(trials)
	
	for cur_trial in trials:
		print(cur_trial)
		trial_file.write(separator.join(map(str,cur_trial))+'\n')
	
	trial_file.close()
	return True
				
				
		
	
	


if __name__ == '__main__':
	generate_trials("test",100)	
