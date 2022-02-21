#coding:UTF-8
from tkinter import *
from tkinter import ttk

def ds(root):
    s=Label(root,text='目录1-test')
    s.pack()

def ctm(root):
    c=Label(root,text='目录2-test')
    c.pack()

def lts(root):
    l=Label(root,text='目录3-test')
    l.pack()

root = Tk()
root.geometry('800x600+250+50')
root.resizable(False,False)
root.title('主界面')

tv = ttk.Treeview(root, height=20, selectmode = 'browse',show= 'tree')
tv.insert('',0,text='----------------------')
tv.insert('',1,text='目录1')
tv.insert('',2,text='目录2')
tv.insert('',3,text='目录3')

tv.place(x=30,y=20)

def all(event):
    item = tv.selection() #'I001'、'I002'
    if item:
        txt = tv.item(item[0],'text')
        print(item,'  ',txt)
        if txt == '目录1':
            ds(root)
        elif txt == '目录2':
            ctm(root)
        elif txt == '目录3':
            lts(root)

tv.bind('<ButtonRelease-1>',all)

root.mainloop()