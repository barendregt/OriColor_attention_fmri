
from matplotlib import pyplot as pl 
import numpy as np 
import cPickle as pickle
import glob
import seaborn as sn
import pandas as pd

from IPython import embed as shell


def plot_staircases(initials,run_nr):

	stairs = ['red','green','ori']

	# Load staircase data
	data = pd.read_csv('data/' + initials + '_' + str(run_nr) + '_output.csv')

	num_of_staircases = identify_staircases(data)

	# shell()
	# Compute moving average
	win_len = 5
	avg_data = []
	for ii in range(0,len(data['correct_answer'])-win_len):
		avg_data.extend([np.mean(data['correct_answer'][ii:ii+win_len])])


	# Plot average resp correct over time

	f = pl.figure()

	pl.plot(avg_data,'k-')

	pl.tight_layout()

	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))




def identify_staircases(dataset):

	task = dataset['task']
	base_col = dataset['base_color_a']
	# base_ori = dataset['base_ori']



