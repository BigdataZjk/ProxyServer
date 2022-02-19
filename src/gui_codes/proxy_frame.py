#coding:utf-8
import tkinter as tk
from tkinter import ttk

from gui_codes.decrypt_frame import decrypt_frame

class Tool_Start(object):

    def __init__(self, parent):
        self.root = parent
        self.root.resizable(0,0)
        self.root.title("Main frame")
        self.root.geometry("800x600")
        self.frame = tk.Frame(parent)
        self.frame.pack()
        btn = tk.Button(self.frame, text="Open Frame", command=self.open_other_frame)
        btn.pack()
    def hide_root_window(self):
        self.root.withdraw()
    def show_root_window(self):
        self.root.update()
        self.root.deiconify()
    def close_other_frame(self, frame):
        frame.destroy()
        self.show_root_window()
    def open_other_frame(self):
        self.hide_root_window()
        init_window = tk.Toplevel()
        decrypt_frame_ = decrypt_frame(init_window)
        decrypt_frame_.set_init_window()
        btn = tk.Button(init_window, text='返回代理......',fg='red',compound='center',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=20,command=lambda: self.close_other_frame(init_window))#font=('楷体', 10, 'bold', 'italic')
        btn.grid(row=0, column=20)
        init_window.mainloop()
def use_window_init():
    root = tk.Tk()
    init_ui = Tool_Start(root)
    root.mainloop()




# use_window_init()