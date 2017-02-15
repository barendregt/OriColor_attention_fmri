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
from standard_parameters import *
from Staircase import ThreeUpOneDownStaircase

# import appnope
# appnope.nope()

class OriColorSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on):
		super(OriColorSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = screen_res, full_screen = screen_full, physical_screen_distance = screen_dist, background_color = background_color, physical_screen_size = screen_size, screen_nr = screen_num )

		self.create_output_file_name()
		if tracker_on:
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
			if self.tracker_on:
				self.tracker_setup()
		else:
			self.create_tracker(tracker_on = False)
		
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


		# self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps'])

		self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps']+1)
		self.orientations = self.orientations[0:(self.standard_parameters['stimulus_ori_steps'])]

		# Compute evenly-spaced steps in (L)ab-space

		color_theta = (np.pi*2)/self.standard_parameters['stimulus_col_steps']
		color_angle = color_theta * np.arange(self.standard_parameters['stimulus_col_min'], self.standard_parameters['stimulus_col_max'],dtype=float)
		color_radius = self.standard_parameters['stimulus_col_rad']

		color_a = color_radius * np.cos(color_angle)
		color_b = color_radius * np.sin(color_angle)

		self.colors = [ct.lab2psycho((self.standard_parameters['stimulus_col_baselum'], a, b)) for a,b in zip(color_a, color_b)]			 

		self.stimulus_positions = self.standard_parameters['stimulus_positions']
		
		self.trial_array = []

	
		self.trial_array = np.array([[[o,c[0],c[1],c[2]] for o in self.orientations] for c in self.colors]).reshape((self.standard_parameters['stimulus_ori_steps']*self.standard_parameters['stimulus_col_steps'],4))
		# self.trial_array = np.tile(self.trial_array,(2,1))
		# self.screen.close()

		# dbstop()

		# trial_indices = np.tile(np.arange(0,len(pos_array)+1),(4,1))
		# np.random.permutation(trial_indices)

		emptytrials = self.standard_parameters['mapper_ntrials'] - len(self.trial_array)

		self.trial_indices = np.array([np.random.permutation(len(self.trial_array)+emptytrials) for i in range(4)]).T

		# Add empty trials
		for i in range(self.standard_parameters['mapper_pre_post_trials']):
			self.trial_indices = np.vstack([[100,100,100,100], self.trial_indices, [100,100,100,100]])

		
		# 

		# for fnsti in range(emptytrials):
		# 	pos_array.append([])
		# pos_array = np.array(pos_array)

		# self.trial_array = [[],[],[],[]]

		# for i in range(4):

		# 	self.trial_array[i].extend([[] for x in range(5)])

		# 	trial_thingie = pos_array.copy()
		# 	np.random.shuffle(trial_thingie)

		# 	self.trial_array[i].extend(trial_thingie)
		# 	self.trial_array[i].extend([[] for x in range(5)])

		# 	# newarray = pos_array.copy()

		# 	# np.random.shuffle(newarray)

		# Task on X% of trials
		# task_prob = 0.4

		# min_diff = 1

		#while min_diff == 1:
		# self.task_trials = np.random.choice(range(len(self.trial_indices)), size=round(task_prob * len(self.trial_indices)), replace=False)
			#min_diff = np.diff(np.sort(self.task_trials)).min()
		

			# self.trial_array.append(newarray)

		# self.trial_array = np.array(self.trial_array)

		self.phase_durations = np.array([self.standard_parameters['mapper_ITI_duration'] * self.standard_parameters['TR'], # present stimulus
										 self.standard_parameters['mapper_stimulus_duration'] * self.standard_parameters['TR'] ])	# ITI


		

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=20.0, pos = np.array((0.0,0.0)), color = np.array((0,0,0)), opacity = 1.0, maskParams = {'fringeWidth':0.4})
		
		#ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stimulus_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		#self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def prepare_staircases(self):

		# Create a separate staircase for every stimulus

		self.staircase = ThreeUpOneDownStaircase(initial_value = 0.5, 
												 initial_stepsize= 0.1,
												 stepsize_multiplication_on_reversal = 0.85,
												 max_nr_trials = 100000)	
	

	def time_for_next_task(self):

		#pulse_task = False

		current_time = self.clock.getTime()

		if (not self.pulse_task) and (current_time >= self.next_task_time):
			self.next_task_time = current_time + (self.standard_parameters['mapper_task_timing'][0] + np.random.random() * self.standard_parameters['mapper_task_timing'][1])
			self.pulse_task = True
			self.task_timing = (current_time, current_time + self.standard_parameters['mapper_task_duration'])
			self.response_timing = (current_time, current_time + self.standard_parameters['mapper_response_duration'])
			self.task_direction = 2*np.random.random() - 1
			self.task_responded = False
		elif self.pulse_task and (current_time > self.task_timing[1]):
			self.pulse_task = False 

			if not self.task_responded: # count not responding as an error
				self.staircase.answer(0, self.last_task_val)

				log_msg = 'staircase auto-updated from %f to %f after no response at %f'%( self.last_task_val, self.staircase.get_intensity(), self.clock.getTime() )

				self.last_task_val = min([max([self.session.staircase.get_intensity(), 0.05]), 0.95])

				self.events.append( log_msg )
				print log_msg

				if self.tracker:
					self.tracker.log( log_msg )

			self.task_responded = False

		return self.pulse_task


	def close(self):
		super(OriColorSession, self).close()

		parsopf = open(self.output_file + '_trialinfo.pickle', 'wb')

		output = [self.trial_array, self.trial_indices, self.staircase]

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
		#self.fixation_rim.draw()
		self.fixation.draw()

		this_instruction_string = 'Waiting for scanner to start'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		print 'Waiting for scanner to start...'

		#if self.scanner=='y':
		event.waitKeys(keyList = ['t'])		

		start_time = self.clock.getTime()

		for i in range(len(self.trial_indices)):
			# prepare the parameters of the following trial based on the shuffled trial array
			trial_start_time = self.clock.getTime()
			this_trial_parameters = self.standard_parameters.copy()

			this_trial_parameters['ori_color'] = [[],[],[],[]]

			for posii in range(4):
				if self.trial_indices[i,posii] < (8*8):
					this_trial_parameters['ori_color'][posii] = self.trial_array[self.trial_indices[i,posii],:]

			# this_trial_parameters['task_start'] = -1
			# if i in self.task_trials:
			# 	this_trial_parameters['task_start'] = np.random.random() * self.phase_durations.sum()


			# this_trial_parameters['colors'] = [self.colors[self.trial_array[i,1]], self.colors[self.trial_array[i,3]], self.colors[self.trial_array[i,5]], self.colors[self.trial_array[i,7]]]

			these_phase_durations = self.phase_durations.copy()

			this_trial = OriColorTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
				# run the prepared trial
			this_trial.run(ID = i)

			print "trial #%i took %fs to run" %(i, self.clock.getTime()-trial_start_time)

			if self.stopped == True:
				break
		
		print self.clock.getTime() - start_time
		self.close()
		# Save both separate frame images and movie (attempt)
		# self.screen.saveMovieFrames('movie/expframe.png')			
		#slef.screen.saveMovieFrames('expdemo.mp4', codec = 'libx264')
	

