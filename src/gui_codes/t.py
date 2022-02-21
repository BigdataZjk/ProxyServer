from tkinter import *
from tkinter.ttk import Treeview

#排序函数
def tree_sort_column(tree,col,reverse):   				#Treeview、列名、排列方式
    l = [(tree.set(k,col),k) for k in tree.get_children('')]
    l.sort(reverse=reverse)  		# 排序方式
    for index,(val,k) in enumerate(l):  # 根据排序后索引移动
        tree.move(k, '', index)
    tree.heading(col,command=lambda:treeview_sort_column(tree,col,not reverse))
#点击复制到粘贴板
def treeviewclick(event,tree):
    window.clipboard_clear()
    strs=""
    for item in tree.selection():
        item_text=tree.item(item,"values")
        strs+=item_text[0]+"\n"					#获取本行的第一列的数据
    window.clipboard_append(strs)

window=Tk()
window.geometry('200x450')
cols = ("姓名", "IP地址")
ybar=Scrollbar(window,orient='vertical')      #竖直滚动条 
tree=Treeview(window,show='headings',columns=cols,yscrollcommand=ybar.set)
ybar['command']=tree.yview
#表头设置
for col in cols:
    tree.heading(col,text=col,command=lambda col=col:tree_sort_column(tree,col,False))             #行标题
    tree.column(col,width=80,anchor='w')   #每一行的宽度,'w'意思为靠右
#插入数据
for i in range(1,500):
    tree.insert("","end",values=("john","1.1.1.1"+str(i)))

tree.grid(row=0,column=0)				#grid方案
ybar.grid(row=0,column=1,sticky='ns')
tree.bind('<ButtonRelease-1>',lambda event:treeviewclick(event,tree))	#实现点击行的第一个数据复制到粘贴板
#ybar.pack(side='right',fill='y')		#pack方案
#tree.pack(fill='x')
window.mainloop()
