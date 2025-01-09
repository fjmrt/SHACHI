import sys
import os
import time
import math
from datetime import datetime
import parameters as params_loader
import grblCNC
import gilson_mp3
import tkinter as tk

class FluidicsSystem():
		def __init__(self,
				parameterXML = False,logdest = './', parameterBasic = './params_basic.xml'):

			# -- load experiment-specific parameters
			self.paramsXML = parameterXML
			self.logdest = logdest
			self.prms = params_loader.parameters(parameterXML)
			self.imagingtime = self.prms.get("imagingtime") 
			self.hybnum = self.prms.get("hybnum")
			self.FOVnum = self.prms.get("FOVnum")
			self.protocol_name = self.prms.get("protocol_name")

			# -- load basic parameters such as coordinate, flow rate
			self.prms_b = params_loader.parameters(parameterBasic)
			self.coordinatefile = self.prms_b.get("coordinatefile")
			self.WASHX = self.prms_b.get("WASHX")
			self.BLEACHX = self.prms_b.get("BLEACHX")
			self.IMAGINGX = self.prms_b.get("IMAGINGX")
			self.STRIPPINGX = self.prms_b.get("STRIPPINGX")
			self.WASHY = self.prms_b.get("WASHY")
			self.BLEACHY = self.prms_b.get("BLEACHY")
			self.IMAGINGY = self.prms_b.get("IMAGINGY")
			self.STRIPPINGY = self.prms_b.get("STRIPPINGY")
			self.FLOWSPEED = self.prms_b.get("FLOWSPEED") 
			self.FLOWTIME = self.prms_b.get("FLOWTIME")
			# -- activate CNC and pump
			if self.prms.get("valve_name") == 'Genmitsu3018-PROVer V2':
				import grblCNCv2 as grblCNC
			self.devcnc  = grblCNC.G_CNC(self.prms_b)
			self.devpump = gilson_mp3.APump(self.prms_b)

			# -- protocol parameters
			if self.protocol_name == 'ORCA':
				parameterProtocol = './params_protocol_ORCA.xml'
			elif self.protocol_name == 'multiplexed RNA FISH':
				parameterProtocol = './params_protocol_RNA.xml'
			else:
				parameterProtocol = './params_protocol_test.xml'

			self.prms_p = params_loader.parameters(parameterProtocol)
			self.hybtime = self.prms_p.get("hybtime") 
			self.waitingtime_wash = self.prms_p.get("waitingtime_wash") 
			self.waitingtime_bleach = self.prms_p.get("waitingtime_bleach") 
			self.waitingtime_imaging = self.prms_p.get("waitingtime_imaging") 
			self.waitingtime_stripping = self.prms_p.get("waitingtime_stripping") 
			self.next_pressed = tk.BooleanVar(value=False)

		def SeqHybProtocolRun(self):
			fcoords = open(self.coordinatefile,'r')
			print('MESSAGE -- Opening coordinate file')
			# create log file
			logfile = self.logdest+'log_'+str(datetime.fromtimestamp(time.time())).split('.')[0].replace(':','-').replace(' ','-')+'.txt' # ex) log_2021-03-06-12-04-38.txt
			f_log = open(logfile,'w')
			f_log.write('SeqHybProtocolRun. ParameterFile='+self.paramsXML+'\n')
			f_log.close()
			print('MESSAGE -- Creating log file')
			msg = tk.Toplevel()
			msg.title('Seq Hyb protocol')
			msg.geometry('300x120')
			label = tk.Message(msg, font=("Helvetica",12))
			remainingtime = self.hybtime+self.FLOWTIME+self.waitingtime_wash+self.FLOWTIME*2+self.waitingtime_bleach+self.FLOWTIME+self.waitingtime_imaging+self.FLOWTIME+60.0
			remainingtime = math.floor(remainingtime/60)
			label['text'] = '1. 1st hyb(<<<)\n2. wash\n3. incubation\n ~'+str(remainingtime)+' min left.'
			label.place(x=0,y=0,height=100,width=300)
			msg.update()
			maxdist = self.calcDist('X0','Y0',self.IMAGINGX,self.IMAGINGY)
			currentx = self.IMAGINGX
			currenty = self.IMAGINGY

			cntr = 1
			for line in fcoords:
				if cntr <= self.hybnum:
					cmd=line.strip().split('\t')
					newx = cmd[0]
					newy = cmd[1]
					logmsg = 'hyb'+str(cntr)+'_'+newx+'_'+newy+'_start--'+str(datetime.fromtimestamp(time.time()))+'\n'
					f_log = open(logfile,'a')
					f_log.write(logmsg)
					f_log.close()
					print(logmsg)
					# ---- sequential flow protocol ---- #
					# format: self.Protocol(CNC_class,Pump_class,X_position,Y_position,WaitingtimeAfterFlowStops,HowLongYouWantToFlow)
					# Protocol method executes 
					#    1. up the needle
					#    2. move to the position as you set in X_position and Y_position
					#    3. down the needle, flow the reagent as you set in FLOWSPEED and FLOWTIME
					#    4. stop the flow, hold for a while as you set in WaitingtimeAfterFlowStops
					# ------------------------------------
					# -- stripping for multiplexed RNA FISH
					if self.waitingtime_stripping != 0 and cntr > 1:
						self.Protocol(self.STRIPPINGX,self.STRIPPINGY,self.waitingtime_stripping,self.FLOWTIME)
						self.Protocol(self.BLEACHX,self.BLEACHY,self.waitingtime_bleach,self.FLOWTIME)
						currentx = self.BLEACHX
						currenty = self.BLEACHY
					# -- 96 well
					newdist = 'F'+str(round(2000*self.calcDist(currentx,currenty,newx,newy)/maxdist,2))
					self.Protocol(newx,newy,self.hybtime,self.FLOWTIME,newdist)
					# -- wash buffer
					remainingtime = self.waitingtime_wash+self.FLOWTIME*2+self.waitingtime_bleach+self.FLOWTIME+self.waitingtime_imaging+self.FLOWTIME+60.0
					remainingtime = math.floor(remainingtime/60)
					if cntr == 1:
						label['text'] = '1. 1st hyb(done)\n2. wash(<<<)\n3. incubation\n ~'+str(remainingtime)+' min left.'
						msg.update()
					newdist = 'F'+str(round(2000*self.calcDist(newx,newy,self.WASHX,self.WASHY)/maxdist,2))
					self.Protocol(self.WASHX,self.WASHY,self.waitingtime_wash,self.FLOWTIME*2,newdist)
					# -- bleach buffer
					self.Protocol(self.BLEACHX,self.BLEACHY,self.waitingtime_bleach,self.FLOWTIME)
					# -- imaging buffer + hold untile the image aquisition is done
					remainingtime = self.waitingtime_imaging+self.FLOWTIME+60.0
					remainingtime = math.floor(remainingtime/60)
					if cntr == 1:
						label['text'] = '1. 1st hyb(done)\n2. wash(done)\n3. incubation(<<<)\n ~'+str(remainingtime)+' min left.'
						msg.update()
					self.Protocol(self.IMAGINGX,self.IMAGINGY,self.waitingtime_imaging,self.FLOWTIME)
					currentx = self.IMAGINGX
					currenty = self.IMAGINGY
					# ------------------------------------
					# -- write a log
					logmsg = 'hyb'+str(cntr)+'_'+newx+'_'+newy+'_end--'+str(datetime.fromtimestamp(time.time()))+'\n'
					f_log = open(logfile,'a')
					f_log.write(logmsg)
					f_log.close()
					print(logmsg)
					# -- hold for a while until image aquisition is done
					remainingtime = 60.0
					remainingtime = math.floor(remainingtime/60)
					if cntr == 1:
						label['text'] = '1. 1st hyb(done)\n2. wash(done)\n3. incubation(done)\n '+str(remainingtime)+' min left.'
						msg.update()
					self.Hold(60)
					if cntr == 1:
						# label['text'] = 'Start imaging!'
						# msg.update()
						# ---- under construction ---- #
						label['text'] = 'Ready to start imaging (fluidics is paused)'
						label.place(x=0,y=0,height=80,width=300)
						StartImaging_btn = tk.Button(msg)
						StartImaging_btn['text'] = 'Resume fluidics'
						StartImaging_btn['command'] = self.go_next
						StartImaging_btn.place(x=50,y=85,height=25,width=200)
						msg.update()
						msg.wait_variable(self.next_pressed)
						print("clicked")
						label['text'] = 'Fluidics resumed'
						label.place(x=0,y=0,height=80,width=300)
						msg.update()
					self.Hold(self.imagingtime)
					self.Hold(60)
					# ------------------------------------
					cntr = cntr + 1
			self.Protocol(self.BLEACHX,self.BLEACHY,self.waitingtime_bleach,self.FLOWTIME)
			print('MESSAGE -- Seq Hyb Protocol is done.')
			fcoords.close()

		def SeqHybProtocolOperationTime(self):
			if self.prms.get("valve_name") == 'Genmitsu3018-PROVer V2':
				if self.waitingtime_stripping == 0:
					operatime_time = 31.778 + self.hybtime+self.FLOWTIME+self.waitingtime_wash+self.FLOWTIME*2+self.waitingtime_bleach+self.FLOWTIME+self.waitingtime_imaging+self.FLOWTIME+120 # 31.778 traveling time
				if self.waitingtime_stripping != 0:
					operatime_time = 46.856 + self.hybtime+self.FLOWTIME+self.waitingtime_wash+self.FLOWTIME*2+self.waitingtime_bleach+self.FLOWTIME+self.waitingtime_imaging+self.FLOWTIME+self.waitingtime_stripping+self.FLOWTIME+self.waitingtime_bleach+self.FLOWTIME+120 # 31.778 traveling time
			return operatime_time

		def WashFlow(self,speed):
			self.devcnc.moveXY('X0','Y0')
			input('press <Enter> to start wash.')
			self.devcnc.needleDown()
			self.devcnc.wait(0.5) # -- command below here are not sent until waiting time ends
			print('start flow')
			self.devpump.startFlow(speed)
			input('press <Enter> to stop wash.')
			print('stop flow')
			self.devpump.stopFlow()
			self.devcnc.needleUp()

		def ConstantFlow(self,speed,waitingtime = 0):
			self.devpump.startFlow(speed)
			if waitingtime > 0:
				time.sleep(waitingtime)
				self.devpump.stopFlow()

		def stageForward(self):
			if self.devcnc.zpos != 'Z0':
				self.devcnc.needleUp()
			self.devcnc.moveXY(self.devcnc.xpos,'Y150')

		def goHome(self):
			if self.devcnc.zpos != 'Z0':
				self.devcnc.needleUp()
			self.devcnc.moveXY('X0','Y0')

		def Protocol(self,newx,newy,waitingtime,FLOWTIME,feedspeed = 'default'):
			self.devcnc.needleUp()
			self.devcnc.moveXY(newx,newy,feedspeed)
			self.devcnc.needleDown()
			self.devcnc.wait(1.0) # -- command below here are not sent until waiting time ends
			print('start flow')
			self.devpump.startFlow(self.FLOWSPEED)
			time.sleep(FLOWTIME)
			print('stop flow')
			self.devpump.stopFlow()
			time.sleep(waitingtime)

		def Hold(self,waitingtime):
			self.devcnc.wait(waitingtime) 

		def go_next(self):
			current_value = self.next_pressed.get()
			self.next_pressed.set(not current_value)
			print(f'current value: {self.next_pressed.get()}')

		def calcDist(self,x1,y1,x2,y2):
			dist = math.sqrt((float(x1.split('X')[1]) - float(x2.split('X')[1]))**2 + (float(y1.split('Y')[1]) - float(y2.split('Y')[1]))**2)
			return dist


# devcnc.serial.close()
# devpump.serial.close()


