#coding:utf-8
import tkinter as tk
import tkinter.messagebox
from tkinter import font
import tips_control
import gui_codes.tool
def sign_in_window():
    #==============================================登陆界面==============================================================
    login_window = tk.Tk()
    login_window.title('请登陆后使用')
    login_window.resizable(0,0)
    screen_width_x = str(int(login_window.winfo_screenwidth()/2) - 160)
    screen_height_y = str(int(login_window.winfo_screenheight()/2) - 100)
    screen_inti_str = r'340x180' + r'+' + screen_width_x + r'+' + screen_height_y
    login_window.geometry(screen_inti_str)

    lab_1 = tk.Label(login_window,width=7,text='用户名 :',compound='center')
    lab_1.place(x=30,y=40)

    lab_2 = tk.Label(login_window,width=7,text='密  码 :',compound='center')
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
    show_passwd_label = tk.Label(login_window,text='鼠标给我显示密码',font=('华文行楷',10,'italic',font.BOLD))
    toolTip = tips_control.ToolTip(show_passwd_label)
    def enter(event):
        toolTip.showtip(passwd_entry.get())
    def leave(event):
        toolTip.hidetip()
    show_passwd_label.bind('<Enter>', enter)
    show_passwd_label.bind('<Leave>', leave)
    # create_ToolTip(show_passwd_label, passwd_entry.get())
    show_passwd_label.pack()
    show_passwd_label.place(x=220,y=150)
    #登陆 按钮
    btn = tk.Button(login_window,text='登陆',fg='black',width=8,compound='center', bg = 'white',cursor='hand2',command = lambda :jurge(login_window))
    btn.pack()
    btn.place(x=140,y=120)

    def jurge(login_window):
        if entry.get() != 'zjk' or  passwd_entry.get() !='zjk':
            tk.messagebox.showerror('*_*','密码错误,请重新输入')
        else:
            tk.messagebox.showinfo('^_^','欢迎使用本工具')
            #密码正确 进入工具界面
            login_window.destroy()
    login_window.mainloop()

if __name__ == '__main__':
    # try:
        sign_in_window()

        gui_codes.use_window
