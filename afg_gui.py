import tkinter as tk

from afg_store import read_store, draw_store_data,store_data_func
from afg_real_time import read_real_time,real_time_func


    

win = tk.Tk()
win.title('داده‌نگار')
win.geometry('1000x600')
win.columnconfigure(0, weight=1)
win.rowconfigure(0, weight=1)

frm_but = tk.Frame()
frm_but.grid(column=0,row=0,sticky='NE')

store_data = tk.Button(frm_but,text=' خواندن دادههای ذخیره شده',command=lambda :store_data_func(frm_but))
store_data.grid(column=30,row=0,sticky='NE',columnspan=2)

real_time_data = tk.Button(frm_but,text=' خواندن دادههای همزمان ',command=lambda:real_time_func(frm_but))
real_time_data.grid(column=40,row=0,sticky='NE',columnspan=2)





        


win.mainloop()