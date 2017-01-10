import sys, datetime
from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from ExpectationSession import *



def run_first_phase(root,e):
	#print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

	sid = e['SubjectID'].get().strip()

	if (not sid) or (sid == ""):
		Label(root, text = 'Please enter a subject ID!').pack()
	else:
		ts = ExpectationSession( sid, 0, False, True )
		root.quit()
		ts.run()		

def run_second_phase(root,e):
   #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

	sid = e['SubjectID'].get().strip()
	run = e['Run nr'].get().strip()

	if (not sid) or (sid == ""):
		Label(root, text = 'Please enter a subject ID!').pack()
	elif (not run) or (run == ""):
		Label(root, text = 'Run number must be 1 or higher').pack()
	else:

		run = int(run)

		if run <= 0:
			Label(root, text = 'Run number must be 1 or higher').pack()
		else:
			ts = ExpectationSession( sid, run, False, True )
			root.quit()
			ts.run()   
	
fields = 'SubjectID','Run nr','Timestamp'

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

if __name__ == '__main__':
   root = Tk()

   Label(root, text = 'Start training session').pack()

   ents = makeform(root, fields)

   ents['Timestamp'].insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

   # root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Run staircase',
          command=(lambda e=ents: run_first_phase(root,e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Run experiment',
          command=(lambda e=ents: run_second_phase(root,e)))
   b2.pack(side=LEFT, padx=5, pady=5) 
   root.mainloop()