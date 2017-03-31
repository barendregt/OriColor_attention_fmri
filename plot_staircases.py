from matplotlib import pyplot as pl 
import numpy as np 
#import cPickle as pickle
import glob
import seaborn as sn
import pandas as pd
import sys
sys.path.append( 'exp_tools' )

from Staircase import ThreeUpOneDownStaircase
from IPython import embed as shell
   
# data_dir = '/home/xiaomeng/Data/Pre_scan_data/'
# figure_dir = '/home/shared/2017/visual/Attention/behaviour/'

# lab k2d38
#data_dir = 'C:\Userdata\Martijn\OriColor_atention_fmri\data'
#figure_dir = 'C:\Userdata\Martijn\OriColor_atention_fmri\data'

#csv_files = glob.glob(data_dir+'\*.csv')
csv_files = glob.glob('data'+'\*.csv')
# csv_files = glob.glob(subject_dir, '/*.csv')
csv_files.sort()
#initials = csv_files[0].split('_')[0]
#run_nr = csv_files[0].split('_')[1]
#from run_Experiment_training import main

#shell()
def load_beh_data(csv_files):
	'''extend data over runs, print RT, accuracy for each run'''
	#print ' RT  &  accuracy '

	reaction_time = []
	all_responses = []
	task = []
	button =[]
	position_x =[]
	position_y =[]
	trial_color  = []
	trial_ori = []
	trial_stimulus =[]

	#to calculate d prime
	response = []
	trial_direction = []

	for this_file in csv_files: # loop over files

		#shell()
		csv_data = pd.read_csv(this_file)  #load data na_values = ["NaN"]
		
		# # each run
		# RT_run = np.nanmean(csv_data['reaction_time'])
		# accuracy_run = np.nanmean(csv_data['correct_answer'])

		reaction_time.extend(csv_data['reaction_time'])
		all_responses.extend(csv_data['correct_answer'])
		task.extend(csv_data['task'])
		button.extend(csv_data['button'])
		position_x.extend(csv_data['trial_position_x'])
		position_y.extend(csv_data['trial_position_y'])
		trial_color.extend(csv_data['trial_color'])
		trial_ori.extend(csv_data['trial_orientation'])
		trial_stimulus.extend(csv_data['trial_stimulus'])
		response.extend(csv_data['response'])
		trial_direction.extend(['trial_direction'])

		# print RT_run, accuracy_run
	
	return np.array(reaction_time), np.array(all_responses), np.array(task), np.array(button), np.array(position_x), np.array(position_y), np.array(trial_color), np.array(trial_ori), np.array(trial_stimulus), np.array(response), np.array(trial_direction)


def create_masks():
	'''create masks'''
	reaction_time, all_responses, task, button, position_x, position_y, trial_color, trial_ori, trial_stimulus, response, trial_direction = load_beh_data(csv_files) #  all the data

	
	color_task_mask = np.array(np.array(task)==1)
	ori_task_mask = np.array(np.array(task)==2)

	red_task_mask = np.array(color_task_mask * ((trial_stimulus == 0) + (trial_stimulus == 1)))
	gre_task_mask = np.array(color_task_mask * ((trial_stimulus == 2) + (trial_stimulus == 3)))
	hor_task_mask = np.array(ori_task_mask * ((trial_stimulus == 0) + (trial_stimulus == 2)))
	ver_task_mask = np.array(ori_task_mask * ((trial_stimulus == 1) + (trial_stimulus == 3)))
	
	# right_task_masks with nan values
	right_task_mask = np.array(((np.array(task)==1)*((np.array(button)=='s')+(np.array(button)=='f')))+((np.array(task)==2)*((np.array(button)=='j')+(np.array(button)=='l')))) # sfjl
	wrong_task_mask = np.array(((np.array(task)==2)*((np.array(button)=='s')+(np.array(button)=='f')))+((np.array(task)==1)*((np.array(button)=='j')+(np.array(button)=='l')))) # sfjl

	# responses_mask(correct+incorrect): delete nanvalues and invalid values(wrong task)!!
	responses_mask = np.array((np.array(all_responses)==1) + ((np.array(all_responses)==0) * right_task_mask)) 

	correct_answer_mask = np.array(np.array(all_responses)==1) 
	incorrect_answer_mask = np.array((np.array(all_responses)==0) * (~np.array(wrong_task_mask)))

	# four locations
	top_left_mask = np.array((np.array(position_x) == -2.5) * (np.array(position_y) == 2.5))
	top_right_mask = np.array((np.array(position_x) == 2.5) * (np.array(position_y) == 2.5))
	bottom_left_mask = np.array((np.array(position_x) == -2.5) * (np.array(position_y) == -2.5))
	bottom_right_mask = np.array((np.array(position_x) == 2.5) * (np.array(position_y) == -2.5))

	# compared with red_task_mask, these masks gives more trials (red stimulus, regardless the tasks -color or orientation)
	red_stimulus_mask = np.array((trial_stimulus == 0) + (trial_stimulus == 1))
	gre_stimulus_mask = np.array((trial_stimulus == 2) + (trial_stimulus == 3))
	hor_stimulus_mask = np.array((trial_stimulus == 0) + (trial_stimulus == 2))
	ver_stimulus_mask = np.array((trial_stimulus == 1) + (trial_stimulus == 3))

	return color_task_mask, ori_task_mask, red_task_mask, gre_task_mask, hor_task_mask, ver_task_mask, right_task_mask, wrong_task_mask, responses_mask, correct_answer_mask, incorrect_answer_mask, top_left_mask, top_right_mask, bottom_left_mask, bottom_right_mask, red_stimulus_mask, gre_stimulus_mask, hor_stimulus_mask, ver_stimulus_mask


def plot_staircases (csv_files, initials, run_nr):
	'''plot stairecase for each participant'''

	all_responses = load_beh_data(csv_files)[1] # index starts from 0
	responses_mask = create_masks()[8] # changes! if add seperatable analysis
	correct_answer_mask = create_masks()[9]
	color_task_mask = create_masks()[0]
	ori_task_mask = create_masks()[1]
	red_task_mask = create_masks()[2]
	gre_task_mask = create_masks()[3]
	hor_task_mask = create_masks()[4]
	ver_task_mask = create_masks()[5]

	#initials = csv_files[0].split('_')[0]

	# color & orientation accuracy
	#responses = np.array(all_responses)[responses_mask]
	color_responses = np.array(all_responses)[responses_mask * color_task_mask]
	color_n_responses = np.arange(1, len(color_responses)+1)
	color_cum_responses = np.cumsum(color_responses)
	color_accuracy = color_cum_responses/color_n_responses

	ori_responses = np.array(all_responses)[responses_mask * ori_task_mask]
	ori_n_responses = np.arange(1, len(ori_responses)+1)
	ori_cum_responses = np.cumsum(ori_responses)
	ori_accuracy = ori_cum_responses/ori_n_responses

	red_task_responses = np.array(all_responses)[responses_mask * red_task_mask]
	red_task_n_responses = np.arange(1, len(red_task_responses)+1)
	red_task_cum_responses = np.cumsum(red_task_responses)
	red_task_accuracy = red_task_cum_responses/red_task_n_responses

	gre_task_responses = np.array(all_responses)[responses_mask * gre_task_mask]
	gre_task_n_responses = np.arange(1, len(gre_task_responses)+1)
	gre_task_cum_responses = np.cumsum(gre_task_responses)
	gre_task_accuracy = gre_task_cum_responses/gre_task_n_responses

	hor_task_responses = np.array(all_responses)[responses_mask * hor_task_mask]
	hor_task_n_responses = np.arange(1, len(hor_task_responses)+1)
	hor_task_cum_responses = np.cumsum(hor_task_responses)
	hor_task_accuracy = hor_task_cum_responses/hor_task_n_responses

	ver_task_responses = np.array(all_responses)[responses_mask * ver_task_mask]
	ver_task_n_responses = np.arange(1, len(ver_task_responses)+1)
	ver_task_cum_responses = np.cumsum(ver_task_responses)
	ver_task_accuracy = ver_task_cum_responses/ver_task_n_responses

	# staircase
	trial_color = load_beh_data(csv_files)[6]
	trial_ori = load_beh_data(csv_files)[7]

	red_staircase = np.abs(trial_color[responses_mask * red_task_mask])
	gre_staircase = np.abs(trial_color[responses_mask * gre_task_mask])
	hor_staircase = np.abs(trial_ori[responses_mask * hor_task_mask])
	ver_staircase = np.abs(trial_ori[responses_mask * ver_task_mask])

	#plot accuracy & staircase
	f = pl.figure(figsize = (25,15))

	s1 = f.add_subplot(231)
	pl.plot(red_task_accuracy)
	pl.plot(gre_task_accuracy)
	pl.legend(['red', 'green'], loc ='best', fontsize = 18)
	pl.ylim([0, 1])
	pl.axhline(0.79,color='k',ls='--')
	pl.axhline(0.71,color='k',ls='--')
	sn.despine(offset=10)
	s1.set_title('Moving color accuracy', fontsize = 20)

	s2 = f.add_subplot(232)
	pl.plot(hor_task_accuracy)
	pl.plot(ver_task_accuracy)
	pl.legend(['horizontal', 'vertical'], loc ='best', fontsize = 18)
	pl.ylim([0, 1])
	pl.axhline(0.79,color='k',ls='--')
	pl.axhline(0.71,color='k',ls='--')
	sn.despine(offset=10)
	s2.set_title('Moving orientation accuracy', fontsize = 20)

	s3 = f.add_subplot(233)
	objects = ('red','green', 'horzontal', 'vertical')
	y_pos = np.arange(len(objects))
	y_values = [np.mean(red_task_accuracy[51:]), np.mean(gre_task_accuracy[51:]), np.mean(hor_task_accuracy[51:]), np.mean(ver_task_accuracy[51:])]
	sd = np.array([np.std(red_task_accuracy[51:]), np.std(gre_task_accuracy[51:]), np.std(hor_task_accuracy[51:]), np.std(ver_task_accuracy[51:])])
	n = np.array([np.array(red_task_accuracy[51:]).shape[0], np.array(gre_task_accuracy[51:]).shape[0], np.array(hor_task_accuracy[51:]).shape[0], np.array(ver_task_accuracy[51:]).shape[0] ])
	yerr = (sd/np.sqrt(n.squeeze()))*1.96
	# why shape? ValueError: In safezip, len(args[0])=4 but len(args[1])=1, !!! could use len()
	pl.bar(y_pos, y_values, yerr = yerr, align = 'center', alpha = 0.5)
	pl.axhline(0.79,color='k',ls='--')
	pl.axhline(0.71,color='k',ls='--')
	pl.xticks (y_pos, objects, fontsize = 40) # why doesn't work?
	pl.title( 'accuracy for four conditions (delete first 50 trials)', fontsize = 20)
	pl.ylim([0.5, 1])
	sn.despine(offset=10)

	s4 = f.add_subplot(234)
	pl.plot(red_staircase)
	pl.plot(gre_staircase)
	pl.legend(['red', 'green'], loc ='best', fontsize = 18)
	sn.despine(offset=10)
	s4.set_title('staircase color', fontsize = 20)

	s5 = f.add_subplot(235)
	pl.plot(hor_staircase)
	pl.plot(ver_staircase)
	pl.legend(['horizontal', 'vertical'], loc ='best', fontsize = 18)
	sn.despine(offset=10)
	s5.set_title('staircase orientation', fontsize = 20)


	pl.savefig( 'data\lab_%s_%d_color_ori_staircase_plot.jpg'%(initials,run_nr))
	#pl.savefig( figure_dir +'\lab_%s_%d_color_ori_staircase_plot.jpg'%(initials,run_nr))
	# pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))










# def plot_staircases(initials,run_nr):


# 	stairs = ['red','green','ori']

# 	# Load staircase data
# 	staircases = pickle.load(open('data/' + initials + '_staircase.pickle','rb'))

# 	# shell()
# 	# Compute average performance over time
# 	percent_correct = list()
# 	for ii in range(len(staircases)):

# 		responses = staircases[ii].past_answers

# 		percent_correct.append(np.cumsum(responses) / np.arange(1,len(responses)+1))


# 	# Plot average resp correct over time

# 	f = pl.figure()

# 	for s in range(len(stairs)):
# 		pl.plot(percent_correct[s],'-')
# 	pl.legend(stairs)

# 	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))


