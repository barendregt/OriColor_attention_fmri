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

from OriColorSession import *
from MapperTrial import *
from standard_parameters import *
# from Staircase import YesNoStaircase

import appnope
appnope.nope()

class MapperSession(OriColorSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on):
		super(MapperSession, self).__init__( subject_initials, index_number, scanner, tracker_on)
	
	def close(self):
		super(MapperSession, self).close()

	def prepare_trials(self):

		self.standard_parameters = standard_parameters

		# self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps'])

		# self.orientations = np.linspace(self.standard_parameters['stimulus_ori_min'], self.standard_parameters['stimulus_ori_max'], self.standard_parameters['stimulus_ori_steps']+1)
		# self.orientations = self.orientations[0:(self.standard_parameters['stimulus_ori_steps'])]

		# self.colors = np.linspace(0.0, 1.0, self.standard_parameters['stimulus_col_steps']+1)
		# self.colors = self.colors[0:(self.standard_parameters['stimulus_col_steps'])]			 

		self.stimulus_positions = self.standard_parameters['stimulus_positions']
		
		self.trial_array = []
	
		pos_array = []

		for a in range(2):
			for b in range(2):
				for c in range(2):
					for d in range(2):
						pos_array.append([a,b,c,d])	

		pos_array = pos_array  * 5	

		for x in range(5):
			pos_array.append([0,0,0,0])

		prepend_list = [[0,0,0,0] for i in range(5)]
		prepend_list.extend(pos_array)

		self.trial_array = np.array(prepend_list)

		tmp = self.trial_array[5:-5,:]
		np.random.shuffle(tmp)

		self.trial_array[5:-5,:] = tmp

		self.phase_durations = np.array([
			-0.0001, # instruct time
			1.00,	 # present instruction auditorily
			-0.0001, # wait for scan pulse
			self.standard_parameters['timing_stimulus_duration'] * self.standard_parameters['TR'], # present stimulus
			self.standard_parameters['timing_ITI_duration'] * self.standard_parameters['TR'] ])	# ITI

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (-.5, -.5 ,-.5), opacity = 1.0, maskParams = {'fringeWidth':0.4})

	
	def close(self):
		super(MapperSession, self).close()

		parsopf = open(self.output_file + '_HRFmapper_trialOrder.pickle', 'a')

		output = {}
		output['trialOrder'] = self.trial_array
		output['positionOrder'] = self.stimulus_positions

		pickle.dump(output,parsopf)
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials

		for i in range(len(self.trial_array)):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.standard_parameters.copy()
			this_trial_parameters['ori_color'] = self.trial_array[i,:]
			# this_trial_parameters['colors'] = [self.colors[self.trial_array[i,1]], self.colors[self.trial_array[i,3]], self.colors[self.trial_array[i,5]], self.colors[self.trial_array[i,7]]]

			these_phase_durations = self.phase_durations.copy()

			this_trial = MapperTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
	

