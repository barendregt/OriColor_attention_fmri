from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
from IPython import embed as dbstop
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time

# import Quest

import ColorTools as ct

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from OriColorTrial import *
from constants  import *
from Staircase import ThreeUpOneDownStaircase

# import appnope
# appnope.nope()

class OriColorSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on, run_type):
		super(OriColorSession, self).__init__( subject_initials, index_number)

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
		

		self.run_type = run_type

		self.response_button_signs = response_buttons
		self.response_buttons = response_buttons

		self.task_timing = (0.0, 0.0)
		self.response_timing = (0.0, 0.0)
		self.next_task_time = 0.0
		self.pulse_task = False
		self.last_task_val = 0
		self.task_responded = False

		self.last_taskdir = 0
		self.last_colval = 0

		self.scanner = scanner
		# trials can be set up independently of the staircases that support their parameters
		self.prepare_trials()
		self.prepare_staircases()
		#self.prepare_sounds()
	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		self.standard_parameters = standard_parameters

		# if self.run_type==1:	
		# 	self.standard_parameters['mapper_ntrials'] *= 2


		self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps']+1)[:-1]

		# Compute evenly-spaced steps in (L)ab-space

		color_theta = (np.pi*2)/self.standard_parameters['stimulus_col_steps']
		color_angle = color_theta * np.arange(self.standard_parameters['stimulus_col_min'], self.standard_parameters['stimulus_col_max'],dtype=float)
		color_radius = self.standard_parameters['stimulus_col_rad']

		color_a = color_radius * np.cos(color_angle)
		color_b = color_radius * np.sin(color_angle)

		self.colors = [ct.lab2psycho((self.standard_parameters['stimulus_col_baselum'], a, b)) for a,b in zip(color_a, color_b)]			 

		#self.stimulus_positions = self.standard_parameters['stimulus_positions']
		
		self.trial_array = []

	
		self.trial_array = np.array([[[o,c[0],c[1],c[2]] for o in self.orientations] for c in self.colors]).reshape((self.standard_parameters['stimulus_ori_steps']*self.standard_parameters['stimulus_col_steps'],4))
		# dbstop()

		# emptytrials = self.standard_parameters['mapper_ntrials'] - len(self.trial_array)

		self.trial_indices = np.hstack([np.random.permutation(self.standard_parameters['mapper_ntrials']) for i in range(len(self.standard_parameters['stimulus_positions'][self.run_type]))])[:,np.newaxis]#np.random.permutation(self.standard_parameters['mapper_ntrials'])#


		self.trial_params = np.hstack([self.trial_indices, np.vstack([np.reshape(item*self.standard_parameters['mapper_ntrials'],(self.standard_parameters['mapper_ntrials'],2)) for item in self.standard_parameters['stimulus_positions'][self.run_type]])])

		self.trial_params = self.trial_params[np.random.permutation(self.trial_params.shape[0]),:]

		if self.run_type==1:
			tmp = self.trial_params
			self.trial_params = np.hstack([100*np.ones((self.trial_params.shape[0]*2,1)), np.zeros((self.trial_params.shape[0]*2,1)), np.zeros((self.trial_params.shape[0]*2,1))])
			self.trial_params[0::2] = tmp

		

		# Add empty trials
		for i in range(self.standard_parameters['mapper_pre_post_trials']):
			self.trial_params = np.vstack([[100,0,0], self.trial_params, [100,0,0]])


		self.phase_durations = np.array([0, # present stimulus
										 self.standard_parameters['mapper_stimulus_duration'] * self.standard_parameters['TR'],
										 0])	# ITI

		self.per_trial_parameters = []
		self.per_trial_phase_durations = []

		mapper_trial_duration = self.standard_parameters['mapper_ITI_duration'] + self.standard_parameters['mapper_stimulus_duration']

		for i in range(len(self.trial_params)):

			self.per_trial_parameters.append(self.standard_parameters.copy())

			self.per_trial_parameters[i]['stimulus_params'] = []

			if self.trial_params[i,0] < (8*8):
				self.per_trial_parameters[i]['stimulus_params'] = np.hstack([self.trial_array[int(self.trial_params[i,0])], self.trial_params[i,1:]])

			# for posii in range(4):
			# 	if self.trial_indices[i,posii] < (8*8):
			# 		this_trial_parameters['ori_color'][posii] = self.trial_array[self.trial_indices[i,posii],:]

			# this_trial_parameters['task_start'] = -1
			# if i in self.task_trials:
			# 	this_trial_parameters['task_start'] = np.random.random() * self.phase_durations.sum()


			# this_trial_parameters['colors'] = [self.colors[self.trial_array[i,1]], self.colors[self.trial_array[i,3]], self.colors[self.trial_array[i,5]], self.colors[self.trial_array[i,7]]]

			self.per_trial_phase_durations.append(self.phase_durations.copy())

			stim_shift = self.standard_parameters['mapper_ITI_duration'] * np.random.random()

			self.per_trial_phase_durations[i][0] = stim_shift * mapper_trial_duration
			self.per_trial_phase_durations[i][2] = mapper_trial_duration-self.per_trial_phase_durations[i][:2].sum()		

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22.5, pos = np.array((0.0,0.0)), color = (-1,-1,-1), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='circle',tex=None, size=50, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=20.0, pos = np.array((0.0,0.0)), color = np.array((0,0,0)), opacity = 1.0, maskParams = {'fringeWidth':0.4})
		
		#ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stimulus_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		#self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def prepare_staircases(self):


		# Create a separate staircase for every stimulus

		self.staircase = ThreeUpOneDownStaircase(initial_value = 0.5, 
												 initial_stepsize= 0.1,
												 stepsize_multiplication_on_reversal = 0.8,
												 min_test_val = 0,
												 max_test_val = 1,
												 max_nr_trials = 100000)	
	

	def time_for_next_task(self):

		#pulse_task = False

		current_time = self.clock.getTime()

		if (not self.pulse_task) and (current_time >= self.next_task_time):

			# Did we get a response to the last pulse?
			if not self.task_responded: # count not responding as an error
				self.staircase.answer(0)#, self.last_task_val)

				log_msg = 'staircase auto-updated from %f to %f after no response at %f'%( self.last_task_val, self.staircase.get_intensity(), current_time )

				self.last_task_val = min([max([self.staircase.get_intensity(), 0.01]), 0.99])

				# self.task_responded = True

				self.events.append( log_msg )
				print log_msg

				if self.tracker:
					self.tracker.log( log_msg )			

			self.next_task_time = current_time + (self.standard_parameters['mapper_task_timing'][0] + np.random.random() * self.standard_parameters['mapper_task_timing'][1])
			self.pulse_task = True
			self.task_timing = (current_time, current_time + self.standard_parameters['mapper_task_duration'])
			# self.response_timing = (current_time, current_time + self.standard_parameters['mapper_response_duration'])
			self.task_direction = 2*round(np.random.random()) - 1
			self.task_responded = False

			log_msg = 'Running task from %f to %f' % (current_time, self.next_task_time)

			print log_msg

			self.events.append(log_msg)
		elif self.pulse_task and (current_time > self.task_timing[1]):
			self.pulse_task = False 

		return self.pulse_task

	def create_output_file_name(self, data_directory = 'data'):
		"""create output file"""
		now = datetime.datetime.now()
		opfn = now.strftime("%Y-%m-%d_%H.%M.%S")
		
		if not os.path.isdir(data_directory):
			os.mkdir(data_directory)
			
		#self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_' + opfn )
		self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_mapper-' + opfn )

	def close(self):
		super(OriColorSession, self).close()

		parsopf = open(self.output_file + '_trialinfo.pickle', 'wb')

		output = [self.trial_array, self.trial_indices, self.trial_params, self.per_trial_parameters, self.per_trial_phase_durations, self.staircase]

		pickle.dump(output,parsopf)

		# with open(self.output_file_name, 'w') as f:
		# 	pickle.dump(self.trial_array, f)
		# for s in self.staircases.keys():
		# 	print 'Staircase {}, mean {}, standard deviation {}'.format(s, self.staircases[s].mean(), self.staircases[s].sd())
		
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials


		# self.screen.close()
		# dbstop()


		# Wait to start th experiment
		self.fixation_outer_rim.draw()
		self.fixation_rim.draw()
		self.fixation.draw()

		this_instruction_string = 'Waiting for scanner to start'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		print 'Waiting for scanner to start...'

		#if self.scanner=='y':
		event.waitKeys(keyList = ['t'])		

		# self.screen.close()

		# dbstop()
		print len(self.trial_params)

		start_time = self.clock.getTime()

		for i in range(len(self.trial_params)):
			# prepare the parameters of the following trial based on the shuffled trial array
			trial_start_time = self.clock.getTime()


			this_trial = OriColorTrial(self.per_trial_parameters[i], phase_durations = self.per_trial_phase_durations[i], session = self, screen = self.screen, tracker = self.tracker)
			
				# run the prepared trial
			
			this_trial.run(ID = i)

			print "trial #%i took %fs to run" %(i, self.clock.getTime()-trial_start_time)

			if self.stopped == True:
				break

			
			while self.clock.getTime()-trial_start_time < self.standard_parameters['TR']:
				# event.waitKeys(keyList = ['t'])
				time.sleep(0.00001)
		
		print self.clock.getTime() - start_time
		self.close()
		# Save both separate frame images and movie (attempt)
		# self.screen.saveMovieFrames('movie/expframe.png')			
		#slef.screen.saveMovieFrames('expdemo.mp4', codec = 'libx264')
	

