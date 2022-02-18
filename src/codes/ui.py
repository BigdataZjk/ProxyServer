import json
import time
from tkinter import *
from decrypt import aesDecrypt
import hashlib

LOG_LINE_NUM = 0
DECTYPT_PASSWD = 'neteasemobiledat'

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title('银河埋点抓拆包工具')
        self.init_window_name.geometry('1068x681+400+50')
        self.init_window_name['bg'] = 'DEEPSKYBLUE'
        self.init_window_name.attributes('-alpha',0.618)   #虚化
        #标签
        self.init_data_label = Label(self.init_window_name, text='待解密数据')
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text='解密结果')
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text='日志')
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.aes_trans_to_str_button = Button(self.init_window_name, text='解密', bg='lightblue', width=10,command=self.aes_trans_to_str)  # 调用内部方法  加()为直接调用
        self.aes_trans_to_str_button.grid(row=1, column=11)

    #功能函数
    def aes_trans_to_str(self):
        aes_string = self.init_data_Text.get(1.0,END).strip().replace(' ','').replace('\n|\t','').encode('utf8')
        print(aes_string)
        aes_string2 = str(aes_string).replace(' ','').encode('utf8')
        if aes_string2:
            try:
                decrypt_res = aesDecrypt(DECTYPT_PASSWD, aes_string2)
                if '{' not in decrypt_res:
                    print()
                else:
                    middle_json = json.loads(aesDecrypt(DECTYPT_PASSWD, aes_string2))
                    decrypt_res = json.dumps(middle_json, sort_keys=True, indent=2)
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
        logmsg_in = str(current_time) +' ' + str(logmsg) + '\n'      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)

if __name__ == '__main__':
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()