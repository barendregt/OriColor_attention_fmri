import numpy as np


DISPSIZE = (1920,1080)#(1024,768)#(1280,1024)#(1024,768)#(1680,1050)#(1280,1024) # canvas size
SCREENSIZE = (70,40)#(33.8,27.1) #(48.0,38.0)# physical screen size in centimeters
SCREENDIST = 225#65.0#60.0#57.0 # centimeters; distance between screen and participant's eyes


screen_num = -1#0#1
#screen_res = (2560,1440)#(1920,1080)#(2560,1440)#(3840,2160)#(1024,768)#(1920,1080)#(1280,1024)#(1680,1050)#(3840,2160)#(1920,1080)#(
#screen_dist = 60#112.5#60#225#60#225#60.0 # 159.0
#screen_size = (33,22)#(69.84,39.29)#(48, 38) # (70, 40)
screen_full = True
background_color = (0.0, 0.0, 0.0)



# standard parameters
standard_parameters = {
	
	## common parameters:
	'TR':               	 0.945,		# VERY IMPORTANT TO FILL IN!! (in secs)
	'mapper_ntrials':		      128,# trials per location
	'mapper_max_index': 63,

	# For custom eye tracker points
	'eyelink_calib_size': 0.5,
	'x_offset':			  0.0,
	
	## stimulus parameters:calc
	'stimulus_size': 100,#2.5,#100,#2.5,#1.5,	# diameter in dva


	'stimulus_mask': None,#'raisedCos',#None,
	'stimulus_positions': [[0.0,0.0]],#[[1.5, 1.5], [1.5, -1.5], [-1.5, -1.5], [-1.5, 1.5]],#(0.0, 0.0),

	'stimulus_base_spatfreq': 0.04,#4,#0.04,#0.02,#0.04,

	'stimulus_base_orientation': (0,90),#(45, 135),
	'stimulus_base_colors': ((55,80,75), (55,-80,75)),

	'quest_initial_stim_values': (70,70,5,5),# (50, 50, 5),

	'quest_stepsize': [15,15,2,2],
				 
	'quest_r_index': (0),#(0,1),
	'quest_g_index': (1),#(2,3),
	'quest_h_index': (2),#(4,5),
	'quest_v_index': (3),

	'quest_minmax': [(0,80),(0,80),(0,100),(0,100)],
	

	'session_types': [0,1,2,3],
	'tasks': [1,2],

	## timing of the presentation:

	'timing_start_empty': 0,#15,
	'timing_finish_empty': 0,#15,

	'timing_stim_1_Duration' : .15, # duration of stimulus presentation, in sec
	'timing_ISI'             : .03,
	'timing_stim_2_Duration' : .15, # duration of stimulus presentation, in sec
	'timing_cue_duration'    : 0.75,	# Duration for each cue separately
	'timing_stimcue_interval' : 0.5,
	'timing_responseDuration' : 1.5,#2.75, # time to respond	
	'timing_ITI_duration':  (0.5, 1.5),		# in sec

	'response_buttons_orientation': ['b','y'],#['j','l'], #
	'response_buttons_color': ['w','e'],#['s','f'],#

	# mapper location order (from above):
	# (T=top,B=bottom,L=left,R=right)
	# TR-BR-BL-TL

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
	'mapper_stimulus_duration':      0.65,		# in TR
	'mapper_task_duration':			 0.5,    # in TR
	'mapper_response_duration':		 1.0,	 # in TR
	'mapper_task_timing':			(2.0, 8.0), # min and max separation of fix task
	'mapper_ITI_duration':           0.2,		# in TR
	'mapper_n_redraws':		 	 	 5.0,		# refresh random phase this many times during presentation	
	'mapper_mapper_redraws':		20.0	

}


response_buttons = {
	standard_parameters['response_buttons_color'][0] : -1, 		# more yellow's' / 'w'
	standard_parameters['response_buttons_color'][1] : 1, 		# more blue'f' / 'e'
	standard_parameters['response_buttons_orientation'][0] : -1,# CCW  more vertical'j' / 'b'
	standard_parameters['response_buttons_orientation'][1] : 1 	# CW    more horizontal 'l' / 'y'
}