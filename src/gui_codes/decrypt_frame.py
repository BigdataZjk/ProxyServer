#coding:utf-8
import json
import tkinter
from tkinter import *
import time
from codes.decrypt import aesDecrypt

LOG_LINE_NUM = 0
DECTYPT_PASSWD = 'neteasemobiledat'

class decrypt_frame(object):
    def __init__(self,init_tk_object):
        self.init_tk_object = init_tk_object
        self.init_tk_object.resizable(0,0)
        screen_width_x = str(int(self.init_tk_object.winfo_screenwidth()/2) - 500)
        screen_height_y = str(int(self.init_tk_object.winfo_screenheight()/2) - 300)
        screen_inti_str = r'1024x670' + r'+' + screen_width_x + r'+' + screen_height_y
        self.init_tk_object.geometry(screen_inti_str)
        self.init_tk_object.title('银河埋点抓拆包工具')
        # self.init_tk_object['bg'] = 'DEEPSKYBLUE'
        # self.init_tk_object.attributes('-alpha',0.618)   #虚化
        #标签
        self.init_data_label = Label(self.init_tk_object, text='待解密数据',font=('楷体',10, 'bold'))
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_tk_object, text='解密结果',font=('楷体',10, 'bold'))
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_tk_object, text='日志',font=('楷体',10, 'bold'))
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = Text(self.init_tk_object, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_tk_object, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_tk_object, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.aes_trans_to_str_button = Button(self.init_tk_object, text='解密', bg='lightblue',font=('楷体',15, 'bold'), width=10,command=self.aes_trans_to_str)  # 调用内部方法  加()为直接调用
        self.aes_trans_to_str_button.grid(row=1, column=11)
    #返回代理frame 按钮事件
    def show_root_window(self):
        self.init_tk_object.update()
        self.init_tk_object.deiconify()
    def close_other_frame(self, frame):
        # self.init_tk_object.destroy
        # frame.destroy()
        self.show_root_window()
    #功能函数
    def aes_trans_to_str(self):
        aes_string = str(self.init_data_Text.get(1.0,END)).replace(' ','').encode('utf8')
        if aes_string:
            try:
                decrypt_res = aesDecrypt(DECTYPT_PASSWD, aes_string)
                if '{' not in decrypt_res:
                    print()
                else:
                    middle_json = json.loads(decrypt_res)
                    decrypt_res = json.dumps(middle_json, sort_keys=True, indent=2,ensure_ascii=False)
                #输出到界面
                self.result_data_Text.delete(1.0,END) #清空内容
                self.result_data_Text.insert(1.0,decrypt_res)
                self.write_log_to_Text('INFO:aes_trans_to_str success')
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,'字符串解密失败')
        else:
            self.write_log_to_Text('ERROR:aes_trans_to_str failed')

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +' ' + str(logmsg) + '\n'
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)
# init_window = tkinter.Tk()
# decrypt_frame_ = decrypt_frame(init_window)
# init_window.mainloop()