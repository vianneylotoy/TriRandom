#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from interval import Intervalle
from task import Tasks
from computer import Computer
from random import randint, uniform, randrange, seed
import matplotlib.pyplot as plt


class Execution:
	
	#Attribute of instances of the class
	def __init__(self):
		self.RejectedTasks = []
		self.PlacedTasks = []
		self.L_Cmax = []
		self.PlacedSlot = []
		self.L_intervalle = []
		self.LT = []
		self.LT_sorted = []
		self.freeMachine = -1
		self.lastStart = -1
		self.RemainderEnergy = 0
		self.doc = open('output.txt','w')
		self.computer = Computer()
		self.interv = Intervalle()
		self.tache = Tasks()
		self.init_busyCompute()
		self.create_Interval()
		
		
	
	#Automatic random generation of task list
	def create_Task(self,startPi,endPi,startφi,endφi):
		seed(startPi)
		#LT = [[pi,φi,si]:Ti]
		for i in range(0,1000):
			self.tache.pi = round(uniform(startPi,endPi),1)
			self.tache.φi = round(uniform(startφi,endφi),1)
			self.LT.insert(i,[self.tache.pi,self.tache.φi,self.tache.si])
	
	
	#Sort randomly item list
	def sort_random(self):
		self.LT_sorted = sorted(self.LT, key=lambda k: randrange(len(self.LT)))
		
	#Display of the Generated Task List
	def display_task(self):
		for i,ti in enumerate(self.LT):
			self.tache.pi, self.tache.φi, self.tache.si = ti
			print("Generated Task: T[%r] = [%r,%r,%r]" % (i, self.tache.pi, self.tache.φi, self.tache.si))
			self.doc.write("Generated Task: T["+str(i)+"] = p"+str(i)+"-> "+str(self.tache.pi)+", φ"+str(i)+"-> "+str(self.tache.φi)+", s"+str(i)+"-> "+str(self.tache.si)+ '\n')
	
	#Display of the list of tasks sorted randomly
	def display_sortedTask(self):
		self.doc.write("___________________________________________________ Random sorting Task ______________________________________________________"+'\n')
		for i,ti in enumerate(self.LT_sorted):
			self.tache.pi, self.tache.φi, self.tache.si = ti
			print("Random sorting Task ->: T[%r] = [%r,%r,%r]" % (i,self.tache.pi, self.tache.φi, self.tache.si))	
			self.doc.write("Task random sorting->: T["+str(i)+"] = p"+str(i)+"-> "+str(self.tache.pi)+", φ"+str(i)+"-> "+str(self.tache.φi)+", s"+str(i)+"-> "+str(self.tache.si)+ '\n')
			
		
	#Creating the list of equal intervals
	def create_Interval(self):
		seed(3)
		for t in range(1, 20301):
			self.interv.st = self.interv.et 
			self.interv.et = t * 10
			self.interv.Φ = randint(3,20)
			self.L_intervalle.insert(t,[self.interv.Φ,self.interv.st,self.interv.et])
	
	
	def display_intervalle(self):
		self.doc.write("------------------------------------ Initial list of intervals ---------------------------------------"+'\n')
		for t,tval in enumerate(self.L_intervalle):
			self.interv.Φ, self.interv.st, self.interv.et = tval
			self.doc.write("t"+str(t)+" = "+str(self.interv.Φ)+","+str(self.interv.st)+","+str(self.interv.et)+ '\n')

		
	
	#Initializing of using time machine List
	def init_busyCompute(self):
		self.computer.Mbusy = [[[-1,-1]] * 1 for _ in range(0,500)]
	
	#Display of the using times of machines
	def display_Mbusy(self):
		self.doc.write("#############################################################################"+'\n')
		for m, count in enumerate(self.computer.Mbusy):
			if not [-1,-1] in self.computer.Mbusy[m]:
				#print("Machine[%r] used = %r" % (m,self.computer.Mbusy[m]))
				self.doc.write("Machine["+str(m)+"] used = "+ str(self.computer.Mbusy[m])+'\n')
				self.doc.write(" "+'\n')
		self.doc.write("#############################################################################"+'\n')
		
	
	#The next interval right item
	def nextRightboundedItem(self, subliste, index):
		st = 0  # start
		ed = 0  # end
		if index < len(subliste) and index+1 <= len(subliste)-1:
			st, ed = subliste[index+1]

		return ed
	
	#The next interval left item
	def nextLeftboundedItem(self, sub_list, index):
		st = 0   # start
		ed = 0   # end
		if index < len(sub_list) and index+1 <= len(sub_list)-1:
			st, ed = sub_list[index+1]
		
		return st
		
	
	
	#Check of free machine at a time t
	def CheckAvailability(self,start, end):
		j = 0
		k = 0
		m = -1
		sublist = []
		found = False
		
		while j < len(self.computer.Mbusy) and not found:
			k = 0
			trouve = True
			sublist = []
			sublist = self.computer.Mbusy[j]
			
			while k < len(sublist) and trouve:
				start_busy, end_busy = sublist[k]
				
				nextStart = self.nextLeftboundedItem(sublist,k)
				nextEnd = self.nextRightboundedItem(sublist,k)
				
				if start == end_busy and end == nextStart:
					m = -1
					trouve = False
					
				elif start >= start_busy and end <= end_busy:
					m = -1 
					trouve = False
					
				elif start == start_busy and end == end_busy:
					m = -1 
					trouve = False
				
				elif start >= start_busy and start < end_busy and end >= end_busy:
					m = -1
					trouve = False
				
				elif ((start < start_busy) and (end > (start_busy + self.computer.DelayOn)) and (end <= end_busy)):
					m = -1
					trouve = False
				
				elif start <= start_busy and end > (start_busy + self.computer.DelayOn) and end >= end_busy:
					m = -1
					trouve = False
				
				else:
					m = j
				
				k += 1
			
			if m != -1:
				found = True
			
			j += 1
								
		return m  

	
	#Filling of the using times of the used machine
	def FillupBusyComputer(self,startT,endT, machine):
		# check if PlacedSlot list is empty
		if not self.PlacedSlot:
			if [-1,-1] in self.computer.Mbusy[machine]:
				indexe =  self.computer.Mbusy[machine].index([-1,-1])
				self.computer.Mbusy[machine][indexe] = [startT, endT]
			else:
				self.computer.Mbusy[machine] += [[startT, endT]]
				
			self.PlacedSlot = [startT, endT]
				


	#The task fit slot
	def FitSlot(self, pi,varphi,si):
		t = 0 
		trouve = False
		
		
		while t < len(self.L_intervalle) and not trouve:
			s = t
			
			#self.doc.write("t iterator:"+str(t)+'\n')
			
			self.interv.Φ, self.interv.st, self.interv.et = self.L_intervalle[t]
			
			
			##print("pi ", pi)
			#self.doc.write("st_t: "+str(st_t)+'\n')
			#self.doc.write("et_t: "+str(et_t)+'\n')
			#self.doc.write("Φ(t): "+str(phi_t)+'\n')
			
			Φ_s, st_s, et_s = self.L_intervalle[s]
			
			#self.doc.write("pi: "+str(pi)+'\n')
			St_pi = round((self.interv.st + pi),1)
			#print("st+pi ", St_pi)
			
			#self.doc.write("st+pi: "+str(St_pi)+'\n')
			
			##print("consumption ", round((self.computer.PowerOn + varphi),1))
			
			#self.doc.write("consumption: "+str(round((self.computer.PowerOn + varphi),1))+'\n')
			
			while self.interv.Φ >= self.computer.PowerOn + varphi and St_pi > et_s and s < len(self.L_intervalle):
				s += 1
			
			
			if St_pi >= et_s and self.interv.Φ >= self.computer.PowerOn + varphi:
				start = self.interv.st
				end = St_pi
				self.freeMachine = self.CheckAvailability(start,end)
				self.doc.write("satisfied (st + pi): "+str(St_pi)+'\n')
				
				if self.freeMachine != -1:
					trouve = True
					self.FillupBusyComputer(start,end, self.freeMachine)
				
			
			t += 1
	
			
		return trouve
	
	#Creating placement of the task on the machine in free slot
	def CreateAvailability(self,pi,varphi,si, index):
		found = False
		
		found = self.FitSlot(pi,varphi,si)
		
		if found:
	
			self.PlacedTasks.append(index)
			self.PlacingTask(pi,varphi,si, self.freeMachine,index)
			##print("T[%r] = [%r,%r,%r] is placed on machine %r" % (index,pi,varphi,self.tache.si, self.freeMachine))
			self.doc.write("T["+str(index)+"]"+" = "+ str(pi)+","+str(varphi)+","+str(self.tache.si)+" is placed on machine "+str(self.freeMachine)+'\n')
			
		else:
	
			self.RejectedTasks.append(index)
			##print("T[%r] is rejected " % (index))
			self.doc.write("T["+str(index)+"]"+" = "+ str(pi)+","+str(varphi)+","+str(si)+" is rejected"+'\n')

	
	
	#Get interval list index
	def GetIndexSlot(self, val, varphi):
		t = 0
		index = -1
		found = False
		
		while t < len(self.L_intervalle) and not found:
			self.interv.Φ, self.interv.st, self.interv.et = self.L_intervalle[t]
			if self.interv.et >= val and self.interv.Φ >= self.computer.PowerOn + varphi:
				index = t
				found = True
			
			t += 1
				
		return index
	
	#Update interval amount of energy
	def UpdateEnergy(self, index1, index2, varphi):
		if (index1 != -1 or index2 != -1) or (index1 != -1 and index2 != -1):
			computerConsumption = Mconsumption = 0
			self.RemainderEnergy = 0
			self.interv.Φ, self.interv.st, self.interv.et = self.L_intervalle[index2]
			
			if index1 == index2:
				Mconsumption = round((self.computer.PowerOn + varphi),1)
				if self.interv.Φ > 0 and self.interv.Φ > Mconsumption:
					self.RemainderEnergy = self.interv.Φ - Mconsumption
					phi_t, st_t, et_t = self.L_intervalle[index1]
					self.L_intervalle[index1] = [round(self.RemainderEnergy,1), st_t, et_t]
					
					self.doc.write("The remainder energy is for equal indexes: "+str(round(self.RemainderEnergy,1))+'\n')
					#print("The remainder energy is for equal indexes: ", self.RemainderEnergy)
				
			else:
				t = index1
				
				while index2 >= t:
					computerConsumption += round((self.computer.PowerOn + varphi),1)
					
					#print("Computer consumption is ", computerConsumption)
					self.doc.write("The computer Consumption is: "+str(round(computerConsumption,1))+'\n')
					
					phi_T, st_T, et_T = self.L_intervalle[t]
					if phi_T > 0 and phi_T > computerConsumption:
						#print("phi_T for different indexes: ", phi_T)
						self.doc.write("phi_T for different indexes: "+str(round(phi_T,1))+'\n')
						
						consump = round(computerConsumption,1)
						self.RemainderEnergy = round(phi_T,1) - consump
						
						self.L_intervalle[t] = [round(self.RemainderEnergy,1), st_T, et_T]
						
						self.doc.write("The remainder energy is for different indexes: "+str(round(self.RemainderEnergy,1))+'\n')
						#print("The remainder energy is for different indexes: ", self.RemainderEnergy)
					
						
					t += 1
	
	#The remainder time of task placing
	def RemainderTime(self, phi, start_t, end_t, pi, index2, freeComputer):
		
		et_tp = round(end_t,1)     # et_t'
		

		self.interv.Φ, self.interv.st, self.interv.et = self.L_intervalle[index2]
		st_tp = self.interv.st    # st_t'
		
		#check remainder time and check split time is superior than start time
		if self.interv.et > et_tp and index2 != -1 and et_tp > self.interv.st:
			#print("index2 ", index2)
			#print("Split time: ", et_tp)
			
			self.doc.write("Split time: "+str(et_tp)+'\n')
			
			#print("end_t", et_tt)
			
			self.doc.write("end_t: "+str(self.interv.et)+'\n')
			
			self.L_intervalle[index2] = [round(self.RemainderEnergy,1), st_tp, et_tp]
			self.L_intervalle.insert(index2 + 1, [phi, et_tp, self.interv.et])
				
		
		#Modifying of end time of the used machine according what has been really used in the booked slot
		self.UpdateBusyTime(et_tp, freeComputer, index2)			
			
	
	
	#Placement of the task on the machine in free slot
	def PlacingTask(self, pi,varphi,si, freeComputer,index):
		#check list not empty
		if self.PlacedSlot:
			#print("PlacedSlot[0] ", self.PlacedSlot[0])
			#print("PlacedSlot[1] ", self.PlacedSlot[1]+ self.computer.DelayOn)
			
			index1 = self.GetIndexSlot(self.PlacedSlot[0],varphi)
			value = self.PlacedSlot[1] + self.computer.DelayOn
			index2 = self.GetIndexSlot(value,varphi)
			
			self.interv.Φ, self.interv.st, self.interv.et = self.L_intervalle[index2]
			phiSlot = self.interv.Φ
			
			self.UpdateEnergy(index1,index2,varphi)
			
			if (index1 != -1 or index2 != -1) or (index1 != -1 and index2 != -1):
				#Initializing of task start time
				self.tache.si = self.PlacedSlot[0] + self.computer.DelayOn
				starttime = round(self.tache.si,1)
				self.doc.write("Task start time: "+str(starttime)+'\n')
				
				#check if not out of range of task list
				if index >= len(self.LT_sorted):
					 self.LT_sorted[-1] = [round(self.tache.pi,1),round(self.tache.φi,1),starttime]
				else:
					self.LT_sorted[index] = [round(self.tache.pi,1),round(self.tache.φi,1),starttime]
					
				self.RemainderTime(phiSlot,self.PlacedSlot[0], value, pi, index2, freeComputer) 
							  
				
				#Completion time
				self.tache.Ci = starttime + pi
				self.lastStart = starttime
				self.L_Cmax.append(round(self.tache.Ci,1))
				
				#Turn off machine
				pi + self.computer.DelayOff
				phi_t, st_t, et_t = self.L_intervalle[index2]
				
				if phi_t >= self.computer.PowerOff:
					Remainder = phi_t - self.computer.PowerOff
					self.L_intervalle[index2] = [round(Remainder,1), st_t, et_t] 
			self.PlacedSlot.clear()
			
    #Modifying the end time of the using times of the used machine
	def UpdateBusyTime(self,endTime, free_computer, index2):
		
		sublist = []
		
		if index2 == -1:
			sublist = self.computer.Mbusy[free_computer]
			##print("Updated sub list ", sublist)
			sublist[-1] = [-1,-1]
			self.computer.Mbusy[free_computer] = sublist
		
		else:
			sublist = self.computer.Mbusy[free_computer]
			start_busy, end_busy = sublist[-1]
			#update the using end time of the current used machine
			sublist[-1] = [start_busy, endTime]
			self.computer.Mbusy[free_computer] = sublist
			self.doc.write("   "+'\n')	
			self.doc.write("Machine["+str(free_computer)+"] used updated "+str(sublist)+'\n')
			self.doc.write(" "+'\n')		

			
	
	#Graphic display
	def PrintGraphic(self):
		name = ['Rejected Tasks', 'Placed Tasks']
		# check if Rejectedtasks List is empty
		if not self.RejectedTasks:
			data = [0, len(self.PlacedTasks)]
			self.doc.write("Number of placed tasks: "+str(len(self.PlacedTasks))+'\n')
			self.doc.write("Number of rejected tasks: 0"+'\n')
		# check if PlacedTasks List is empty
		elif  not self.PlacedTasks:
			data = [len(self.RejectedTasks), 0]
			self.doc.write("Number of rejected tasks: "+str(len(self.RejectedTasks))+'\n')
			self.doc.write("Number of placed tasks: 0"+'\n')
		else:
			data = [len(self.RejectedTasks), len(self.PlacedTasks)]
			self.doc.write("Number of placed tasks: "+str(len(self.PlacedTasks))+'\n')
			self.doc.write("Number of rejected tasks: "+str(len(self.RejectedTasks))+'\n')
			
		explode=(0, 0.15)
		plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
		plt.axis('equal')
		plt.show()


    #Printing cmax result
	def getMakespan(self):
		if self.L_Cmax:
			Cmax = max(self.L_Cmax)
			print("Makespan is: ", Cmax)
			self.doc.write("---------------------------"+"|"+'\n')
			self.doc.write("Makespan is: "+str(Cmax)+"         |"+'\n')
			self.doc.write("---------------------------"+"|"+'\n')			
			
	#Updated slot		
	def getUpdatedInterval(self):
		self.doc.write("------------------------------------ Final list of intervals -----------------------------------------"+'\n')
		for t,tval in enumerate(self.L_intervalle):
			self.interv.Φ, self.interv.st, self.interv.et = tval
			self.doc.write("t"+str(t)+" = "+str(self.interv.Φ)+","+str(self.interv.st)+","+str(self.interv.et)+ '\n')
	
	
			
			
