import numpy as np

# standard parameters
standard_parameters = {
	
	## common parameters:
	'TR':               	 0.945,		# VERY IMPORTANT TO FILL IN!! (in secs)
	# 'number_of_quest_trials':  120,		# this needs to divide into 8
	# 'number_of_trials':       400,		# this needs to divide into 8
	'ntrials_per_stim':		 24,#100,   # this * 8 will be the total number of trials
	'mapper_ntrials':		       168,
	'mapper_max_index': 63,
	
	## stimulus parameters:calc
	'stimulus_size': 3.0,#1.5,	# diameter in dva

	'stimulus_positions': ([2.5, 2.5], [2.5, -2.5], [-2.5, -2.5], [-2.5, 2.5],[2.5, 2.5],[-2.5, 2.5],[-2.5, -2.5], [2.5, -2.5]),#(0.0, 0.0),

	'stimulus_base_spatfreq': 0.02,#0.04,

	'stimulus_base_orientation': (0,90),#(45, 135),
	'stimulus_base_colors': ((55,80,75), (55,-80,75)),

	'quest_initial_stim_values': (50, 50, 5),

	'quest_stepsize': (np.r_[np.array([10,5,2,2]), 1*np.ones((1000))],
		 			   np.r_[np.array([10,5,2,2]), 1*np.ones((1000))],
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

	'response_buttons_orientation': ['b','y'],
	'response_buttons_color': ['w','e'],


	# OriColorMapper stuff
	'stimulus_ori_min':			90.0,		# minimal orientation to show (in deg)
	'stimulus_ori_max':		   270.0,		# maximum orientation to show (in deg)
	'stimulus_ori_steps':		   8,		# how many steps between min and max
	'stimulus_col_min': 		   0,		# start point on color circle
	'stimulus_col_max':			   8,		# end point on color circle
	'stimulus_col_steps':		   8,		# how many steps through colorspace
	'stimulus_col_rad':			  75,		# radius of color circle
	'stimulus_col_baselum':		  55,	    # L

	'mapper_pre_post_trials':		 5,
	'mapper_stimulus_duration':      1.0,		# in TR
	'mapper_task_duration':			 2.0,    # in TR
	'mapper_ITI_duration':           2.0,		# in TR
	'mapper_n_redraws':		 	 	 10.0,		# refresh random phase this many times during presentation	
	'mapper_mapper_redraws':		20.0	

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

# response_buttons = {
# 	'w' : -1, # more yellow's'
# 	'e' : 1, # more blue'f'
# 	'b' : -1, # CCW  more vertical'j'
# 	'y' : 1 # CW    more horizontal 'l'
# }

response_buttons = {
	standard_parameters['response_buttons_color'][0] : -1, 		# more yellow's' / 'w'
	standard_parameters['response_buttons_color'][1] : 1, 		# more blue'f' / 'e'
	standard_parameters['response_buttons_orientation'][0] : -1,# CCW  more vertical'j' / 'b'
	standard_parameters['response_buttons_orientation'][1] : 1 	# CW    more horizontal 'l' / 'y'
}

screen_num = -1#0#1
screen_res = (2560,1440)#(1920,1080)#(2560,1440)#(3840,2160)#(1024,768)#(1920,1080)#(1280,1024)#(1680,1050)#(3840,2160)#(1920,1080)#(
screen_dist = 60#112.5#60#225#60#225#60.0 # 159.0
screen_size = (69.84,39.29)#(48, 38) # (70, 40)
screen_full = False
background_color = (0.0, 0.0, 0.0)