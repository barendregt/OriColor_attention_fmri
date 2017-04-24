from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as dbstop
from math import *
import random, sys
import ColorTools as ct

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class OriColorStim(object):
	def __init__(self, screen, trial, session, trial_params):
		# parameters
		
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = session.standard_parameters['stimulus_size'] * session.pixels_per_degree
		
		# self.orientation = orientation	# convert to radians immediately, and use to calculate rotation matrix

		self.trial_params = trial_params

		self.orientations = []
		self.positions = []
		self.colors = []

		self.element_array = []

		# for i,c in enumerate(self.trial_params):
		# 	if len(c):

		# 		#self.element_array.append(visual.GratingStim(self.screen, tex = 'sqr', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = self.session.standard_parameters['stimulus_base_spatfreq'], ori = c[0], units = 'pix',  size = (self.size_pix, self.size_pix), pos = (self.session.stimulus_positions[i][0]*self.session.pixels_per_degree, self.session.stimulus_positions[i][1]*self.session.pixels_per_degree), colorSpace = 'rgb', color = c[1:]))

		# 		# self.colors.append([rgbc*255.0 for rgbc in colorsys.hls_to_rgb(c[1], .5, 1)])
		# 		self.colors.append(c[1:])
		# 		self.positions.append((self.session.stimulus_positions[i][0]*session.pixels_per_degree,self.session.stimulus_positions[i][1]*session.pixels_per_degree))
		# 		self.orientations.append(c[0])

		self.period = session.standard_parameters['mapper_stimulus_duration'] * session.standard_parameters['TR']
		self.refresh_frequency = self.period / session.standard_parameters['mapper_n_redraws']

		self.phase = 0
		# bookkeeping variables
		self.eccentricity_bin = -1
		self.redraws = 0
		self.last_redraw = 0
		self.frames = 0
		self.last_stimulus_present_for_task = 0

		# psychopy stimuli
		self.fix_gray_value = (0,0,0)

		# self.populate_stimulus()

		# make this stimulus array a session variable, in order to have to create it only once...
		# if not hasattr(session, 'element_array'):
		self.element_array = None
		if len(self.trial_params):
			# try:
				#self.element_array = visual.ElementArrayStim(screen, elementTex = 'sqr', elementMask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, nElements = 1, sizes = session.standard_parameters['stimulus_size'] * session.pixels_per_degree, sfs = session.standard_parameters['stimulus_base_spatfreq'], xys = self.trial_params[4:][np.newaxis,:] * session.pixels_per_degree, oris = self.trial_params[0], colors = self.trial_params[1:4], colorSpace = 'rgb', units='pix') 
				#self.element_array = visual.GratingStim(screen, tex = 'sqr', mask = None, size = np.array([[2560, 2560]]), sf = session.standard_parameters['stimulus_base_spatfreq'], pos = np.array([[0,0]]) * session.pixels_per_degree, ori = self.trial_params[0], color = self.trial_params[1:4], colorSpace = 'rgb', units='pix') 
			self.element_array = visual.GratingStim(screen, tex = 'sqr', mask = session.standard_parameters['stimulus_mask'], maskParams = {'fringeWidth': 0.6}, size = session.standard_parameters['stimulus_size'] * session.pixels_per_degree, sf = session.standard_parameters['stimulus_base_spatfreq'], pos = self.trial_params[4:][np.newaxis,:] * session.pixels_per_degree, ori = self.trial_params[0], color = self.trial_params[1:4], colorSpace = 'rgb', units='pix') 
				# dbstop()

	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		if self.element_array is not None:#len(self.element_array):

			if (self.phase - self.last_redraw) > self.refresh_frequency:
				self.redraws += 1

				self.last_redraw = self.phase

					# self.populate_stimulus()
				# for ii in range(len(self.element_array)):
				# 	self.element_array[ii].phase = (self.redraws * 0.5) % 1

				
			# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
				self.element_array.phase = (self.redraws * 0.5) % 1
			# for ii in range(len(self.element_array)):
			# 	self.element_array[ii].draw()
			self.element_array.draw()
		# log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
		# self.trial.events.append( log_msg )
		# if self.session.tracker:
		# 	self.session.tracker.log( log_msg )			
		
		# self.session.fixation_outer_rim.draw()
		# self.session.fixation_rim.draw()
		# self.session.fixation.setColor(self.fix_gray_value)
		# self.session.fixation.draw()

		# self.session.mask_stim.draw()
		
	