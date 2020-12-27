import serial
import sys
from tkinter import messagebox as msg
import tkinter as tk
import matplotlib.pyplot as plt
from mytable import My_Table

def read_store():

    ser = serial.Serial('COM1', 9600, timeout=5)
    if not ser.is_open:
            msg.showerror('','COM1 IS NOT OPEN')
   
    if ser.read(100):   #ckeck device is on correct mode
        msg.showerror('','مطمئن شوید نیرو سنج در حالت ارسال همزمان داده نیست')
        return 0,0
    else:
        raw_data = ''

        while not raw_data:
            msg.showinfo('','کلید انتقال داده نیرو سنج را فشار دهید')
            raw_data = ser.read(2000)
            if not raw_data:
                answer = msg.askquestion('','داده‌ای دریافت نشد. منتظر می‌مانید؟')
                if answer == 'no':
                    return 0,0

        raw_data =  raw_data.decode().split()
        data =  [float(raw_data[x]) for x in range (0,len(raw_data),2)]
        unit = raw_data[1]
        ser.close()
    
        return data,unit
def draw_store_data(data,unit):
    plt.style.use('seaborn-whitegrid')
    fig = plt.figure()
    axis = fig.add_subplot(111)
    x_values = [x for x in range(len(data))]
    y_values = data
    plt.scatter(x_values, y_values)
    axis.set_xlabel('Read')
    axis.set_ylabel(unit)
    axis.grid(linestyle = '-')
    plt.show()

def store_data_func(root):
    data,unit = read_store()
    if not(data == 0):#if device isnot in correct mode bypass function
        
        for child in root.winfo_children()[2:]:
            child.destroy()

        table = My_Table(root,data) 

        def mean():
            mean_text = tk.Text(root,height=1,width=10)
            mean_text.grid(column=10,row=1)
            try:
                mean_text.insert(tk.END,sum(table.choose_data)/len(table.choose_data))
            except :
                pass
        mean_button = tk.Button(root,text = 'محاسبه میانگین داده‌های انتخاب شده',command=mean)
        mean_button.grid(column=10,row=0)
        draw_store_data(data,unit)
