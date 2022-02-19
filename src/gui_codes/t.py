#coding:utf-8
from tkinter import *
'''
为Listbox添加滚动条。
滚动条是独立的组件。
为了在某个足尖上安装垂直滚动条，你需要做两件事：
1、设置该组件的yscrollbarcommand选项为Scrollbar组件的set()方法
2、设置Scrollbar组件的command选项为该组件的yview()方法
'''
root = Tk()

mainloop()

