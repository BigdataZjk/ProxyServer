#coding:utf-8
import _thread
import tkinter as tk
import tkinter.messagebox
from threading import Thread
from tkinter import font
from codes.http_proxy_server import proxy_frame, start_server, get_local_ip
from gui_codes import tips_control

global_account = ''
global_passwd = ''
class sign_in_window(object):
    def __init__(self):
        #==============================================登陆界面==============================================================
        self.root = tk.Tk()
        self.root.title('请登陆后使用')
        self.root.resizable(0,0)
        screen_width_x = str(int(self.root.winfo_screenwidth()/2) - 160)
        screen_height_y = str(int(self.root.winfo_screenheight()/2) - 100)
        screen_inti_str = r'340x180' + r'+' + screen_width_x + r'+' + screen_height_y
        self.root.geometry(screen_inti_str)
    
        lab_1 = tk.Label(self.root,width=7,text='授权账户:',compound='center')
        lab_1.place(x=30,y=40)
    
        lab_2 = tk.Label(self.root,width=7,text='使用密码:',compound='center')
        lab_2.place(x=32,y=80)
        global uesr_name,password
        user_name = tk.StringVar()
        password= tk.StringVar()
        #用户名输入框
        self.entry1 = tk.Entry(self.root,textvariable=user_name,font='Times',bd=4)
        self.entry1.pack()
        self.entry1.place(x=100,y=41)
        #密码输入框 不可见
        self.entry2 = tk.Entry(self.root,show='*',textvariable=password,font='Times',bd=4)
        self.entry2.pack()
        self.entry2.place(x=100,y=80)
        #鼠标悬停 显示密码的label件，绑定事件
        show_passwd_label = tk.Label(self.root,text='显示密码',font=('华文行楷',10,'italic',font.BOLD))
        self.toolTip = tips_control.ToolTip(show_passwd_label)

        show_passwd_label.bind('<Enter>', self.enter)
        show_passwd_label.bind('<Leave>', self.leave)
        # create_ToolTip(show_passwd_label, passwd_entry.get())
        show_passwd_label.pack()
        show_passwd_label.place(x=260,y=150)
        #登陆 按钮
        btn = tk.Button(self.root,text='登陆',fg='black',width=8,compound='center', bg = 'white',cursor='hand2',command = self.jurge)
        btn.pack()
        btn.place(x=140,y=130)
    
        self.root.mainloop()
    def enter(self,event):
        self.toolTip.showtip(self.entry2.get())
    def leave(self,event):
        self.toolTip.hidetip()
    def jurge(self):
        global global_account,global_passwd
        account = self.entry1.get()
        passwd = self.entry2.get()
        if account in ['000'] and passwd =='000':
            global_account = account
            global_passwd = passwd
            tk.messagebox.showinfo('^_^','欢迎使用本工具')
            #密码正确 进入工具界面

            self.root.destroy()
        elif not account in ('000'):
            tk.messagebox.showerror('*_*','无此账号,请重新输入')
        elif passwd !='000':
            tk.messagebox.showerror('*_*','密码错误,请重新输入')
    def get_ip_passwd(self):
        return [global_account,global_passwd]
if __name__ == '__main__':
    sign_in_window()
    if global_account in ['000'] and global_passwd =='000':
        _thread.start_new_thread(proxy_frame, ())
        Thread(target=start_server(host=get_local_ip())).start()