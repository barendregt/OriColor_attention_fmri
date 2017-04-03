from __future__ import division
from psychopy import visual, core, misc, event
# from psychopy.data import StairHandler
import numpy as np
from IPython import embed as dbstop
from math import *

import os, sys, time, datetime, cPickle
import pygame
from pygame.locals import *

sys.path.append( 'exp_tools' )


# import Quest
from Session import *
from TrainingTrial import *
from constants_training import *

from Staircase import ThreeUpOneDownStaircase

class ExpectationSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on, task):
		super(ExpectationSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = DISPSIZE, full_screen = screen_full, physical_screen_distance = SCREENDIST, background_color = background_color, physical_screen_size = SCREENSIZE, screen_nr = screen_num )

		self.create_output_file_name()
		if tracker_on:
			# self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
			# if self.tracker_on:
			#     self.tracker_setup()
			# how many points do we want:
			n_points = 5#9

			# order should be with 5 points: center-up-down-left-right
			# order should be with 9 points: center-up-down-left-right-leftup-rightup-leftdown-rightdown 
			# order should be with 13: center-up-down-left-right-leftup-rightup-leftdown-rightdown-midleftmidup-midrightmidup-midleftmiddown-midrightmiddown
			# so always: up->down or left->right

			# creat tracker
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV%d'%n_points)

			# it is setup to do a 9 or 5 point circular calibration, at reduced ecc

			# create 4 x levels:
			width = standard_parameters['eyelink_calib_size'] * DISPSIZE[1]
			x_start = (DISPSIZE[0]-width)/2
			x_end = DISPSIZE[0]-(DISPSIZE[0]-width)/2
			x_range = np.linspace(x_start,x_end,5) + standard_parameters['x_offset']  
			y_start = (DISPSIZE[1]-width)/2
			y_end = DISPSIZE[1]-(DISPSIZE[1]-width)/2
			y_range = np.linspace(y_start,y_end,5) 

			# set calibration targets    
			cal_center = [x_range[2],y_range[2]]
			cal_left = [x_range[0],y_range[2]]
			cal_right = [x_range[4],y_range[2]]
			cal_up = [x_range[2],y_range[0]]
			cal_down = [x_range[2],y_range[4]]
			cal_leftup = [x_range[1],y_range[1]]
			cal_rightup = [x_range[3],y_range[1]]
			cal_leftdown = [x_range[1],y_range[3]]
			cal_rightdown = [x_range[3],y_range[3]]            

			# create 4 x levels:
			width = standard_parameters['eyelink_calib_size']*0.75 * DISPSIZE[1]
			x_start = (DISPSIZE[0]-width)/2
			x_end = DISPSIZE[0]-(DISPSIZE[0]-width)/2
			x_range = np.linspace(x_start,x_end,5) + standard_parameters['x_offset']  
			y_start = (DISPSIZE[1]-width)/2
			y_end = DISPSIZE[1]-(DISPSIZE[1]-width)/2
			y_range = np.linspace(y_start,y_end,5) 

			# set calibration targets    
			val_center = [x_range[2],y_range[2]]
			val_left = [x_range[0],y_range[2]]
			val_right = [x_range[4],y_range[2]]
			val_up = [x_range[2],y_range[0]]
			val_down = [x_range[2],y_range[4]]
			val_leftup = [x_range[1],y_range[1]]
			val_rightup = [x_range[3],y_range[1]]
			val_leftdown = [x_range[1],y_range[3]]
			val_rightdown = [x_range[3],y_range[3]]   

			# get them in the right order
			if n_points == 5:
			    cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0]])
			    cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1]])
			    val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0]])
			    val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1]])
			elif n_points == 9:
			    cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0],cal_leftup[0],cal_rightup[0],cal_leftdown[0],cal_rightdown[0]])
			    cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1],cal_leftup[1],cal_rightup[1],cal_leftdown[1],cal_rightdown[1]])         
			    val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0],val_leftup[0],val_rightup[0],val_leftdown[0],val_rightdown[0]])
			    val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1],val_leftup[1],val_rightup[1],val_leftdown[1],val_rightdown[1]])                     
			#xs = np.round(np.linspace(x_edge,DISPSIZE[0]-x_edge,n_points))
			#ys = np.round([self.ywidth/3*[1,2][pi%2] for pi in range(n_points)])

			# put the points in format that eyelink wants them, which is
			# calibration_targets / validation_targets: 'x1,y1 x2,y2 ... xz,yz'
			calibration_targets = ' '.join(['%d,%d'%(cal_xs[pi],cal_ys[pi]) for pi in range(n_points)])
			# just copy calibration targets as validation for now:
			#validation_targets = calibration_targets
			validation_targets = ' '.join(['%d,%d'%(val_xs[pi],val_ys[pi]) for pi in range(n_points)])

			# point_indices: '0, 1, ... n'
			point_indices = ', '.join(['%d'%pi for pi in range(n_points)])

			# and send these targets to the custom calibration function:
			self.custom_calibration(calibration_targets=calibration_targets,
			    validation_targets=validation_targets,point_indices=point_indices,
			    n_points=n_points,randomize_order=True,repeat_first_target=True,)
			# reapply settings:
			self.tracker_setup()
		else:
			self.create_tracker(tracker_on = False)
		
		self.response_buttons = response_buttons

		self.scanner = scanner
		# self.setup_sounds()

		self.task = task

		self.fileOperations = {}
		
		self.standard_parameters = standard_parameters
		
		self.trialID = -1

		self.pdOutput = list()
		# trials can be set up independently of the staircases that support their parameters
		
		self.parameter_names = ['base_ori', 'base_r', 'base_g', 'base_b', 'ori_offset', 'color_offset', 'stim_type', 'task', 'x', 'y']
		

		self.prepare_staircases()
		
		self.prepare_trials()
		
		self.setup_sounds()

	def create_output_file_name(self, data_directory = 'data'):
		"""create output file"""
		now = datetime.datetime.now()
		opfn = now.strftime("%Y-%m-%d_%H.%M.%S")
		
		if not os.path.isdir(data_directory):
			os.mkdir(data_directory)
			
		#self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_' + opfn )
		self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_task-' + opfn )		

	def setup_sounds(self):
		"""initialize pyaudio backend, and create dictionary of sounds."""
		self.pyaudio = pyaudio.PyAudio()

		# task_sounds = [['lowToneSingle.wav','lowToneDouble.wav','highToneSingle.wav','highToneDouble.wav'],
		# 		   ['highToneSingle.wav','highToneDouble.wav','lowToneSingle.wav','lowToneDouble.wav'],
		# 		   ['lowToneSingle.wav','highToneSingle.wav','lowToneDouble.wav','highToneDouble.wav'],
		# 		   ['lowToneDouble.wav','highToneDouble.wav','lowToneSingle.wav','highToneSingle.wav'],
		# 		   ['lowToneDouble.wav','lowToneSingle.wav','highToneDouble.wav','highToneSingle.wav'],
		# 		   ['highToneDouble.wav','highToneSingle.wav','lowToneDouble.wav','lowToneSingle.wav'],
		# 		   ['highToneSingle.wav','lowToneSingle.wav','highToneDouble.wav','lowToneDouble.wav'],
		# 		   ['highToneDouble.wav','lowToneDouble.wav','highToneSingle.wav','lowToneSingle.wav']					   
		# 			  ]

		# if not os.path.isfile(os.path.join('data', self.subject_initials + '_soundmap.txt')):
		# 	f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'w')			

		# 	f.write(','.join(task_sounds[np.random.randint(len(task_sounds))]))
		# 	f.close()

		# f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'r')

		# sub_task_sounds = f.read().split(",")

		self.sound_files = {
						   'correct' : 'sounds/correct.wav',
						   'incorrect' : 'sounds/incorrect.wav',
							}
		self.sounds = {}
		for sf in self.sound_files:
			self.read_sound_file(file_name = self.sound_files[sf], sound_name = sf)
		# print self.sounds
	
	def play_sound(self, sound_key = ''):
		
		## assuming 44100 Hz, mono channel np.int16 format for the sounds
		#stream_data = self.parameters['sounds']['error']
		if len(sound_key)>0:
			stream_data = self.sounds[sound_key] #self.cue_sound

			self.frame_counter = 0
			def callback(in_data, frame_count, time_info, status):
				data = stream_data[self.frame_counter:self.frame_counter+frame_count]
				self.frame_counter += frame_count
				return (data, pyaudio.paContinue)

			#shell()

			# open stream using callback (3)
			stream = self.pyaudio.open(format=pyaudio.paInt16,
							channels=1,
							rate=44100,
							output=True,
							stream_callback=callback)

			stream.start_stream()
			# stream.write(stream_data)	
			#stream_data = None
			del stream

	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		self.phase_durations = np.array([
			self.standard_parameters['timing_ITI_duration'], 	# inter trial interval
			# self.standard_parameters['timing_cue_duration'],	# present first cue (audio)
			self.standard_parameters['timing_cue_duration'],	# present second cue (task)
			self.standard_parameters['timing_stimcue_interval'],# wait before presenting stimulus
			self.standard_parameters['timing_stim_1_Duration'], # present first stimulus
			self.standard_parameters['timing_ISI'], 			# inter stimulus interval
			self.standard_parameters['timing_stim_2_Duration'], # present second stimulus
			self.standard_parameters['timing_responseDuration'], # wait for response			
			self.standard_parameters['timing_AudioFeedback']    # present AudioFeedbacj
			])	# ITI

		## TRIAL DESIGN: 
		#stim_types = np.vstack([[(a,b) for a in self.standard_parameters['session_types']] for b in self.standard_parameters['tasks']])			
		stim_types = self.standard_parameters['session_types']

		self.trials = list()

		
		trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])
		stim_labels = ['red0','red90','green0','green90']#['red45','red135','green45','green135']
		# trial_labels = ['base','P-UP','UP-P','UP-UP']

		nTrialsPerStim = self.standard_parameters['ntrials_per_stim']

		xy_positions = self.standard_parameters['stimulus_positions'] * nTrialsPerStim * 4

		xy_ii = 0
		
		task_ii = 0

		for ttype in range(len(trial_types)):
			# for stype in range(len(stim_types)):

				for ii in range(nTrialsPerStim):
					
					this_trial_parameters = {'base_ori': trial_types[ttype][0],
											'base_color_lum': trial_types[ttype][1],
											'base_color_a': trial_types[ttype][2],
											'base_color_b': trial_types[ttype][3],
											'trial_stimulus_label': stim_labels[ttype],
											'trial_stimulus': ttype,
											'task': self.task[task_ii],
											'trial_position_x': xy_positions[xy_ii][0],
											'trial_position_y': xy_positions[xy_ii][1]																											 																												 
											}

					self.trials.append(this_trial_parameters)

					xy_ii += 1

					if len(self.task)>1:
						task_ii = 1-task_ii


		shuffle(self.trials)

		for ii,t in enumerate(self.trials):
			if ii > 0:
				while (self.trials[ii]['trial_position_x'] == self.trials[ii-1]['trial_position_x']) and (self.trials[ii]['trial_position_y'] == self.trials[ii-1]['trial_position_y']):

				      self.trials[ii]['trial_position_x'] = self.standard_parameters['stimulus_positions'][np.random.randint(low=0,high=4)][0]
				      self.trials[ii]['trial_position_y'] = self.standard_parameters['stimulus_positions'][np.random.randint(low=0,high=4)][1]
		


	def prepare_staircases(self):

		# Create a separate staircase for every stimulus

		self.staircases = list([0] * len(self.standard_parameters['quest_initial_stim_values']))
		
		for stimt in range(0,len(self.standard_parameters['quest_initial_stim_values'])):


			self.staircases[stimt] = ThreeUpOneDownStaircase(initial_value = self.standard_parameters['quest_initial_stim_values'][stimt], 
												  			 initial_stepsize= self.standard_parameters['quest_stepsize'][stimt],
															 stepsize_multiplication_on_reversal = 0.85,
															 min_test_val = self.standard_parameters['quest_minmax'][stimt][0],
															 max_test_val = self.standard_parameters['quest_minmax'][stimt][1],
															 max_nr_trials = 100000)	

		self.last_used_staircase = {'red': int(round(np.random.rand())), 'green': int(round(np.random.rand())), 'horizontal': int(round(np.random.rand())), 'vertical': int(round(np.random.rand()))} 

	def partial_store(self, tid):
		data = pd.concat(self.pdOutput)	
		data.to_csv(self.output_file + '_output.csv')		

		if os.path.isfile(self.output_file + '_INPROGRESS.pickle'):
			self.fileOperations['lastModified'] = '%s' % datetime.datetime.now()
		else:
			self.fileOperations.update({'created': '%s' % datetime.datetime.now()})
			self.fileOperations.update({'lastModified': '%s' % datetime.datetime.now()})		

		parsopf = open(self.output_file + '_INPROGRESS.pickle', 'wb')
		cPickle.dump([self.outputDict, self.pdOutput, self.trials, self.events, tid, self.fileOperations], parsopf)
		# cPickle.dump(self.trialID, parsopf)
		parsopf.close()
		
	def close(self):
		
		this_instruction_string = 'Exporting data, please wait'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 20, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()		
		
		#self.outputDict['trials'] = self.trial_array

		super(ExpectationSession, self).close()

		#if self.index_number == 0:

		parsopf = open(os.path.join('data', self.subject_initials + '_training_staircase.pickle'), 'wb')

		cPickle.dump(self.staircases,parsopf)

		f = open(os.path.join('data', self.subject_initials + '_training_staircase.txt'), 'w')
		f.write(";".join([str(self.staircases[s].get_intensity()) for s in range(len(self.staircases))]))			
		f.close()


	
	def run(self):
		"""docstring for fname"""
		# cycle through trials

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.51 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (-.8, -.8, -.8), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})


		# Wait to start th experiment
		self.fixation_outer_rim.draw()
		#self.fixation_rim.draw()
		self.fixation.draw()

		this_instruction_string = 'Waiting for scanner to start'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		#print 'Expected total duration: %3.2fs (%1.0f TRs)' % (1.0,2.0)#(self.phase_durations.sum() * len(self.trials), (self.phase_durations.sum() * len(self.trials)) / self.standard_parameters['TR'])

		print 'Waiting for scanner to start...'

		#if self.scanner=='y':
		event.waitKeys(keyList = ['t'])

		self.fixation_outer_rim.draw()
		# self.fixation_rim.draw()
		self.fixation.draw()

		self.screen.flip()

		if self.scanner == 'y':
			time.sleep(self.standard_parameters['timing_start_empty'])
		#else:
		#	event.waitKeys(keyList = ['space'])		


		event.clearEvents()




		# if self.trialID >= 0:
		# 	rStart = self.trialID
		# else:
		rStart = 0

		for self.trialID in range(rStart, len(self.trials)):
			# prepare the parameters of the following trial based on the shuffled trial array
			# this_trial_parameters = self.trial_array[self.trialID,:]			

			print 'Running trial ' + str(self.trialID)

			# Randomly sample ITI and response duration for this trial (will stepsize TR/2)
			these_phase_durations = self.phase_durations.copy()

			these_phase_durations[0] = np.random.choice(np.arange(these_phase_durations[0][0], these_phase_durations[0][1], self.standard_parameters['TR']/2))#these_phase_durations[0][0] + np.random.rand()*these_phase_durations[0][1]			
			# these_phase_durations[-1] = np.random.choice(np.arange(these_phase_durations[-1][0], these_phase_durations[-1][1], self.standard_parameters['TR']/2))

			# self.trials(self.trialID).run(ID = self.trialID)
			this_trial = ExpectationTrial(parameters = self.trials[self.trialID], phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = self.trialID)
			
			self.partial_store(self.trialID)			
			
			if self.stopped == True:
				break
			

		self.fixation_outer_rim.draw()
		# self.fixation_rim.draw()
		self.fixation.draw()

		self.screen.flip()

		if (self.scanner=='y') and (not self.stopped):
			time.sleep(self.standard_parameters['timing_end_empty'])
				
		self.close()
	

