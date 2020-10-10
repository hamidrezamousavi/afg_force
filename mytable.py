import tkinter as tk

class My_Table():
    choose_data = []
    
    class My_Text(tk.Text):
        def event_handeler(self,event):
            temp =float( self.get(1.0, tk.END).strip())
            if not self.cget('bg')=='LightBlue':
                My_Table.choose_data.append(temp)
                self.configure(bg='LightBlue',fg='yellow')
            else:
                My_Table.choose_data.remove(temp)
                self.configure(bg='White',fg='Black')

           
    def __init__(self,root,list):
        self.root = root
        self.list = list
        
        
        canvas = tk.Canvas( root,borderwidth=0, background="#ffffff")          #place canvas on self
        viewPort = tk.Frame(canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview) #place a scrollbar on self 
        canvas.configure(yscrollcommand=vsb.set)                          #attach scrollbar action to scroll of canva
        vsb.grid(column=4,row=0,rowspan=10)
        canvas.grid(column=0,row=0,rowspan=10)
        canvas_window = canvas.create_window((4,2), window=viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")
        def onFrameConfigure( event):                                              
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.
        def onCanvasConfigure(event):
            '''Reset the canvas window to encompass inner frame when required'''
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width = canvas_width)
        viewPort.bind("<Configure>", onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        canvas.bind("<Configure>", onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes
        onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resiz
           
        t = []
        for i in range(len(self.list)):
            t.append( My_Table.My_Text(viewPort,height=1,width=10))
            t[i].insert(tk.END,list[i])
            t[i].grid(column=0,row=0+i)   
            t[i].grid(padx=10)
           
            t[i].bind('<Double-Button-1>',t[i].event_handeler)


