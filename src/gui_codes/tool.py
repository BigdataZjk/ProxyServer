#coding:utf-8
import tkinter as tk

class use_window():

    tool_window = tk.Tk()
    tool_window.geometry('300x400')
    tool_window.title('新界面')
    Lab = tk.Label(tool_window,text='new window')
    Lab.pack()
    Lab.place(x=220,y=150)
    tool_window.mainloop()