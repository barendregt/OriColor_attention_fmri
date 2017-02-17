import sys, datetime
from Tkinter import *

from IPython import embed

sys.path.append( 'exp_tools' )

from ExpectationSession import *
from plot_staircases import plot_staircases

# useTracker = True

def run_first_phase(root,e,inScanner=False,useTracker=False,expTask=1):
	#print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

   sid = e['SubjectID'].get().strip()
   run = e['Run nr'].get()

   print (sid, inScanner.get(),useTracker.get(),expTask.get())

   if (not sid) or (sid == ""):
      Label(root, text = 'Please enter a subject ID!').pack()
   else:
      ts = ExpectationSession( sid, run, inScanner.get(), useTracker.get(), expTask.get() )
      root.quit()
      ts.run()	
      plot_staircases(sid, run)	
	
fields = 'SubjectID','Run nr'#,'Timestamp'

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      lab.config(font=("Arial", 10))
      ent = Entry(row, width=25)
      ent.config(font=("Arial", 10))
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

def cb(event):
  print "variable is", self.var.get()   

if __name__ == '__main__':

   textFontSize = 10
   titleFontSize = 18

   root = Tk()

   Label(root, text = 'Start experiment', font=("Arial",16)).pack()

   ents = makeform(root, fields)

   useTracker = IntVar()

   row = Frame(root)
   labl = Label(row, width = 15, text='Eye tracker', anchor='w')
   labl.config(font=("Arial",10))
   
      # ent.var = useTracker
   row.pack(side=TOP, fill=X, padx=5, pady=5)
   # cb.pack(side=RIGHT, padx=5)
   labl.pack(side=LEFT)

   Radiobutton(row, width=25, variable=useTracker, value=1, text='On',indicatoron=0, font=("Arial",8)).pack(side=RIGHT)
   Radiobutton(row, width=25, variable=useTracker, value=0, text='Off',indicatoron=0, font=("Arial",8)).pack(side=RIGHT)


   inScanner = IntVar()

   row2 = Frame(root)
   labl = Label(row2, width = 15, text='In scanner?', anchor='w')
   labl.config(font=("Arial",10))
   
      # ent.var = useTracker
   row2.pack(side=TOP, fill=X, padx=5, pady=5)
   # cb.pack(side=RIGHT, padx=5)
   labl.pack(side=LEFT)

   Radiobutton(row2, width=25, variable=inScanner, value=1, text='Yes',indicatoron=0, font=("Arial",8)).pack(side=RIGHT)
   Radiobutton(row2, width=25, variable=inScanner, value=0, text='No',indicatoron=0, font=("Arial",8)).pack(side=RIGHT)

   # ents['Tracker'] = ent

   # Eye tracker on by default
   # ent.select()
   # ents['Tracker'].select()

   row = Frame(root)
   expTask = IntVar()
   lbl = Label(row, width = 15, text = 'Task', font=("Arial",10), anchor='w')
   
   row.pack(side=TOP, fill=X, padx=5, pady=5)
   lbl.pack(side=LEFT)

   Radiobutton(row, width=25, text="Color", variable=expTask,value=1,indicatoron=0, font=("Arial",8)).pack(side=RIGHT,anchor=W)
   Radiobutton(row, width=25, text="Orientation", variable=expTask,value=2,indicatoron=0, font=("Arial",8)).pack(side=RIGHT,anchor=W)

   # ents['Timestamp'].insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

   # root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   # b1 = Button(root, text='Run staircase',
   #        command=(lambda e=ents: run_first_phase(root,e)))
   # b1.pack(side=LEFT, padx=5, pady=5)
   b1 = Button(root, text='Run experiment',
          command=(lambda e=ents: run_first_phase(root,e, inScanner,useTracker,expTask)), font=("Arial", 10))
   b1.pack(side=LEFT, padx=5, pady=5) 
   root.mainloop()