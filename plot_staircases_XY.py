
from matplotlib import pyplot as pl 
import numpy as np 
import cPickle as pickle
import glob
import seaborn as sn
import pandas as pd
import sys
sys.path.append( 'exp_tools' )

from Staircase import ThreeUpOneDownStaircase


from IPython import embed as shell


#def plot_staircases(initials,run_nr):


stairs = ['color','ori']# ['red','green','ori']
all_initials = ['ms','sl']

shell()

for initials in all_initials:

	# Load staircase data
	staircases = pickle.load(open('data/' + initials + '_staircase.pickle','rb'))

	# shell()
	# Compute average performance over time
	percent_correct = list()
	for ii in range(len(staircases)):

		responses = staircases[ii].past_answers

		percent_correct.append(np.cumsum(responses) / np.arange(1,len(responses)+1))


	# Plot average resp correct over time

	f = pl.figure()

	for s in range(len(stairs)):
		pl.plot(percent_correct[s],'-')
	pl.legend(stairs)

	pl.savefig('data/%s_staircase_plot.pdf'%(initials))


