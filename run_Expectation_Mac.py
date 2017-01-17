import sys, datetime
# from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from ExpectationSession import *

# useTracker = True
sid = 'tt'
inScanner =0 
useTracker =0
expTask = 1

ts = ExpectationSession( sid, 0, inScanner, useTracker, expTask )
ts.run()		
