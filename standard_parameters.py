import numpy as np

# standard parameters
standard_parameters = {
	
	## common parameters:
	'TR':               	 0.945,		# VERY IMPORTANT TO FILL IN!! (in secs)
	# 'number_of_quest_trials':  120,		# this needs to divide into 8
	# 'number_of_trials':       400,		# this needs to divide into 8
	'ntrials_per_stim':		 24,#100,   # this * 8 will be the total number of trials

	## stimulus parameters:calc
	'stimulus_size': 3.0,#1.5,	# diameter in dva

	'stimulus_positions': ([2.5, 2.5], [2.5, -2.5], [-2.5, -2.5], [-2.5, 2.5],[2.5, 2.5],[-2.5, 2.5],[-2.5, -2.5], [2.5, -2.5]),#(0.0, 0.0),

	'stimulus_base_spatfreq': 0.02,#0.04,

	'stimulus_base_orientation': (0,90),#(45, 135),
	'stimulus_base_colors': ((70,80,75), (70,-80,75)),

	'quest_initial_stim_values': (50, 50, 5),

	'quest_stepsize': (np.r_[np.array([5,5,2,2]), 1*np.ones((1000))],
		 			   np.r_[np.array([5,5,2,2]), 1*np.ones((1000))],
		 			   np.r_[np.array([0.5,0.5,0.25,0.25]), 0.25*np.ones((1000))]),
				 
	'quest_r_index': (0),#(0,1),
	'quest_g_index': (1),#(2,3),
	'quest_o_index': (2),#(4,5),
	

	'session_types': [0,1,2,3],
	'tasks': [1,2],

	## timing of the presentation:

	'timing_start_empty': 15,
	'timing_finish_empty': 15,

	'timing_stim_1_Duration' : .10, # duration of stimulus presentation, in sec
	'timing_ISI'             : .05,
	'timing_stim_2_Duration' : .10, # duration of stimulus presentation, in sec
	# 'timing_preStimDuration' : 0.75, # SOA will be random between 1 frame and this
	'timing_cue_duration'    : 0.75,	# Duration for each cue separately
	'timing_stimcue_interval' : 0.5,
	'timing_responseDuration' : 1.5,#2.75, # time to respond	
	'timing_ITI_duration':  (0.5, 1.5),		# in sec

	'response_buttons_orientation': ['j','l'],
	'response_buttons_color': ['s','f'],

}

# response_button_signs = {
# 'e':-1,  # left 'less' answer
# 'b':1,   # right 'more' answer
# 'y':2}   # confirm color match

# response_buttons = {
# 	'c' : -1, # more yellow's'
# 	'e' : 1, # more blue'f'
# 	'b' : -1, # CCW  more vertical'j'
# 	'y' : 1 # CW    more horizontal 'l'
# }

response_buttons = {
	's' : -1, # more yellow's'
	'f' : 1, # more blue'f'
	'j' : -1, # CCW  more vertical'j'
	'l' : 1 # CW    more horizontal 'l'
}

screen_num = 1
screen_res = (3840,2160)#(1920,1080)#(1024,768)#(1280,1024)#(1680,1050)#(3840,2160)#(1920,1080)(2560,1440)#(
screen_dist = 60.0 # 159.0
screen_size = (70,40)#(48, 38) # (70, 40)
background_color = (0.0, 0.0, 0.0)