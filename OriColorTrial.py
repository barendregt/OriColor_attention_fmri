from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from OriColorStim import *
from Trial import *

class OriColorTrial(Trial):
	def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
		super(OriColorTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
		
		self.stim = OriColorStim(self.screen, self, self.session, trial_params = self.parameters['stimulus_params'])
		
		this_instruction_string = 'Waiting for scanner to start...'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))

		self.fix_col_val = 0.0

		self.run_time = 0.0
		self.instruct_time = self.t_time = self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
		self.instruct_sound_played = False
		
		self.parameterDict = self.parameters.copy()
	
	def draw(self):
		"""docstring for draw"""
		if (self.phase == 0) or (self.phase == 2):
			self.session.fixation.color = (self.fix_col_val, self.fix_col_val, self.fix_col_val)
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
		
		elif self.phase == 1:
			self.phase_time = self.session.clock.getTime()
			self.stim.draw(phase = self.phase_time - self.phase_time_start)

			self.session.fixation.color = (self.fix_col_val, self.fix_col_val, self.fix_col_val)
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()

			
		super(OriColorTrial, self).draw( )
		# self.screen.getMovieFrame() # Save frame for movie, outside scanner!		

	def event(self):
		for ev in event.getKeys():
			if len(ev) > 0:
				if ev in ['esc', 'escape']:
					self.events.append([-99,self.session.clock.getTime()-self.start_time])
					self.stopped = True
					self.session.stopped = True
					print 'run canceled by user'
				# it handles both numeric and lettering modes 
				elif ev == ' ':
					self.events.append([0,self.session.clock.getTime()-self.start_time])
					if (self.phase == 0) & (self.ID==0):
						self.phase_forward()
					# else:
					# 	self.events.append([-99,self.session.clock.getTime()-self.start_time])
					# 	self.stopped = True
					# 	print 'trial canceled by user'
				# elif ev == 't': # TR pulse
				# 	# self.events.append([99,self.session.clock.getTime()-self.start_time])
				# 	# if (self.phase == 0) + (self.phase==2):
				# 	# 	self.phase_forward()
				elif ev in self.session.response_buttons.keys():

					# Check if the response is within the time window
					#if self.session.clock.getTime() < self.session.response_timing[1]:
						
					if self.session.response_buttons[ev] == self.session.task_direction:
						response = 1						
					else:
						response = 0

					self.session.staircase.answer(response)

					self.session.task_responded = True


					# first check, do we even need an answer?
					# if self.phase == 3:
						# if self.stim.last_sampled_staircase != None:
						# 	# what value were we presenting at?
						# 	test_value = self.session.staircases[self.stim.last_sampled_staircase].quantile()
						# 	if self.session.tasks[self.parameters['task_index']] == 'Color':
						# 		response = self.session.response_button_signs[ev]*self.stim.present_color_task_sign
						# 	elif self.session.tasks[self.parameters['task_index']] == 'Speed':
						# 		response = self.session.response_button_signs[ev]*self.stim.present_speed_task_sign
						# 	elif self.session.tasks[self.parameters['task_index']] == 'Fix':
						# 		response = self.session.response_button_signs[ev]*self.stim.present_fix_task_sign
						# 	elif self.session.tasks[self.parameters['task_index']] == 'Fix_no_stim':
						# 		response = self.session.response_button_signs[ev]*self.stim.present_fns_task_sign

						# 	# update the staircase
						# 	self.session.staircases[self.stim.last_sampled_staircase].update(test_value,(response+1)/2)
						# 	# now block the possibility of further updates
						# 	self.stim.last_sampled_staircase = None

						# 	if self.session.tasks[self.parameters['task_index']] != 'Fix_no_stim':tt
						# 		log_msg = 'staircase %s bin %d updated from %f after response %s at %f'%( self.session.tasks[self.parameters['task_index']], self.stim.eccentricity_bin,test_value, str((response+1)/2), self.session.clock.getTime() )
						# 	else:
					log_msg = 'staircase updated from %f to %f after response %s [key %s, dir %d] at %f'%( self.session.task_direction*self.session.last_task_val, self.session.task_direction*self.session.staircase.get_intensity(), str(response), ev,self.session.response_buttons[ev], self.session.clock.getTime() )

					self.events.append( log_msg )
					print log_msg

					if self.session.tracker:
						self.session.tracker.log( log_msg )



				# add answers based on stimulus changes, and interact with the staircases at hand
				# elif ev == 'b' or ev == 'right': # answer pulse
				event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
				self.events.append(event_msg)
		
			super(OriColorTrial, self).key_event( ev )


	# def run(self, ID = 0):
	# 	self.ID = ID
	# 	super(OriColorTrial, self).run()
		
	# 	while not self.stopped:
	# 		self.run_time = self.session.clock.getTime() - self.start_time
	# 		# Only in trial 1, phase 0 represents the instruction period.
	# 		# After the first trial, this phase is skipped immediately
	# 		if self.phase == 0:
	# 			self.instruct_time = self.session.clock.getTime()
	# 			if self.ID != 0:
	# 				self.phase_forward()
	# 		# In phase 1, we present the task instruction auditorily
	# 		if self.phase == 1:
	# 			self.fix_time = self.session.clock.getTime()
	# 			# if not self.instruct_sound_played:
	# 			# 	self.session.play_sound(self.session.task_instructions[self.parameters['task_index']].lower())
	# 			# 	self.instruct_sound_played = True
	# 			# this trial phase is timed
	# 			# if( self.fix_time  - self.instruct_time ) > self.phase_durations[1]:
	# 			self.phase_forward()
	# 		# In phase 2, we wait for the scanner pulse (t)
	# 		if self.phase == 2:
	# 			self.t_time = self.session.clock.getTime()
	# 			if self.session.scanner == 'n':
	# 				self.phase_forward()
	# 		# In phase 3, the stimulus is presented
	# 		if self.phase == 3:
	# 			self.stimulus_time = self.session.clock.getTime()
	# 			if ( self.stimulus_time - self.t_time ) > self.phase_durations[3]:
	# 				self.phase_forward()
	# 		# Phase 4 reflects the ITI
	# 		if self.phase == 4:
	# 			self.post_stimulus_time = self.session.clock.getTime()
	# 			if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[4]:
	# 				self.stopped = True
		
	# 		# events and draw
	# 		self.event()
	# 		self.draw()

	
	# 	self.stop()


	def run(self, ID = 0):
		self.ID = ID
		super(OriColorTrial, self).run()
		self.parameterDict.update({'trial_start': self.start_time})

		#print self.start_time
		task_msg_printed = False
		while not self.stopped:
			self.run_time = self.session.clock.getTime() - self.start_time

			if self.run_time >= self.phase_durations.sum():
				self.stopped = True
				break

			if self.run_time >= np.sum(self.phase_durations[0:(self.phase+1)]):
				self.phase_forward()
				self.phase_time_start = self.session.clock.getTime()

			if self.phase == len(self.phase_durations):
				self.stopped = True
				break

			if self.session.time_for_next_task():
				if ~task_msg_printed:
					log_msg = 'Running task at %f' % (self.session.clock.getTime())
					self.events.append( log_msg )
					task_msg_printed = True

				if self.session.run_type==0:
					self.fix_col_val = self.session.task_direction * 0.5#self.session.task_direction * min([max([self.session.staircase.get_intensity(), 0.01]), 0.99])
					#self.session.last_task_val = min([max([self.session.staircase.get_intensity(), 0.01]), 0.99]) 
				else:
					self.fix_col_val = self.session.task_direction * 0.5#np.random.rand()
				self.session.last_task_val = np.abs(self.fix_col_val)
			else:
				self.fix_col_val = 0.0

			# events and draw
			self.event()
			self.draw()
			


		#print self.run_time
		self.stop()		
		