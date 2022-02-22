from tkinter import Scrollbar
from threading import Timer, Thread
from tkinter import messagebox, ttk
import select
from codes.decrypt import read_and_decode
import _thread
import socket
import tkinter as tk
from gui_codes.decrypt_frame import *
class table():
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0,0)
        screen_width_x = str(int(self.root.winfo_screenwidth()/2) - 500)
        screen_height_y = str(int(self.root.winfo_screenheight()/2) - 300)
        screen_inti_str = r'1024x670' + r'+' + screen_width_x + r'+' + screen_height_y
        self.root.geometry(screen_inti_str)
        self.root.title('银河代理')
        # #代理和解码 工具切换按钮
        # self.change_btn = tk.Button(self.root, text='切换解密面板...',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=17, command=self.open_other_frame)
        # self.change_btn.place(x=830, y=0)
        # # #刷新按钮
        # self.restart_btn = tk.Button(self.root, text='开启自动刷新',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=15 ,command= self.write_kv_to_table)
        # self.restart_btn.place(x=535, y=0)
        # #清屏按钮
        # self.restart_btn = tk.Button(self.root, text='清屏',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=10 ,command= self.clean_table)
        # self.restart_btn.place(x=40, y=0)
        # 左边列表使用树目录
        self.ybar = Scrollbar(self.root,orient='vertical')
        self.xbar = Scrollbar(self.root,orient='horizontal')

        self.tv = ttk.Treeview(self.root, selectmode = 'browse',yscrollcommand=self.ybar.set,xscrollcommand=self.xbar.set)

        self.ybar.config(width=20, orient='vertical',command=self.tv.yview)
        self.xbar.config(width=20, orient='horizontal',command=self.tv.xview)
        for i in range(1,500):
            self.tv.insert('',0,text=str(i)+'dawncuihuiuuuuuuuuuuuuuudfssdfsuuuuuuuuuuuu77777777777777777777777777777uuuuuuuuu')
        self.tv.place(relx=0.025, rely=0.05, relwidth=0.28, relheight=0.50)
        self.ybar.pack(side=LEFT, fill=Y)
        self.xbar.place(relx=0.6, rely=0.6)
        #右边的文本
        self.mt_ybar = Scrollbar(self.root,orient='vertical')
        self.mt = Text(self.root, width=10, height=48)
        self.mt.configure(yscrollcommand=self.mt_ybar.set)
        self.mt_ybar.config(width=20, orient='vertical',command=self.tv.yview)
        self.mt.place(relx=0.35, rely=0.05, relwidth=0.55, relheight=0.50)
        self.mt.configure(font=('Courier', 9))
        self.mt_ybar.pack(side=RIGHT, fill=Y)
        for i in range(1,300):
            self.mt.insert(1.0,str(i)+'dawncuihuiuuuuuuuu')
        self.root.mainloop()
if __name__ == '__main__':
    table()