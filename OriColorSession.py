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

		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

		self.create_output_file_name()
		if tracker_on:
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
			if self.tracker_on:
				self.tracker_setup()
		else:
			self.create_tracker(tracker_on = False)
		
		self.response_button_signs = response_button_signs

		self.scanner = scanner
		# trials can be set up independently of the staircases that support their parameters
		self.prepare_trials()
		#self.prepare_staircases()
		#self.prepare_sounds()
	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		self.standard_parameters = standard_parameters


		# self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps'])

		self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps']+1)
		self.orientations = self.orientations[0:(self.standard_parameters['stimulus_ori_steps'])]

		self.colors = np.linspace(0.0, 1.0, self.standard_parameters['stimulus_col_steps']+1)
		self.colors = self.colors[0:(self.standard_parameters['stimulus_col_steps'])]			 

		self.stimulus_positions = self.standard_parameters['stimulus_positions']
		
		self.trial_array = []

	
		pos_array = []

		for d in self.orientations:
			for t in self.colors:
				pos_array.append([d, t])

		pos_array = pos_array*2

		emptytrials = self.standard_parameters['ntrials'] - len(pos_array)
		for fnsti in range(emptytrials):
			pos_array.append([])
		pos_array = np.array(pos_array)

		self.trial_array = [[],[],[],[]]

		for i in range(4):

			self.trial_array[i].extend([[] for x in range(5)])

			trial_thingie = pos_array.copy()
			np.random.shuffle(trial_thingie)

			self.trial_array[i].extend(trial_thingie)
			self.trial_array[i].extend([[] for x in range(5)])

			# newarray = pos_array.copy()

			# np.random.shuffle(newarray)

			

			# self.trial_array.append(newarray)

		self.trial_array = np.array(self.trial_array)

		self.phase_durations = np.array([
			-0.0001, # instruct time
			1.00,	 # present instruction auditorily
			-0.0001, # wait for scan pulse
			self.standard_parameters['timing_stimulus_duration'] * self.standard_parameters['TR'], # present stimulus
			self.standard_parameters['timing_ITI_duration'] * self.standard_parameters['TR'] ])	# ITI

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (-.5,-0.5,-0.5), opacity = 1.0, maskParams = {'fringeWidth':0.4})
		
		#ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stimulus_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		#self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def close(self):
		super(OriColorSession, self).close()

		parsopf = open(self.output_file + '_trialOrder.pickle', 'a')

		output = {}
		output['trialOrder'] = self.trial_array
		output['positionOrder'] = self.stimulus_positions

		pickle.dump(output,parsopf)

		# with open(self.output_file_name, 'w') as f:
		# 	pickle.dump(self.trial_array, f)
		# for s in self.staircases.keys():
		# 	print 'Staircase {}, mean {}, standard deviation {}'.format(s, self.staircases[s].mean(), self.staircases[s].sd())
		
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials

		for i in range(5,10):#len(self.trial_array[0])):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.standard_parameters.copy()
			this_trial_parameters['ori_color'] = self.trial_array[:,i]
			# this_trial_parameters['colors'] = [self.colors[self.trial_array[i,1]], self.colors[self.trial_array[i,3]], self.colors[self.trial_array[i,5]], self.colors[self.trial_array[i,7]]]

			these_phase_durations = self.phase_durations.copy()

			this_trial = OriColorTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
		# Save both separate frame images and movie (attempt)
		self.screen.saveMovieFrames('movie/expframe.png')			
		#slef.screen.saveMovieFrames('expdemo.mp4', codec = 'libx264')
	

