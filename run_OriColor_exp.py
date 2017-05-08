import sys

sys.path.append( 'exp_tools' )

from OriColorSession import *
# from plot_staircases import *
# import appnope

def main():
	initials = raw_input('Your initials: ')
	run_nr = int(raw_input('Run number: '))
	run_type = int(raw_input('Run type (0=location, 1=full):'))
	scanner = raw_input('Are you in the scanner (y/n)?: ')
	track_eyes = raw_input('Are you recording gaze (y/n)?: ')
	if track_eyes == 'y':
		tracker_on = True
	elif track_eyes == 'n':
		tracker_on = False

	# appnope.nope()

	ts = OriColorSession( initials, run_nr, scanner, tracker_on, run_type )
	ts.run()

	# plot_staircases(initials, run_nr)
	
if __name__ == '__main__':
	main()