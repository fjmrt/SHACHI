import tkinter as tk
import FluidicsSystem
import os

class FluidicsControlGUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=630, height=600,
                         borderwidth=1, relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_canvas()
        self.getdest_widgets()
        self.create_control_widgets()
        self.create_accessory_widgets()

    def create_canvas(self):
        self.canvas = tk.Canvas(self,width=630, height=600)#,bg='white')
        self.canvas.create_rectangle(10,12,200,300)
        ms1 = tk.Label(self,text='param file location',anchor='w', font=("Helvetica",12))
        ms1.place(x=10,y=6,height=18,width=140)

        self.canvas.create_rectangle(210,12,400,300)
        ms2 = tk.Label(self,text='stage control',anchor='w', font=("Helvetica",12))
        ms2.place(x=210,y=6,height=18,width=100)

        self.canvas.create_rectangle(410,12,600,300)
        ms3 = tk.Label(self,text='pump control',anchor='w', font=("Helvetica",12))
        ms3.place(x=410,y=6,height=18,width=100)

        self.canvas.create_rectangle(10,320,600,500)
        ms4 = tk.Label(self,text='Seq Hyb protocol',anchor='w', font=("Helvetica",12))
        ms4.place(x=10,y=310,height=18,width=150)

        self.canvas.create_rectangle(10,580,600,520)
        ms5 = tk.Label(self,text='Imaging time calculator',anchor='w', font=("Helvetica",12))
        ms5.place(x=10,y=510,height=18,width=200)
        # -- made this independent window 20220329 Taihei Fujimori
        # self.canvas.create_rectangle(10,520,600,580)
        # ms4 = tk.Label(self,text='Tiff to Dax Converter',anchor='w', font=("Helvetica",12))
        # ms4.place(x=10,y=510,height=18,width=150)

        self.canvas.pack()

    def getdest_widgets(self):
        # text box to enter the param file location folder
        ms1 = tk.Label(self,text='folder',anchor='w', font=("Helvetica",12))
        ms1.place(x=12,y=30,height=20,width=60)
        self.text_box_dest = tk.Entry(self)
        self.text_box_dest.insert(0, "C:/SHACHI/")
        self.text_box_dest.place(x=12,y=50,height=20,width=180)
        ms2 = tk.Label(self,text='parameter file',anchor='w', font=("Helvetica",12))
        ms2.place(x=12,y=70,height=30,width=150)
        self.text_box_param = tk.Entry(self)
        self.text_box_param.insert(0, "params_test.xml")
        self.text_box_param.place(x=12,y=95,height=20,width=180)

        # execute
        getdest_btn = tk.Button(self, font=("Helvetica",12))
        getdest_btn['text'] = 'load params'
        getdest_btn['command'] = self.load_params_activate_system
        getdest_btn.place(x=12,y=120,height=30,width = 100)

        # message
        self.message = tk.Message(self, font=("Helvetica",12))
        self.message.place(x=12,y=160,width=150)
        self.message['text'] = 'not connected to the system yet.'

    def load_params_activate_system(self):
        self.fs = []
        self.dest = os.path.join(self.text_box_dest.get(),'')
        root_f, ext_f = os.path.splitext(self.text_box_param.get())
        self.fparam = root_f+'.xml'
        fpath = self.dest + self.fparam
        if os.path.isfile(fpath):  
            self.message['text'] = 'waking up the system...'
            self.update()
            self.fs = FluidicsSystem.FluidicsSystem(fpath,self.dest)
            self.operation_time = self.fs.SeqHybProtocolOperationTime()
            self.SeqHyb_widgets()
            self.message['text'] = 'connected to the system. ready to send commands.'
        else:  
            self.message['text'] = 'parameter file not exist.  cannot connect to the system.'

    def create_control_widgets(self):
        # -- needle Up -- #
        NeedleUp_btn = tk.Button(self,font=("Helvetica",12))
        NeedleUp_btn['text'] = 'needle Up'
        NeedleUp_btn['command'] = self.needleup
        NeedleUp_btn.place(x=430, y = 30, height=50, width = 150)

        # -- needle Down -- #
        NeedleDown_btn = tk.Button(self,font=("Helvetica",12))
        NeedleDown_btn['text'] = 'needle Down'
        NeedleDown_btn['command'] = self.needledown
        NeedleDown_btn.place(x=430, y = 90, height=50, width = 150)

        # -- start and stop flow -- #
        ms1 = tk.Label(self,text='flow rate [rpm]',anchor='w', font=("Helvetica",10))
        ms1.place(x=412,y=150,height=20,width=100)
        self.text_box_flowrate = tk.Entry(self, font=("Helvetica",12))
        self.text_box_flowrate.place(x=412,y=170, height = 20,width=80)
        ms2 = tk.Label(self,text='flow time [sec]',anchor='w', font=("Helvetica",10))
        ms2.place(x=508,y=150,height=20,width=87)
        self.text_box_flowtime = tk.Entry(self, font=("Helvetica",12))
        self.text_box_flowtime.place(x=508,y=170, height = 20,width=80)
        startflow_btn = tk.Button(self,font=("Helvetica",12))
        startflow_btn['text'] = 'start flow'
        startflow_btn['command'] = self.startflow
        startflow_btn.place(x=430,y=200, height=40, width = 150)
        startflow_btn = tk.Button(self,font=("Helvetica",12))
        startflow_btn['text'] = 'stop flow'
        startflow_btn['command'] = self.stopflow
        startflow_btn.place(x=430,y=250, height=40, width = 150)

        # -- move stage forward -- #
        StgFwd_btn = tk.Button(self)
        StgFwd_btn['text'] = 'move Stage forward'
        StgFwd_btn['command'] = self.movestageforward
        StgFwd_btn.place(x=230, y = 30, height=30, width = 150)

        # -- move to wash buffer -- #
        MoveToWash_btn = tk.Button(self)
        MoveToWash_btn['text'] = 'move to Wash buffer'
        MoveToWash_btn['command'] = self.movetowash
        MoveToWash_btn.place(x=230, y = 73, height=30, width = 150)

        # -- move to bleach buffer -- #
        MoveToBleach_btn = tk.Button(self)
        MoveToBleach_btn['text'] = 'move to Bleach buffer'
        MoveToBleach_btn['command'] = self.movetobleach
        MoveToBleach_btn.place(x=230, y = 116, height=30, width = 150)

        # -- move to imaging buffer -- #
        MoveToImagB_btn = tk.Button(self)
        MoveToImagB_btn['text'] = 'move to Imaging buffer'
        MoveToImagB_btn['command'] = self.movetoimaging
        MoveToImagB_btn.place(x=230, y = 159, height=30, width = 150)

        # -- move to stripping buffer -- #
        MoveToStrpB_btn = tk.Button(self)
        MoveToStrpB_btn['text'] = 'move to Stripping buffer'
        MoveToStrpB_btn['command'] = self.movetostripping
        MoveToStrpB_btn.place(x=230, y = 202, height=30, width = 150)

        # -- move to home position -- #
        MoveToHome_btn = tk.Button(self)
        MoveToHome_btn['text'] = 'move to Home position'
        MoveToHome_btn['command'] = self.gohome
        MoveToHome_btn.place(x=230, y = 245, height=30, width = 150)

    def create_accessory_widgets(self):
        # -- start and stop flow -- #
        ms1 = tk.Label(self,text='Start time',anchor='w', font=("Helvetica",12))
        ms1.place(x=50,y=530,height=20,width=80)
        ms1 = tk.Label(self,text='H',anchor='w', font=("Helvetica",10))
        ms1.place(x=15,y=550,height=20,width=20)
        self.text_box_SH = tk.Entry(self, font=("Helvetica",12))
        self.text_box_SH.place(x=35,y=550, height = 20,width=25)
        ms2 = tk.Label(self,text='M',anchor='w', font=("Helvetica",10))
        ms2.place(x=60,y=550,height=20,width=20)
        self.text_box_SM = tk.Entry(self, font=("Helvetica",12))
        self.text_box_SM.place(x=80,y=550, height = 20,width=25)
        ms3 = tk.Label(self,text='S',anchor='w', font=("Helvetica",10))
        ms3.place(x=105,y=550,height=20,width=20)
        self.text_box_SS = tk.Entry(self, font=("Helvetica",12))
        self.text_box_SS.place(x=125,y=550, height = 20,width=55)

        ms1 = tk.Label(self,text='End time',anchor='w', font=("Helvetica",12))
        ms1.place(x=240,y=530,height=20,width=80)
        ms1 = tk.Label(self,text='H',anchor='w', font=("Helvetica",10))
        ms1.place(x=205,y=550,height=20,width=20)
        self.text_box_EH = tk.Entry(self, font=("Helvetica",12))
        self.text_box_EH.place(x=225,y=550, height = 20,width=25)
        ms2 = tk.Label(self,text='M',anchor='w', font=("Helvetica",10))
        ms2.place(x=255,y=550,height=20,width=20)
        self.text_box_EM = tk.Entry(self, font=("Helvetica",12))
        self.text_box_EM.place(x=270,y=550, height = 20,width=25)
        ms3 = tk.Label(self,text='S',anchor='w', font=("Helvetica",10))
        ms3.place(x=295,y=550,height=20,width=20)
        self.text_box_ES = tk.Entry(self, font=("Helvetica",12))
        self.text_box_ES.place(x=315,y=550, height = 20,width=55)
        CalcImTime_btn = tk.Button(self,font=("Helvetica",12))
        CalcImTime_btn['text'] = 'calculate\nimaging time'
        CalcImTime_btn['command'] = self.CalculateImagingTime
        CalcImTime_btn.place(x=380,y=530, height=40, width = 120)
        # startflow_btn = tk.Button(self,font=("Helvetica",12))
        # startflow_btn['text'] = 'stop flow'
        # startflow_btn['command'] = self.stopflow
        # startflow_btn.place(x=430,y=250, height=40, width = 150)

    def SeqHyb_widgets(self):
        ms1 = tk.Label(self,text='Protocol name: '+self.fs.protocol_name,anchor='w', font=("Helvetica",10))
        ms1.place(x=12,y=335,height=18,width=450)
        ms1 = tk.Label(self,text='Number of hybridization: '+str(int(self.fs.hybnum)),anchor='w', font=("Helvetica",10))
        ms1.place(x=12,y=355,height=18,width=450)
        ms2 = tk.Label(self,text='Duration of imaging aquisition [sec]: '+str(self.fs.imagingtime),anchor='w', font=("Helvetica",10))
        ms2.place(x=12,y=375,height=18,width=450)

        im_time = self.fs.imagingtime+self.operation_time
        im_min,im_sec = divmod(im_time,60)
        ms3 = tk.Label(self,text='1. Set the time interval on the microscope: '+str(round(im_min))+'min '+str(round(im_sec,1))+'sec',anchor='w', font=("Helvetica",12))
        ms3.place(x=12,y=400,height=18,width=450)
        ms4 = tk.Label(self,text='2. Set the number of loop on the microscope: '+str(int(self.fs.hybnum)),anchor='w', font=("Helvetica",12))
        ms4.place(x=12,y=420,height=18,width=450)
        ms5 = tk.Label(self,text='3. Click [run Seq Hyb] button',anchor='w', font=("Helvetica",12))
        ms5.place(x=12,y=440,height=18,width=450)
        ms6 = tk.Label(self,text='4. Start imaging when the popup window shows [Ready to start imaging]',anchor='w', font=("Helvetica",12))
        ms6.place(x=12,y=460,height=18,width=500)
        ms7 = tk.Label(self,text='5. Click [Resume fluidics] on the popup window',anchor='w', font=("Helvetica",12))
        ms7.place(x=12,y=480,height=18,width=500)
        runSeqHyb_btn = tk.Button(self, font=("Helvetica",12))
        runSeqHyb_btn['text'] = 'run Seq Hyb'
        runSeqHyb_btn['command'] = self.runSeqHyb
        runSeqHyb_btn.place(x=470, y = 350, height=80, width = 100)
       
    def needleup(self):
        self.fs.devcnc.needleUp()
    def needledown(self):
        self.fs.devcnc.needleDown()
    def movestageforward(self):
        self.fs.stageForward()
    def movetowash(self):
        self.fs.devcnc.moveXY(self.fs.WASHX,self.fs.WASHY)
    def movetobleach(self):
        self.fs.devcnc.moveXY(self.fs.BLEACHX,self.fs.BLEACHY)
    def movetoimaging(self):
        self.fs.devcnc.moveXY(self.fs.IMAGINGX,self.fs.IMAGINGY)
    def movetostripping(self):
        self.fs.devcnc.moveXY(self.fs.STRIPPINGX,self.fs.STRIPPINGY)
    def gohome(self):
        self.fs.goHome()
    def CalculateImagingTime(self):
            StartTime = float(self.text_box_SH.get())*3600 + float(self.text_box_SM.get())*60 + float(self.text_box_SS.get())
            EndTime   = float(self.text_box_EH.get())*3600 + float(self.text_box_EM.get())*60 + float(self.text_box_ES.get())
            ms1 = tk.Label(self,text=str(round(EndTime - StartTime,3)),anchor='w', font=("Helvetica",12))
            ms1.place(x=500,y=540,height=20,width=100)
    def startflow(self):
        self.fs.devcnc.needleDown()
        self.fs.devcnc.wait(0.1)
        self.fs.ConstantFlow(float(self.text_box_flowrate.get()),float(self.text_box_flowtime.get()))
    def stopflow(self):
        self.fs.devpump.stopFlow()
    def runSeqHyb(self):
        self.fs.SeqHybProtocolRun()

root = tk.Tk()
root.title('SHACHI GUI')
app = FluidicsControlGUI(root=root)
app.mainloop()