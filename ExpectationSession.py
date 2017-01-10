from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
from IPython import embed as dbstop
from math import *

import os, sys, time, datetime, cPickle
import pygame
from pygame.locals import *
# from pygame import mixer, time



sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


import Quest
from Session import *
from ExpectationTrial import *
from standard_parameters import *
# from Staircase import YesNoStaircase

# import appnope
# appnope.nope()

class ExpectationSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on):
		super(ExpectationSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

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

		self.fileOperations = {}
		
		self.standard_parameters = standard_parameters
		
		self.trialID = -1

		self.pdOutput = list()
		# trials can be set up independently of the staircases that support their parameters
		
		self.parameter_names = ['base_ori', 'base_r', 'base_g', 'base_b', 'ori_offset', 'color_offset', 'stim_type', 'task', 'x', 'y']
		if (self.index_number == 0) or (not os.path.isfile(os.path.join('data', self.subject_initials + '_staircase.pickle'))):
			self.prepare_trials_first_run()
			self.prepare_staircases()

		elif os.path.isfile(os.path.join('data', self.subject_initials + '_' + str(self.index_number) + '_INPROGRESS.pickle')):
			print 'Found previous data file for this run, loading to continue'

			f = open(os.path.join('data', self.subject_initials + '_' + str(self.index_number) + '_INPROGRESS.pickle'),'rb')

			self.outputDict, self.pdOutput, self.trial_array, self.events, self.trialID, self.fileOperations = cPickle.load(f)

			# self.trial_array = tmp.trial_array
			# self.trialID = tmp.trialID
			# self.outputDict = tmp.outputDict
			# self.pdOutput = tmp.pdOutput
		else:
			
			pfile = open(os.path.join('data', self.subject_initials + '_staircase.txt'),'r')
			#self.staircases = cPickle.load(pfile)
			self.staircases = pfile.read().split(";")
			pfile.close()

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
	
	def prepare_trials_first_run(self):
		"""docstring for prepare_trials(self):"""

		

#		probs = {0: (1.0, 0.0, 0.0, 0.0),
#			  1: (0.0, 1.0, 0.0, 0.0),
#			  2: (0.0, 0.0, 1.0, 0.0),
#			  3: (0.0, 0.0, 0.0, 1.0) }

		## TRIAL DESIGN: 
		
		stim_types = np.vstack([[(a,b) for a in self.standard_parameters['session_types']] for b in self.standard_parameters['tasks']])

		np.random.shuffle(stim_types)

		#    [base_ori    base_color_r base_color_g base_color_b    ori_increment    red_increment   green_increment   position]
		# trial_types = np.vstack([[a, b[0], b[1], b[2]] for a in self.params['stimulus_base_orientation'] for b in zip(self.params['stimulus_base_color_r'], self.params['stimulus_base_color_g'], self.params['stimulus_base_color_b'])])
		trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])
		#trial_incs = np.vstack([[ori_inc, color_inc_r, color_inc_g] for ori_inc, color_inc_r, color_inc_g in zip(self.params['stimulus_orientation_offset'], self.params['stimulus_colors_r'], self.params['stimulus_colors_g'])])

		
		stim_type = stim_types[0]
		#stim_probs = probs[stim_type[0]]
		#trial_probs = (int(round( stim_probs[0] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[1] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[2] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[3] * self.standard_parameters['number_of_quest_trials'])))
		trial_bases = np.tile(trial_types[stim_type[0]], (self.standard_parameters['number_of_quest_trials']/len(stim_types),1))
		trial_params = np.hstack([trial_bases, np.ones((len(trial_bases),1))*stim_type[0], np.ones((len(trial_bases),1)) * stim_type[1]])
		
		for ii in range(1,len(stim_types)):
			stim_type = stim_types[ii]
			#stim_probs = probs[stim_type[0]]
			#trial_probs = (int(round( stim_probs[0] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[1] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[2] * self.standard_parameters['number_of_quest_trials'])), int(round( stim_probs[3] * self.standard_parameters['number_of_quest_trials'])))
			trial_bases = np.tile(trial_types[stim_type[0]], (self.standard_parameters['number_of_quest_trials']/len(stim_types),1))
			trial_params = np.vstack([trial_params, np.hstack([trial_bases, np.ones((len(trial_bases),1))*stim_type[0], np.ones((len(trial_bases),1)) * stim_type[1]])])
		
		# if self.exptype == 'T':
		trial_params = trial_params[np.random.permutation(len(trial_params))]

		self.trial_array = np.hstack([trial_params, np.tile(self.standard_parameters['stimulus_position'],(len(trial_params),1))])

		# self.phase_durations = np.array([
		# 	self.standard_parameters['timing_ITI_duration'], 	# inter trial interval
		# 	self.standard_parameters['timing_cue_duration'],	# present first cue (audio)
		# 	self.standard_parameters['timing_cue_duration'],	# present second cue (task)
		# 	self.standard_parameters['timing_stimcue_interval'],# wait before presenting stimulus
		# 	self.standard_parameters['timing_stim_1_Duration'], # present first stimulus
		# 	self.standard_parameters['timing_ISI'], 			# inter stimulus interval
		# 	self.standard_parameters['timing_stim_2_Duration'], # present second stimulus
		# 	self.standard_parameters['timing_responseDuration'] # wait for response			
		# 	])	# ITI

		# # fixation point
		# self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.2 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		# self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.2 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		# self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.2 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})
		
		
		#ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stimulus_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		#self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		# self.standard_parameters = standard_parameters
		# dbstop()
		probs = {0: (0.7, 0.1, 0.1, 0.1), # green45
			   1: (0.1, 0.7, 0.1, 0.1),
			   2: (0.1, 0.1, 0.7, 0.1),
			   3: (0.1, 0.1, 0.1, 0.7) }

		## TRIAL DESIGN: 
		stim_types = np.vstack([[(a,b) for a in self.standard_parameters['session_types']] for b in self.standard_parameters['tasks']])

		#np.random.shuffle(stim_types)

		ori_offsets_expected = float(self.staircases[self.standard_parameters['quest_o_index']]) * np.array(self.standard_parameters['test_values_expected'])
		col_offsets_expected = np.mean([float(self.staircases[self.standard_parameters['quest_r_index']]), float(self.staircases[self.standard_parameters['quest_g_index']])]) * np.array(self.standard_parameters['test_values_expected'])

		ori_offsets_unexpected = float(self.staircases[self.standard_parameters['quest_o_index']]) * np.array(self.standard_parameters['test_values_unexpected'])
		col_offsets_unexpected = np.mean([float(self.staircases[self.standard_parameters['quest_r_index']]), float(self.staircases[self.standard_parameters['quest_g_index']])]) * np.array(self.standard_parameters['test_values_unexpected'])


		# self.screen.close()
		# dbstop()

		#    [base_ori    base_color_lum base_color_a base_color_b    ori_increment    red_increment   green_increment stim_type task  position]

		trial_params = list()


		# trial_types = np.vstack([[a, b[0], b[1], b[2]] for a in self.params['stimulus_base_orientation'] for b in zip(self.params['stimulus_base_color_r'], self.params['stimulus_base_color_g'], self.params['stimulus_base_color_b'])])
		trial_types = np.vstack([[[a,b[0], b[1], b[2]] for a in self.standard_parameters['stimulus_base_orientation']] for b in self.standard_parameters['stimulus_base_colors']])
		trial_incs_expected = [[0.5, 0.5],[0.5, 0.5]]# np.vstack([[[ori_inc, color_inc] for ori_inc in ori_offsets_expected] for color_inc in col_offsets_expected])
		trial_incs_unexpected = [[10, 10], [10, 10]] #np.vstack([[[ori_inc, color_inc] for ori_inc in ori_offsets_unexpected] for color_inc in col_offsets_unexpected])

		# stim_type = stim_types[0]
		# stim_probs = probs[stim_type[0]] 

		# trial_probs = (int(round( stim_probs[0] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[1] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[2] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[3] * (self.standard_parameters['number_of_trials']/len(stim_types)))))
		#trial_bases = np.vstack([np.tile(t, (p,1)) for t, p in zip(trial_types, trial_probs)])
		# trial_params = np.hstack([trial_bases, np.tile(trial_incs,(len(trial_bases)/len(trial_incs),1)), np.ones((len(trial_bases),1))*stim_type[0], np.ones((len(trial_bases),1)) * stim_type[1]])
		
		# for sp in stim_probs:
		# 	if sp == max(stim_probs):
		# 		trial_params.extend(np.hstack([np.tile(trial_types[sp],(len(trial_incs_expected),1)), trial_incs_expected, np.ones((len(trial_incs_expected),1))*stim_type[0], np.ones((len(trial_incs_expected),1)) * stim_type[1]]))
		# 	else:
		# 		trial_params.extend(np.hstack([np.tile(trial_types[sp],(len(trial_incs_unexpected),1)), trial_incs_unexpected, np.ones((len(trial_incs_unexpected),1))*stim_type[0], np.ones((len(trial_incs_unexpected),1)) * stim_type[1]]))
		dbstop()
		for ii in range(0,len(stim_types)):
			stim_type = stim_types[ii]
			stim_probs = probs[stim_type[0]]
			# trial_probs = (int(round( stim_probs[0] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[1] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[2] * (self.standard_parameters['number_of_trials']/len(stim_types)))), int(round( stim_probs[3] * (self.standard_parameters['number_of_trials']/len(stim_types)))))
			# trial_bases = np.vstack([np.tile(t, (p,1)) for t, p in zip(trial_types, trial_probs)])
			# trial_params = np.vstack([trial_params, np.hstack([trial_bases, np.tile(trial_incs,(len(trial_bases)/len(trial_incs),1)), np.ones((len(trial_bases),1))*stim_type[0], np.ones((len(trial_bases),1)) * stim_type[1]])])
			for ii,sp in enumerate(stim_probs):
				if sp == max(stim_probs):
					trial_params.extend(np.hstack([np.tile(trial_types[ii],(len(trial_incs_expected),1)), trial_incs_expected, np.ones((len(trial_incs_expected),1))*stim_type[0], np.ones((len(trial_incs_expected),1)) * stim_type[1],np.ones((len(trial_incs_expected),1))]))
				else:
					trial_params.extend(np.hstack([np.tile(trial_types[ii],(len(trial_incs_unexpected),1)), trial_incs_unexpected, np.ones((len(trial_incs_unexpected),1))*stim_type[0], np.ones((len(trial_incs_unexpected),1)) * stim_type[1],np.zeros((len(trial_incs_unexpected),1))]))			

		trial_params = np.array(trial_params)

		#trial_params = trial_params[np.random.permutation(len(trial_params))]

		self.trial_array = np.hstack([trial_params, np.tile(self.standard_parameters['stimulus_position'],(len(trial_params),1))])

		#ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stimulus_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		#self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	

	def prepare_staircases(self):

		# Create a separate staircase for every stimulus

		self.staircases = list([0] * len(self.standard_parameters['quest_initial_stim_values']))
		#stim_types = {'ori45','ori135','colorR','colorG'}

		for stimt in range(0,len(self.standard_parameters['quest_initial_stim_values'])):

			self.staircases[stimt] = Quest.QuestObject(
											tGuess = self.standard_parameters['quest_initial_stim_values'][stimt],  
											tGuessSd = self.standard_parameters['quest_sd'][stimt], #self.params['initial_stim_values'][stimt]*2, 
											pThreshold = self.standard_parameters['quest_threshold'],#0.81, 
											beta = 3.5, 
											delta = 0.01,#0.05, #0.05, 
											gamma = 0.01,
											range = self.standard_parameters['quest_range'][stimt]) 	

		# self.last_sampled_staircase_ori = 1
		# self.last_sampled_staircase_colr = 1
		# self.last_sampled_staircase_colg = 1

	def partial_store(self, tid):
		data = pd.concat(self.pdOutput)	
		data.to_csv(self.output_file + '_output.csv')		

		if os.path.isfile(self.output_file + '_INPROGRESS.pickle'):
			self.fileOperations['lastModified'] = '%s' % datetime.datetime.now()
		else:
			self.fileOperations.update({'created': '%s' % datetime.datetime.now()})
			self.fileOperations.update({'lastModified': '%s' % datetime.datetime.now()})		

		parsopf = open(self.output_file + '_INPROGRESS.pickle', 'wb')
		cPickle.dump([self.outputDict, self.pdOutput, self.trial_array, self.events, tid, self.fileOperations], parsopf)
		# cPickle.dump(self.trialID, parsopf)
		parsopf.close()
		
	def close(self):
		
		this_instruction_string = 'Exporting data, please wait'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()		
		
		self.outputDict['trials'] = self.trial_array

		super(ExpectationSession, self).close()

		if self.index_number == 0:

			parsopf = open(os.path.join('data', self.subject_initials + '_staircase.pickle'), 'wb')

			cPickle.dump(self.staircases,parsopf)

			f = open(os.path.join('data', self.subject_initials + '_staircase.txt'), 'w')
			f.write(";".join([str(self.staircases[s].quantile()) for s in range(len(self.staircases))]))			
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


		self.phase_durations = np.array([
			self.standard_parameters['timing_ITI_duration'], 	# inter trial interval
			self.standard_parameters['timing_cue_duration'],	# present first cue (audio)
			self.standard_parameters['timing_cue_duration'],	# present second cue (task)
			self.standard_parameters['timing_stimcue_interval'],# wait before presenting stimulus
			self.standard_parameters['timing_stim_1_Duration'], # present first stimulus
			self.standard_parameters['timing_ISI'], 			# inter stimulus interval
			self.standard_parameters['timing_stim_2_Duration'], # present second stimulus
			self.standard_parameters['timing_responseDuration'] # wait for response			
			])	# ITI		

		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=0.5 * self.pixels_per_degree, pos = np.array((0.0,0.0)), color = (1.0, 1.0, 1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})


		# Wait to start th experiment
		self.fixation_outer_rim.draw()
		self.fixation_rim.draw()
		self.fixation.draw()

		this_instruction_string = 'Press spacebar to start'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, -100.0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))
		self.instruction.draw()

		self.screen.flip()

		event.waitKeys(keyList = ['space'])

		event.clearEvents()

		if self.trialID >= 0:
			rStart = self.trialID
		else:
			rStart = 0

		for self.trialID in range(rStart, len(self.trial_array)):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.trial_array[self.trialID,:]			

			print 'Running trial ' + str(self.trialID)

			these_phase_durations = self.phase_durations.copy()
			these_phase_durations[0] = these_phase_durations[0][0] + np.random.rand()*these_phase_durations[0][1]

			this_trial = ExpectationTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = self.trialID)
			
			if self.index_number > 0:
				self.partial_store(self.trialID)			
			
			if self.stopped == True:
				break
			
			if (self.trialID > 0) and ((self.trialID % self.standard_parameters['trials_to_break'])==0):
				
				if self.tracker_on:
					self.tracker.stop_recording()
				
				self.fixation_outer_rim.draw()
				self.fixation_rim.draw()
				self.fixation.draw()
		
				this_instruction_string = 'Take a break! Press spacebar to continue, or q to stop.'# self.parameters['task_instruction']
				self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, -100.0), italic = True, height = 20, alignHoriz = 'center')
				self.instruction.setSize((1200,50))
				self.instruction.draw()
		
				self.screen.flip()
		
				keys = event.waitKeys(keyList = ['space','q'])
		
				if 'q' in keys:
					break
		
				event.clearEvents()		
				
				if self.tracker_on:
					self.tracker_setup()
		self.close()
	

