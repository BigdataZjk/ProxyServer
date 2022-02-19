#coding:utf-8
import _thread
import socket
import tkinter as tk
from concurrent.futures import thread
from queue import Queue
from tkinter import messagebox
from tkinter import *
import time
import inspect
import ctypes
from codes.http_proxy_server import ConnectionHandler
from gui_codes.decrypt_frame import decrypt_frame

class proxy_frame(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0,0)
        screen_width_x = str(int(self.root.winfo_screenwidth()/2) - 500)
        screen_height_y = str(int(self.root.winfo_screenheight()/2) - 300)
        screen_inti_str = r'1024x670' + r'+' + screen_width_x + r'+' + screen_height_y
        self.root.geometry(screen_inti_str)
        self.root.title('银河代理')
        #代理和解码 工具切换按钮
        btn = tk.Button(self.root, text='切换解密面板...',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=20, command=self.open_other_frame)
        btn.place(x=835, y=0)
        # #开启/重启 代理按钮
        # btn = tk.Button(self.root, text='切换解密面板...',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=20, command=start_server())
        # btn.place(x=835, y=0)
        #左边的选择概述列表
        sb = Scrollbar(self.root)    #垂直滚动条组件
        sb.pack(side=RIGHT,fill=Y)  #设置垂直滚动条显示的位置
        lb = Listbox(self.root,yscrollcommand=sb.set)    #Listbox组件添加Scrollbar组件的set()方法
        for i in range(1000):
            lb.insert(END,i)
        lb.pack(side=LEFT,fill=BOTH)
        sb.config(command=lb.yview) #设置Scrollbar组件的command选项为该组件的yview()方法

        # #右边的文本
        #
        # self.root = Text(self.root, width=67, height=35)  #原始数据录入框
        # self.root.grid(row=1, column=0, rowspan=10, columnspan=10)
        # self.result_data_Text = Text(self.init_tk_object, width=70, height=49)  #处理结果展示
        # self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        # self.log_data_Text = Text(self.init_tk_object, width=66, height=9)  # 日志框
        # self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #
        #
        #









        self.root.mainloop()
        #代理界面的数据源
        self.queue_msg = Queue()


    def on_closing(self):
        if messagebox.askokcancel("Quit","Do you want to quit?"):
            self.root.destroy()
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
        btn = tk.Button(init_window, text='返回代理......',fg='red',compound='center',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=20,command=lambda: self.close_other_frame(init_window))#font=('楷体', 10, 'bold', 'italic')
        btn.grid(row=0, column=20)
        #退出销毁父级
        init_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        init_window.mainloop()



def tid_drop_thread(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


#开启/重启 事件
def start_server(host='', port=8889, IPv6=False, timeout=60,handler=ConnectionHandler):

    # tid_drop_thread(xxxx.ident, SystemExit)
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print( "Serving on %s:%d."%(host, port))#debug
    soc.listen(1)
    while 1:
        th = _thread.start_new_thread(handler, soc.accept()+(timeout,))
        _thread.TIMEOUT_MAX
        time.sleep(0.3)

if __name__ == '__main__':


    proxy_frame()