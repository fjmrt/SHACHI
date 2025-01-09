import tkinter as tk
import TiffToDax_Leica
import os

class Tiff2Dax_GUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=630, height=150,
                         borderwidth=1, relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.TifftoDax_widgets()

    def TifftoDax_widgets(self):
        self.canvas = tk.Canvas(self, width=630, height=150)
        self.canvas.create_rectangle(10,20,600,140)
        ms4 = tk.Label(self,text='Tiff to Dax Converter',anchor='w', font=("Helvetica",12))
        ms4.place(x=10,y=10,height=18,width=150)
        self.canvas.pack()

        ms1 = tk.Label(self,text='Source folder',anchor='w', font=("Helvetica",10))
        ms1.place(x=12,y=80,height=20,width=90)
        self.out_src = tk.Entry(self)
        self.out_src.place(x=100,y=80,height=20,width=350)
        ms2 = tk.Label(self,text='Dest. folder',anchor='w', font=("Helvetica",10))
        ms2.place(x=12,y=105,height=20,width=90)
        self.out_dest = tk.Entry(self)
        self.out_dest.place(x=100,y=105,height=20,width=350)
        self.bOverwrite = tk.IntVar(0)
        c1 = tk.Checkbutton(self, text='Overwrite dax?',variable=self.bOverwrite, onvalue=1, offvalue=0, font=("Helvetica",10))
        c1.place(x=480,y=80,height=20,width=110)

        ms1 = tk.Label(self,text='# of hyb round',anchor='w', font=("Helvetica",10))
        ms1.place(x=12,y=30,height=20,width=90)
        self.hybnum = tk.Entry(self)
        self.hybnum.place(x=100,y=30,height=20,width=50)
        ms1 = tk.Label(self,text='# of FOV',anchor='w', font=("Helvetica",10))
        ms1.place(x=12,y=55,height=20,width=90)
        self.FOVnum = tk.Entry(self)
        self.FOVnum.place(x=100,y=55,height=20,width=50)


        # execute
        export_btn = tk.Button(self, font=("Helvetica",10))
        export_btn['text'] = 'convert'
        export_btn['command'] = self.TifftoDax_convert
        export_btn.place(x=480,y=105,height=20,width = 100)

    def TifftoDax_convert(self):
        print('overwrite: '+str(self.bOverwrite.get()))
        srcDIR  = os.path.join(self.out_src.get(),'')
        destDIR = os.path.join(self.out_dest.get(),'')
        tiffdax = TiffToDax_Leica.TiffToDax(sourceDIR = srcDIR, destDIR = destDIR, 
            hybnum = int(self.hybnum.get()), FOVnum = int(self.FOVnum.get()), bOverwrite = self.bOverwrite.get())
        tiffdax.export()
       

root = tk.Tk()
root.title('Tiff2Dax Converter')
app = Tiff2Dax_GUI(root=root)
app.mainloop()