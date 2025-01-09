import time

def Protocol(devcnc,devpump,newx,newy,waitingtime,FLOWTIME,FLOWSPEED):
	devcnc.moveXY(newx,newy)
	devcnc.needleDown()
	devcnc.wait(0.5) # -- command below here are not sent until waiting time ends
	print('start flow')
	devpump.startFlow(FLOWSPEED)
	time.sleep(FLOWTIME)
	print('stop flow')
	devpump.stopFlow()
	time.sleep(waitingtime)
	devcnc.needleUp()