#coding:utf-8
import tkinter as tk
import tkinter.messagebox
from tkinter import font
from codes.http_proxy_server import ConnectionHandler
from gui_codes import tips_control
import _thread
import socket
import time
from gui_codes.proxy_frame import use_window_init


def sign_in_window():
    #==============================================登陆界面==============================================================
    login_window = tk.Tk()
    login_window.title('请登陆后使用')
    login_window.resizable(0,0)
    screen_width_x = str(int(login_window.winfo_screenwidth()/2) - 160)
    screen_height_y = str(int(login_window.winfo_screenheight()/2) - 100)
    screen_inti_str = r'340x180' + r'+' + screen_width_x + r'+' + screen_height_y
    login_window.geometry(screen_inti_str)

    lab_1 = tk.Label(login_window,width=7,text='本地IPV4:',compound='center')
    lab_1.place(x=30,y=40)

    lab_2 = tk.Label(login_window,width=7,text='使用密码:',compound='center')
    lab_2.place(x=32,y=80)
    global uesr_name,password
    user_name = tk.StringVar()
    password= tk.StringVar()
    #用户名输入框
    entry = tk.Entry(login_window,textvariable=user_name,font='Times',bd=4)
    entry.pack()
    entry.place(x=100,y=41)
    #密码输入框 不可见
    passwd_entry = tk.Entry(login_window,show='*',textvariable=password,font='Times',bd=4)
    passwd_entry.pack()
    passwd_entry.place(x=100,y=80)
    #鼠标悬停 显示密码的label件，绑定事件
    show_passwd_label = tk.Label(login_window,text='显示密码',font=('华文行楷',10,'italic',font.BOLD))
    toolTip = tips_control.ToolTip(show_passwd_label)
    def enter(event):
        toolTip.showtip(passwd_entry.get())
    def leave(event):
        toolTip.hidetip()
    show_passwd_label.bind('<Enter>', enter)
    show_passwd_label.bind('<Leave>', leave)
    # create_ToolTip(show_passwd_label, passwd_entry.get())
    show_passwd_label.pack()
    show_passwd_label.place(x=260,y=150)
    #登陆 按钮
    btn = tk.Button(login_window,text='登陆',fg='black',width=8,compound='center', bg = 'white',cursor='hand2',command = lambda :jurge(login_window))
    btn.pack()
    btn.place(x=140,y=130)

    def jurge(login_window):
        if entry.get().startswith(r'192') and  passwd_entry.get() =='zjk':
            tk.messagebox.showinfo('^_^','欢迎使用本工具')
            #密码正确 进入工具界面
            login_window.destroy()
            use_window_init()
        elif passwd_entry.get() !='zjk':
            tk.messagebox.showerror('*_*','密码错误,请重新输入')
        elif not entry.get().startswith(r'192'):
            tk.messagebox.showerror('*_*','IP错误,请重新输入')

    def start_server(host=entry.get(), port=8889, IPv6=False, timeout=60,handler=ConnectionHandler):
        if IPv6==True:
            soc_type=socket.AF_INET6
        else:
            soc_type=socket.AF_INET
        soc = socket.socket(soc_type)
        soc.bind((host, port))
        print( "Serving on %s:%d."%(host, port))#debug
        soc.listen(1)
        while 1:
            _thread.start_new_thread(handler, soc.accept()+(timeout,))
            _thread.TIMEOUT_MAX
            time.sleep(0.3)
    login_window.mainloop()

if __name__ == '__main__':
    # 登陆
    sign_in_window()
