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
   
#data_dir = '/home/xiaomeng/Data/Pre_scan_data/'
#figure_dir = '/home/shared/2017/visual/Attention/behaviour/'
#csv_files = glob.glob(data_dir+'/*.csv')

#initials = "xy" #csv_files[0].split('_')[0]
#run_nr = 1 #csv_files[0].split('_')[1]

# lab k2d38
csv_files = glob.glob('data'+'\*.csv')
csv_files.sort()

def plot_staircases(initials,run_nr):

 	stairs = ['red','green','horizontal', 'vertical']

 	# Load staircase data
 	staircases = pickle.load(open('data/' + initials + '_training_staircase.pickle','rb'))

 	# Compute average performance over time
 	percent_correct = list()
	stair_values = list()
	responses = list()
	#n_responses =list()
	
 	for ii in range(len(staircases)):

 		responses.append(staircases[ii].past_answers)
		#n_responses.append()
		
		stair_values.append(staircases[ii].test_values)
		shell()
 		percent_correct.append(np.cumsum(np.array(responses)) / np.arange(1,len(responses)+1))
		
 	# Plot average resp correct over time

# 	f = pl.figure()
# 	for s in range(len(stairs)):
# 		pl.plot(percent_correct[s],'-')
# 	pl.legend(stairs)

	f = pl.figure(figsize = (25,15))
	training_indices =((0,1),(2,3),(4,5),(6,7))
	shell()
	for i in range(len(training_indices)):
		s = f.add_subplot(2,4,i+1)
		pl.plot(percent_correct[training_indices[i][0]],'-')
		pl.plot(percent_correct[training_indices[i][1]],'-')
		sn.despine(offset=10)
		s.set_title('ACC_' + stairs[i], fontsize = 20)
		
		s1 = f.add_subplot(2,4,i+5)
		pl.plot(stair_values[training_indices[i][0]], '-')
		pl.plot(stair_values[training_indices[i][1]], '-')
		sn.despine(offset=10)
		s1.set_title('staircase_' + stairs[i], fontsize = 20)
	
 	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))


