from tkinter import Toplevel, LEFT, SOLID, BOTTOM, Label
#鼠标悬停 提示控件
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    #当光标移动指定控件是显示消息
    def showtip(self, text):
        'Display text in tooltip window'
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox('insert')
        x = x + self.widget.winfo_rootx()+30
        y = y + cy + self.widget.winfo_rooty()+30
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry('+%d+%d' % (x, y))
        label = Label(tw, text=self.text,justify=LEFT,
                      background='white', relief=SOLID, borderwidth=1,
                      font=('Times', '20'))
        label.pack(side=BOTTOM)
    #当光标移开时提示消息隐藏
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()