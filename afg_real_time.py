import  matplotlib.pyplot as plt
from statistics import mean,stdev
import tkinter as tk
from threading import Thread
from mytable import My_Table
import tkinter.font as tkfont
import serial
from toexcel import write_to_excel

#data and unit are global variable that share read data between function
data = []
unit = ''
#this var set for chacking that reading is countinou our finished
reading_data = True




def read_real_time():
    
    global data, unit
    raw_data = []
    
    ser = serial.Serial('COM1', 9600, timeout=0.2)
    
    while reading_data:
        temp = []
        s = ser.read(1000)
        raw_data = s.decode('utf8','ignore').split()
        #convert data to float list   
        
        for item in raw_data:
            try:
                temp.append(float(item))
            except ValueError:
                unit = item if item in ['gf','kgf','N','ozf','lbf',] else unit
        try:
            mean = sum(temp)/len(temp)
        except ZeroDivisionError:
            mean = 0
        
        data.append(mean)
        
    ser.close()

   
def show_real_time(root):
    '''
    show read data online on screen
    '''
    global reading_data,data,unit
    
    
    #clear frame
    for child in root.winfo_children()[2:]:
        child.destroy()

    #deactive button for pereventing unkown action during reading data
    for child in root.winfo_children():
        child.config(state="disable")
        
    #make new thread for reading data
    t = Thread(target=read_real_time)
    t.start()
   # print(data[-1])
    force_font =tkfont.Font(family='Helvetica',
                         size=46,
                         weight='bold')
    force_label = tk.Label(root,font=force_font,fg='green')
    force_label.grid(column=30,row=3)
    unit_font =tkfont.Font(family='Helvetica',
                         size=26,
                         weight='bold')
    
    unit_label = tk.Label(root,font=unit_font,fg='green')
    unit_label.grid(column=40,row=3)
    
    def stop():
        '''
        define stop button action
        '''
        global reading_data
        reading_data = False #inform that data reading finished
        for child in root.winfo_children():
            child.config(state="normal")
        stop_button.destroy()
        
    stop_button = tk.Button(root,text='    پایان    ',command = stop)
    stop_button.grid(column=40,row=1,sticky='NE')
    
    #refresh label after 100 miliseconds
    
    def show():
        global data,unit
        if reading_data:
            try:
                unit_label.configure(text = unit)  
                force_label.configure(text=format(data[-1],'.2f'))
                root.after(100,show)
                
            except :
                root.after(1000,show)
            
    show() 
    
    


def draw_real_time(data,unit):
    '''
    plot read data
    '''

    plt.style.use('seaborn-whitegrid')
    fig=plt.figure()
    chart=fig.add_axes([0.1, 0.1, .9,0.9])
    chart.set_title('Scatter: $x$ versus $y$')
    chart.set_xlabel('$x$')
    chart.set_ylabel(unit)
    chart.yaxis.tick_left()
    chart.plot([i for i in range(len(data))], data, '-o',
    color='blue',
    markersize=2, 
    linewidth=1,
    markerfacecolor='white',
    markeredgecolor='gray',
    markeredgewidth=2,
    label='test')
    chart.axis('tight')
    plt.show()

def real_time_func(root):
    '''
    define what will do after press دادهای همزمان button
    '''
    global reading_data,data,unit
    reading_data = True
    data = []
    unit = ''



    show_real_time(root)
   
    def  show():  #check if data reading is compelet then show drawing and calcluse
        if reading_data:
            root.after(1000,show)
            
        else:
            
            
            dom_label = tk.Label(root,text='محدوده داده‌ها جهت محاسبه')
            dom_label.grid(column = 40,row=4,sticky='sE',columnspan=2)
            
            from_label = tk.Label(root,text='از نقطه')
            from_label.grid(column = 41,row=5,sticky='sE')
            
            from_point = tk.Text(root,height=1,width=6)
            from_point.grid(column = 40,row=5)
            
            to_label = tk.Label(root,text='تا نقطعه')
            to_label.grid(column = 31,row=5,sticky='sE')
            
            to_point = tk.Text(root,height=1,width=6)
            to_point.grid(column = 30,row=5)
            
            mean_label = tk.Label(root,text='میانگین')
            mean_label.grid(column = 41,row=7,sticky='sE')
            mean_number_label = tk.Label(root,text='number')
            mean_number_label.grid(column = 40,row=7,sticky='sE')

            max_label = tk.Label(root,text='حدبالا')
            max_label.grid(column = 41,row=8,sticky='sE')
            max_number_label = tk.Label(root,text='number')
            max_number_label.grid(column = 40,row=8,sticky='sE')

            min_label = tk.Label(root,text='حدپایین')
            min_label.grid(column = 31,row=8,sticky='sE')
            min_number_label = tk.Label(root,text='number')
            min_number_label.grid(column = 30,row=8,sticky='sE')

            stdv_label = tk.Label(root,text='انحراف معیار')
            stdv_label.grid(column = 41,row=9,sticky='sE')
            stdv_number_label = tk.Label(root,text='number')
            stdv_number_label.grid(column = 40,row=9,sticky='sE')

            def cal():
                mean_number_label.configure(text=
                                                mean(data[int(from_point.get(1.0, tk.END)):
                                                         int(to_point.get(1.0,tk.END))
                                                         ]
                                                    )
                                            )                    
                
                                                         
                max_number_label.configure(text=
                                               max(data[int(from_point.get(1.0, tk.END)):
                                                        int(to_point.get(1.0,tk.END))
                                                        ]
                                                   )
                                           )                    
            
                min_number_label.configure(text=
                                                   min(data[int(from_point.get(1.0, tk.END)):
                                                            int(to_point.get(1.0,tk.END))
                                                            ]
                                                       )
                                               )                    

                stdv_number_label.configure(text=format(
                                                     stdev(data[int(from_point.get(1.0, tk.END)):
                                                              int(to_point.get(1.0,tk.END))
                                                              ]
                                                           ),
                                                        '.3f'
                                                        )
                                               )                    

            
            cal_button = tk.Button(root,text='  محاسبه  ',command=cal)
            cal_button.grid(column=41,row=6)
            
            
            def export():
                write_to_excel(data,unit)
            
            
            export_button = tk.Button(root,text='  انتقال به اکسل  ',command=export)
            export_button.grid(column=41,row=10)
            
            draw_real_time(data,unit)
            
    show()
    
  