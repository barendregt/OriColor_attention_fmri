import sys, datetime, glob
 # from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from TrainingSession import *

from plot_staircases import plot_staircases
# useTracker = True

def main():
   initials = raw_input('Subject initials: ')
   run_nr = int(raw_input('Run number: '))
   multi_task = raw_input('Multi task (y/n)?: ')
   if multi_task == 'n':
      task = [int(raw_input('Task (col=1,ori=2)?: '))]
   else:
      task = (1,2)
   scanner = raw_input('Are you in the scanner (y/n)?: ')
   track_eyes = raw_input('Are you recording gaze (y/n)?: ')
   if track_eyes == 'y':
      tracker_on = True
   elif track_eyes == 'n':
      tracker_on = False

   # appnope.nope()

   ts = ExpectationSession( initials, run_nr, scanner, tracker_on, task )
   ts.run()

   # data_dir = '/home/xiaomeng/Data/Pre_scan_data/'
   # figure_dir = '/home/xiaomeng/Data/Pre_scan_data/'
   #figure_dir = '/home/shared/2017/visual/Attention/behaviour/'
   # staircases = pickle.load(open('data/' + initials + '_staircase.pickle','rb'))
   # lab k2d38
   # data_dir = 'C:/Userdata/Martijn/OriColor_atention_fmri/data'
   # figure_dir = 'C:/Userdata/Martijn/OriColor_atention_fmri/data'

   # subject_dir= data_dir #os.path.join(data_dir,initials)
   # csv_files = glob.glob(subject_dir+'/*.csv')

   # subject_dir= data_dir #os.path.join(data_dir,initials)
   csv_files = glob.glob('data'+'/*.csv')
   # csv_files = glob.glob(subject_dir, '/*.csv')
   csv_files.sort()


   plot_staircases(csv_files, initials, run_nr)
    
if __name__ == '__main__':
   main()
      
