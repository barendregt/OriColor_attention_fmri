from __future__ import division
from psychopy import visual, core, misc, event
from psychopy.data import StairHandler
import numpy as np
from IPython import embed as dbstop
from math import *

import os, sys, time, datetime, cPickle
import pygame
from pygame.locals import *

sys.path.append( 'exp_tools' )


import Quest
from Session import *
from ExpectationTrial import *
from standard_parameters import *


class ExpectationSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on, task):
		super(ExpectationSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = screen_res, full_screen = 1, physical_screen_distance = screen_dist, background_color = background_color, physical_screen_size = screen_size, screen_nr = screen_num )

		self.create_output_file_name()
		if tracker_on:
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
			if self.tracker_on:
				self.tracker_setup()
		else:
			self.create_tracker(tracker_on = False)
		
		self.response_buttons = response_buttons

		self.scanner = scanner
		self.setup_sounds()

		self.task = task

		self.fileOperations = {}
		
		self.standard_parameters = standard_parameters
		
		self.trialID = -1

		self.pdOutput = list()
		# trials can be set up independently of the staircases that support their parameters
		
		self.parameter_names = ['base_ori', 'base_r', 'base_g', 'base_b', 'ori_offset', 'color_offset', 'stim_type', 'task', 'x', 'y']
		
		

		# if os.path.isfile(os.path.join('data', self.subject_initials + '_' + str(self.index_number) + '_INPROGRESS.pickle')):
		# 	print 'Found previous data file for this run, loading to continue'

		# 	f = open(os.path.join('data', self.subject_initials + '_' + str(self.index_number) + '_INPROGRESS.pickle'),'rb')

		# 	self.outputDict, self.pdOutput, self.trial_array, self.events, self.trialID, self.fileOperations = cPickle.load(f)

		# else:
			
		# 	pfile = open(os.path.join('data', self.subject_initials + '_staircase.txt'),'r')
		# 	#self.staircases = cPickle.load(pfile)
		# 	self.staircases = pfile.read().split(";")
		# 	pfile.close()

		self.prepare_staircases()
		self.prepare_trials()
		

	def setup_sounds(self):
		"""initialize pyaudio backend, and create dictionary of sounds."""
		self.pyaudio = pyaudio.PyAudio()

		task_sounds = [['lowToneSingle.wav','lowToneDouble.wav','highToneSingle.wav','highToneDouble.wav'],
				   ['highToneSingle.wav','highToneDouble.wav','lowToneSingle.wav','lowToneDouble.wav'],
				   ['lowToneSingle.wav','highToneSingle.wav','lowToneDouble.wav','highToneDouble.wav'],
				   ['lowToneDouble.wav','highToneDouble.wav','lowToneSingle.wav','highToneSingle.wav'],
				   ['lowToneDouble.wav','lowToneSingle.wav','highToneDouble.wav','highToneSingle.wav'],
				   ['highToneDouble.wav','highToneSingle.wav','lowToneDouble.wav','lowToneSingle.wav'],
				   ['highToneSingle.wav','lowToneSingle.wav','highToneDouble.wav','lowToneDouble.wav'],
				   ['highToneDouble.wav','lowToneDouble.wav','highToneSingle.wav','lowToneSingle.wav']					   
					  ]

		if not os.path.isfile(os.path.join('data', self.subject_initials + '_soundmap.txt')):
			f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'w')			

			f.write(','.join(task_sounds[np.random.randint(len(task_sounds))]))
			f.close()

		f = open(os.path.join('data', self.subject_initials + '_soundmap.txt'),'r')

		sub_task_sounds = f.read().split(",")

		self.sound_files = {
						   'red45' : 'sounds/' + sub_task_sounds[0],
						   'red135' : 'sounds/' + sub_task_sounds[1],
						   'green45' : 'sounds/' + sub_task_sounds[2],
						   'green135' : 'sounds/' + sub_task_sounds[3]
						   }
		self.sounds = {}
		for sf in self.sound_files:
			self.read_sound_file(file_name = self.sound_files[sf], sound_name = sf)
		# print self.sounds
	
	
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
			self.standard_parameters['timing_responseDuration'] # wait for response			
			])	# ITI

		## TRIAL DESIGN: 
		#stim_types = np.vstack([[(a,b) for a in self.standard_parameters['session_types']] for b in self.standard_parameters['tasks']])			
		stim_types = self.standard_parameters['session_types']

		self.trials = list()

		
		trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])
		stim_labels = ['red0','red90','green0','green90']#['red45','red135','green45','green135']
		# trial_labels = ['base','P-UP','UP-P','UP-UP']

		nTrialsPerStim = self.standard_parameters['ntrials_per_stim']

		for ttype in range(len(trial_types)):
			# for stype in range(len(stim_types)):

				for ii in range(nTrialsPerStim):
					
					this_trial_parameters = {'base_ori': trial_types[ttype][0],
											'base_color_lum': trial_types[ttype][1],
											'base_color_a': trial_types[ttype][2],
											'base_color_b': trial_types[ttype][3],
											'trial_stimulus_label': stim_labels[ttype],
											'trial_stimulus': ttype,
											'task': self.task,
											'trial_position_x': 0.0,
											'trial_position_y': 0.0																											 																												 
											}

					self.trials.append(this_trial_parameters)

		shuffle(self.trials)

		xy_positions = self.standard_parameters['stimulus_positions'] * nTrialsPerStim * 4

		for tii in range(len(self.trials)):
			self.trials[tii]['trial_position_x'] = xy_positions[tii][0]
			self.trials[tii]['trial_position_y'] = xy_positions[tii][1]


	def prepare_staircases(self):

		# Create a separate staircase for every stimulus

		self.staircases = list([0] * len(self.standard_parameters['quest_initial_stim_values']))

		for stimt in range(0,len(self.standard_parameters['quest_initial_stim_values'])):

			self.staircases[stimt] = StairHandler(self.standard_parameters['quest_initial_stim_values'][stimt], 
												  stepSizes=self.standard_parameters['quest_stepsize'][stimt], 
												  # nTrials = 500,
												  nUp=1, nDown=3, 
												  # method='2AFC', 
												  stepType='db', 
												  minVal=0.0,
												  maxVal=75)


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
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()		
		
		#self.outputDict['trials'] = self.trial_array

		super(ExpectationSession, self).close()

		#if self.index_number == 0:

		parsopf = open(os.path.join('data', self.subject_initials + '_staircase.pickle'), 'wb')

		cPickle.dump(self.staircases,parsopf)

		f = open(os.path.join('data', self.subject_initials + '_staircase.txt'), 'w')
		f.write(";".join([str(self.staircases[s].next()) for s in range(len(self.staircases))]))			
		f.close()

#		
#		data = pd.concat(self.pdOutput)	
#		data.to_csv(os.path.join('data', self.output_file + '_output.csv'))
#		
		# with open(self.output_file_name, 'w') as f:
		# 	pickle.dump(self.trial_array, f)
		# for s in self.staircases.keys():
		# 	print 'Staircase {}, mean {}, standard deviation {}'.format(s, self.staircases[s].mean(), self.staircases[s].sd())
		
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})


		# Wait to start th experiment
		self.fixation_outer_rim.draw()
		self.fixation_rim.draw()
		self.fixation.draw()

		this_instruction_string = 'Press spacebar to start'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		event.waitKeys(keyList = ['space'])

		event.clearEvents()

		if self.trialID >= 0:
			rStart = self.trialID
		else:
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
			
		self.close()
	

