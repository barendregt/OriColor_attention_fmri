from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as dbstop
from math import *
import random, sys
import colorsys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class MapperStim(object):
	def __init__(self, screen, trial, session, orientation):
		# parameters
		
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = session.standard_parameters['stimulus_size'] * session.screen_pix_size[1]
		
		# self.orientation = orientation	# convert to radians immediately, and use to calculate rotation matrix

		self.orientations = []
		self.positions = []
		self.colors = []

		for i,c in enumerate(orientation):
			if c==1:
				# self.colors.append([rgbc*255.0 for rgbc in colorsys.hls_to_rgb(c[1], .5, 1)])
				self.positions.append((self.session.stimulus_positions[i][0]*session.pixels_per_degree,self.session.stimulus_positions[i][1]*session.pixels_per_degree))
				# self.orientations.append(c[0])

		self.period = session.standard_parameters['timing_stimulus_duration'] * session.standard_parameters['TR']
		self.refresh_frequency = session.standard_parameters['timing_mapper_redraws'] / session.standard_parameters['TR']

		self.phase = 0
		# bookkeeping variables
		self.eccentricity_bin = -1
		self.redraws = 0
		self.frames = 0
		self.last_stimulus_present_for_task = 0

		# psychopy stimuli
		self.fix_gray_value = (0,0,0)

		# self.populate_stimulus()

		# make this stimulus array a session variable, in order to have to create it only once...
		# if not hasattr(session, 'element_array'):

		# x,y = np.meshgrid(range(1000), range(1000))

		# checkboard = np.sign(round((np.cos((x)*(2*pi)))/2+.5)*2-1)

		self.element_array = None
		if len(self.positions):
			self.element_array = visual.ElementArrayStim(screen, elementTex = 'sqrXsqr', elementMask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, nElements = len(self.positions), sizes = session.standard_parameters['stimulus_size'] * session.pixels_per_degree, phases = 0.0, sfs = session.standard_parameters['stimulus_sf'], xys = self.positions) 

	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		if self.element_array is not None:

			if self.redraws <= (self.phase * self.period * self.refresh_frequency):
				self.redraws = self.redraws + 1

				# self.populate_stimulus()
				self.element_array.setPhases(np.random.rand(len(self.positions)))
				#self.element_array.setOris(90.0)

				
			# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
			# self.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

			self.element_array.draw()

		log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
		self.trial.events.append( log_msg )
		if self.session.tracker:
			self.session.tracker.log( log_msg )			
		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.setColor(self.fix_gray_value)
		self.session.fixation.draw()

		# self.session.mask_stim.draw()
		
		