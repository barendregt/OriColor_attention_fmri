

# standard parameters
standard_parameters = {
	
	## common parameters:
	'TR':               	 0.945,		# VERY IMPORTANT TO FILL IN!! (in secs)
	'number_of_quest_trials':  120,		# this needs to divide into 8
	'number_of_trials':       400,		# this needs to divide into 8
	'trials_to_break':        100,
	## stimulus parameters:calc
	'stimulus_size': 2.0,#1.5,	# radius in dva

	'stimulus_position': (0.0, 0.0),

	'stimulus_base_spatfreq': 0.04,

	'stimulus_base_orientation': (45, 135),
	'stimulus_base_colors': ((70,80,75), (70,-80,75)),

	'quest_initial_stim_values': (50, 50, 5),
	# 'quest_initial_stim_values': (50, 50,  # [0,1] = red
								  # 50, 50,  # [2,3] = green
								  # 10, 1), # [4,5] = ori
	'quest_threshold': 0.75,
	# 'quest_range': (100, 100, 
					# 100, 100, 
					# 20, 2),
	# 'quest_sd': (50, 50,
				 # 50, 50, 
				 # 10, 1.0),

	'quest_range': (400, 400, 100),
	'quest_sd': (25, 25, 2.5),
				 
	'quest_r_index': (0),#(0,1),
	'quest_g_index': (1),#(2,3),
	'quest_o_index': (2),#(4,5),
	
	'test_values_expected': [0.25,0.35,0.5, 0.7, 1.0, 1.41, 2.0, 2.83, 4],
	'test_values_unexpected': [0.5, 0.7, 1.0, 1.41, 2.0],

	'session_types': [0,1,2,3],
	'tasks': [1,2],

	## timing of the presentation:
	'timing_stim_1_Duration' : .15, # duration of stimulus presentation, in sec
	'timing_ISI'             : .03,
	'timing_stim_2_Duration' : .15, # duration of stimulus presentation, in sec
	'timing_preStimDuration' : 0.75, # SOA will be random between 1 frame and this
	'timing_cue_duration'    : 1.25,	# Duration for each cue separately
	'timing_stimcue_interval' : 0.5,
	'timing_responseDuration' : 2.75, # time to respond	
	'timing_ITI_duration':  (0.5, 1.0),		# in sec

	'response_buttons_orientation': ['j','l'],
	'response_buttons_color': ['s','f'],

	############
	## TRAINING PARAMETERS
	############

	####
	## LEVEL 0
	####

	'trainer_first_level_repeats': 5,

	'trainer_level_0_task_instruction': 'Press spacebar to start...',

	'cue_index_level_0': -3,
	'task_index_level_0': 0,

	## timing of the presentation:
	'trainer_level_0_timing_stim_1_Duration' : 0.5, # duration of stimulus presentation, in sec
	'trainer_level_0_timing_cue_duration'    : 0,	# Duration for each cue separately	
	'trainer_level_0_timing_responseDuration' : 0, # time to respond	
	'trainer_level_0_timing_ITI_duration':  (0.5, 0.75),		# in sec


	####
	## LEVEL 1
	####

	'demo_stim_pos_x': [-3.0, -1.0, 1.0, 3.0],
	'demo_stim_pos_y': [3.0, 3.0, 3.0, 3.0],

	'trainer_second_level_repeats': 100,
	'trainer_second_level_minimal_trials': 20,

	'trainer_response_phase': 2,

	'trainer_second_level_pc_goal': 0.95,

	'trainer_level_1_task_instruction': 'Press spacebar to start...',

	'cue_index_level_1': -3,
	'task_index_level_1': 0,	

	'trainer_response_buttons': ['f','g','h','j'],

	## timing of the presentation:
	'trainer_level_1_timing_stim_1_Duration' : 0.5, # duration of stimulus presentation, in sec
	'trainer_level_1_timing_cue_duration'    : 0.75,	# Duration for each cue separately	
	'trainer_level_1_timing_responseDuration' : 2.5, # time to respond	
	'trainer_level_1_timing_ITI_duration':  (0.5, 2.5)		# in sec

}

# response_button_signs = {
# 'e':-1,  # left 'less' answer
# 'b':1,   # right 'more' answer
# 'y':2}   # confirm color match

response_buttons = {
	's' : -1, # more yellow
	'f' : 1, # more blue
	'j' : -1, # more vertical
	'l' : 1 # more horizontal
}

screen_res = (1024,768)#(1280,1024)#(1680,1050)#(3840,2160)#(1920,1080)
screen_dist = 60.0
screen_size = (48, 38)
background_color = (0.0, 0.0, 0.0)