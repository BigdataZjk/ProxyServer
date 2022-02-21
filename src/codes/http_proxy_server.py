#coding:utf-8
from threading import Timer, Thread

from gui_codes.login import sign_in_window
import socket, _thread, select, time
from codes.decrypt import read_and_decode
import _thread
import socket
import tkinter as tk
from gui_codes.decrypt_frame import *

BUFFER_SIZE = 20480
HTTPVER = 'HTTP/1.1'
__version__ = '0.1.0 Draft 1'
VERSION = 'Python Proxy/'+__version__
global_data_list = [{"1":2}]


PROXY_LINE_NUM = 0
#===============================================================================SOCKET代理模块===============================================================================
class ConnectionHandler(object):
    def __init__(self, connection, address, timeout):
        self.client = connection
        self.client_buffer = b''
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        self.target.close()
    #断开链接
    def link_close(self):
        self.client.close()
        self.target.close()
    # 获取客户端请求
    def get_base_header(self):
        while 1:
            self.client_buffer += self.client.recv(BUFFER_SIZE)
            end = self.client_buffer.find(b'\r\n')
            if end!=-1:
                break
        buff_str = str(self.client_buffer[:end+1],encoding='unicode_escape')
        data = buff_str.split()
        # self.client_buffer = self.client_buffer[end+1:]
        if (buff_str.find(r'm.analytics.126.net') > 0) & (self.client_buffer.find(b'\r\n\x1f\x8b') > 0):
            #抓取并解密POST埋点数据
            tmp = read_and_decode(self.client_buffer)
            # 新消息 拆成单个 放入列表
            self.reload_msg_list(tmp)
        return self.listRepack(data)

    def method_CONNECT(self):
        self._connect_target(self.path)
        self.client.send((HTTPVER+' 200 Connection established\n'+
                          'Proxy-agent: %s\n\n'%VERSION).encode())
        self.client_buffer = b''
        self._read_write()

    def method_others(self):
        self.path = self.path[7:]
        i = str(self.path).find(r'/')
        host = self.path[:i]
        path = self.path[i:]
        self._connect_target(host)
        self.target.send(('%s %s %s\r\n'%(self.method, path, self.protocol)).encode() + self.client_buffer)
        self.client_buffer = b''
        self._read_write()

    def _connect_target(self, host):
        i = str(host).find(r':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(soc_family)
        self.target.connect(address)

    def _read_write(self):
        try:
            time_out_max = self.timeout/2
            socs = [self.client, self.target]
            count = 0
            while 1:
                count += 1
                (recv, _, error) = select.select(socs, [], socs, 1)
                if error:
                    break
                if recv:
                    for in_ in recv:
                        data = in_.recv(BUFFER_SIZE)
                        if in_ is self.client:
                            out = self.target
                        else:
                            out = self.client
                        if data:
                            out.send(data)
                            count = 0
                if count == time_out_max:
                    break
        except Exception as e:
            pass

    def listRepack(self,li):
        new_list = []
        for i in range(3):
            new_list.append(li[i])
        return new_list

    def reload_msg_list(self,new_josn_array):
        global global_data_list
        if new_josn_array is None or new_josn_array == '':
            return
        json_arr = json.loads(new_josn_array)
        for single_json in json_arr:
            # print('+++++  ',single_json)
            if single_json['e']:
                e = single_json['e']
                for i in range(len(e)):
                    dic_item = {}
                    #获取event_id
                    event_id = e[i]['n']
                    #获取event_time
                    timestamp = float(int(e[i]['ts'])/1000)
                    time_local = time.localtime(timestamp)
                    event_time = time.strftime("%H:%M:%S",time_local)
                    #key[event_id---event_time]
                    dic_key = event_id + '---' + event_time
                    #value[simple_msg]
                    simple_msg = json.dumps({**e[i], **get_data(single_json)})
                    dic_item[dic_key] = simple_msg
                    global_data_list.append(dic_item)
        # print(global_data_list)
def get_data(msg):
    tmp = dict(msg)
    del tmp['e']
    return tmp
#===============================================================================代理模块===============================================================================
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
        self.change_btn = tk.Button(self.root, text='切换解密面板...',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=17, command=self.open_other_frame)
        self.change_btn.place(x=830, y=0)
        #开启/重启 代理按钮
        self.restart_btn = tk.Button(self.root, text='开启代理...',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=15 ,command= self.write_kv_to_table)
        self.restart_btn.place(x=535, y=0)
        #清屏按钮
        self.restart_btn = tk.Button(self.root, text='清屏',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=10 ,command= self.clean_table)
        self.restart_btn.place(x=40, y=0)
        #左边的选择概述列表
        self.left_sb = Scrollbar(self.root)
        self.lb = Listbox(self.root,yscrollcommand= self.left_sb.set)
        for i in range(300):
            self.lb.insert(END,i)
        self.lb.place(x=25,y=34,relwidth=0.9,relheight=0.9)
        #左滚动条 绑定左list + 样式
        self.left_sb.pack(side=LEFT, fill=Y)
        self.left_sb.config(width=25, orient='vertical',command=self.lb.yview)
        #右边的文本
        self.mt = Text(self.root, width=10, height=48)
        self.mt.place(x=145,y=35,relwidth=0.9,relheight=0.9)

        self.root.mainloop()
        self.time_task

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

    #抓包数据 动态打印
    def write_kv_to_table(self):
        global global_data_list
        # self.clean_table
        for dic in global_data_list:
            key_list = list(dic.keys())
            for k in key_list:
                self.lb.insert(1,k)
    #抓包数据 动态打印
    def clean_table(self):
        global global_data_list
        global_data_list = []
        if self.mt.get(1.0,END) != '':
            self.mt.delete(1.0,END)
        if self.lb.get(0,END) != ():
            self.lb.delete(0,END)
        else:
            self.mt.insert(1.0,'======无需清空======')
    #定时刷新
    def time_task(self):
        Timer(1, self.write_kv_to_table, ()).start()

# #结束线程
# def tid_drop_thread(tid, exctype):
#     if not inspect.isclass(exctype):
#         raise TypeError("Only types can be raised (not instances)")
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
#     if res == 0:
#         raise ValueError("invalid thread id")
#     elif res != 1:
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")


#开启/重启 事件
def start_server(host='192.168.1.3', port=8889, IPv6=False, timeout=60,handler=ConnectionHandler):

    # tid_drop_thread(xxxx.ident, SystemExit)
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print( "Serving on %s:%d."%(host, port))
    soc.listen(1)
    while 1:
        # print(handler.get_global_msg_list(handler))
        th = _thread.start_new_thread(handler, soc.accept()+(timeout,))
        _thread.TIMEOUT_MAX
        time.sleep(0.3)

def st():
    pf = proxy_frame()
    pf.time_task
    print(111)
if __name__ == '__main__':
    t_list = []
    t_list.append(Thread(target=start_server))
    t_list.append(Thread(target=st))
    # if sign_in_window():
    for th in t_list:
        th.start()


    # login = sign_in_window()

