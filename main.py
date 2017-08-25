#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from execution import Execution
from task import Tasks
import matplotlib.pyplot as plt
import sys




if len(sys.argv) != 5:
    print("Usage : main.py start_pi_value end_pi_value start_φi_value end_φi_value")
    sys.exit(4)

startPi = int(sys.argv[1])
endPi = int(sys.argv[2])
startφi = int(sys.argv[3])
endφi = int(sys.argv[4])

exe = Execution()

exe.create_Task(startPi,endPi,startφi,endφi)
exe.sort_random()
exe.doc.write("start value of task pi: "+str(startPi)+", end value of task pi: "+str(endPi)+'\n')
exe.doc.write("start value of task φi: "+str(startφi)+", end value of task φi: "+str(endφi)+'\n')
exe.doc.write("--------------------------------------------------------------------------------------------------"+'\n')
  
task = Tasks()

exe.display_task()
exe.display_sortedTask()
exe.display_intervalle()


for i,ival in enumerate(exe.LT_sorted):
	task.pi,task.φi,task.si = ival
	exe.doc.write("--------------------------------------------------------------------------------------------------"+'\n')
	exe.doc.write("Task "+str(i)+" = "+str(task.pi)+","+str(task.φi)+","+str(task.si)+ '\n')
	exe.CreateAvailability(task.pi,task.φi,task.si,i)


#check if RejectedTasks list is empty to get result
if not exe.RejectedTasks:
	exe.getMakespan()
	exe.display_Mbusy()
	exe.PrintGraphic()
	exe.getUpdatedInterval()
else:
	print("-----------------------------------------------------|")
	print("Result rejected because %r task(s) is(are) rejected! |" % (len(exe.RejectedTasks)))
	print("-----------------------------------------------------|")
	print("May be, you must give more intervals to solve it     |")
	print("-----------------------------------------------------|")
	exe.doc.write("------------------------------------------------"+"|"+ '\n')
	exe.doc.write("Result rejected because "+str(len(exe.RejectedTasks))+" task(s) is(are) rejected!"+" |"+'\n')
	exe.doc.write("------------------------------------------------"+"|"+ '\n')
	exe.PrintGraphic()



