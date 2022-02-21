#coding:utf-8
from threading import Timer, Thread
from tkinter import messagebox, ttk
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
global_data_list = []
table_data_list = []
LOGIN_IP = ''
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
            if 'e' in single_json:
                dic_item = {}
                e = single_json['e']
                event_id_list = []
                #把单json的 事件id 遍历放入 event_id_list
                for i in range(len(e)):
                    #获取event_id
                    event_id = e[i]['n']
                    event_id_list.append(event_id)
                dic_key = str(event_id_list) + '【%s】'%get_current_time()
                dic_item[dic_key] = single_json
                global_data_list.append(dic_item)
                # print(dic_item)
##================================================细拆==========================
                # for i in range(len(e)):
                #     dic_item = {}
                #     #获取event_id
                #     event_id = e[i]['n']
                #     #获取event_time
                #     timestamp = float(int(e[i]['ts'])/1000)
                #     time_local = time.localtime(timestamp)
                #     event_time = time.strftime("%H:%M:%S",time_local)
                #     #key[event_id---event_time]
                #     dic_key = event_id + '---' + event_time
                #     #value[simple_msg]
                #     simple_msg = json.dumps({**e[i], **get_data(single_json)})
                #     dic_item[dic_key] = simple_msg
                #     global_data_list.append(dic_item)
                #     print(dic_item)
        # print('global_data_list----%s'%global_data_list)
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
        #刷新按钮
        self.restart_btn = tk.Button(self.root, text='刷新',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=15 ,command= self.write_kv_to_table)
        self.restart_btn.place(x=535, y=0)
        #清屏按钮
        self.restart_btn = tk.Button(self.root, text='清屏',compound='center',fg='red',cursor='hand2', bg='lightblue',font=('',10, 'bold'), width=10 ,command= self.clean_table)
        self.restart_btn.place(x=40, y=0)
        # #左边列表
        # self.left_sb = Scrollbar(self.root)
        # self.bottom_sb = Scrollbar(self.root)
        # self.lb = Listbox(self.root,yscrollcommand= self.left_sb.set)
        # self.lb = Listbox(self.root,xscrollcommand= self.bottom_sb.set)
        # self.lb.place(x=25,y=34,relwidth=0.9,relheight=0.9)
        # #左\底部滚动条 绑定左list + 样式
        # self.left_sb.pack(side=LEFT, fill=Y)
        # self.left_sb.config(width=25, orient='vertical',command=self.lb.yview)
        # 左边列表使用树目录
        # self.ybar = Scrollbar(self.root,orient='vertical')
        self.xbar = Scrollbar(self.root,orient='vertical')

        self.tv = ttk.Treeview(self.root, height=10, selectmode = 'browse')

        # self.tv.configure(yscrollcommand=self.ybar.set)
        self.tv.configure(xscrollcommand=self.xbar.set)

        # self.ybar.config(width=25, orient='vertical',command=self.tv.yview)
        self.xbar.config(width=15, orient='vertical',command=self.tv.xview)
        # for i in range(1,500):
        #     self.tv.insert('',0,text='dawncuihuiuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
        self.tv.place(x=25,y=34,relwidth=0.9,relheight=0.9)
        # self.ybar.pack(side=LEFT, fill=Y)
        self.xbar.pack(side=BOTTOM, fill=X)
        self.root.bind('<ButtonRelease-1>',lambda event:self.treeviewclick(event))
        self.tv.bind('<ButtonRelease-1>',lambda event:self.click_event(event,self.tv))
        #右边的文本
        self.mt = Text(self.root, width=10, height=48)
        # self.mt.place(x=500,y=35,relwidth=0.9,relheight=0.9)
        self.mt.place(x=200,y=35,relwidth=0.9,relheight=0.9)
        self.mt.configure(font=('Courier', 16, 'italic'))
        self.root.mainloop()
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
        insert_list = self.init_show()
        global global_data_list
        if len(insert_list)>0:
            # print(json.dumps(insert_list, sort_keys=True, indent=2))
            for dic in insert_list:
                key_list = list(dic.keys())
                for k in key_list:
                    # self.lb.insert(1,k)
                    self.tv.insert('',0,text=k)
    #定时刷新
    def timer_show(self):
        t = RepeatingTimer(1,self.write_kv_to_table)
        t.start()
    #选择未展示的插入列表
    def init_show(self):
        data_insert = []
        global global_data_list,table_data_list
        for i in global_data_list:
            if i not in table_data_list:
                table_data_list.append(i)
                data_insert.append(i)
        return data_insert
    #清空面板
    def clean_table(self):
        global global_data_list
        global_data_list = []
        if self.mt.get(1.0,END) != '':
            self.mt.delete(1.0,END)
        if self.tv.selection() != ():
            for item in self.tv.get_children():
                self.tv.delete(item)

        else:
            self.mt.insert(1.0,'======无需清空======')
    #点击 复制
    def treeviewclick(self,event):
        item_text = ''
        self.root.clipboard_clear()
        ts = self.tv.selection()
        for item in ts:
            item_text = self.tv.item(item,'text')
        self.root.clipboard_append(item_text)
    #点击 显示原始数据
    def click_event(self,event,tree):
        old_json = ''
        key = ''
        global global_data_list
        for item in tree.selection():
            key = tree.item(item,'text')
        for i in global_data_list:
            if key in i:
                old_json = i[key]
        if self.mt.get(1.0,END) != '':
            self.mt.delete(1.0,END)
        self.mt.insert(1.0,old_json)

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

class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
#开启/重启 事件
def start_server(host,port=8889, IPv6=False, timeout=60,handler=ConnectionHandler):
    # tid_drop_thread(xxxx.ident, SystemExit)
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print( "Serving on %s:%d..."%(host, port))
    soc.listen(1)
    while 1:
        _thread.start_new_thread(handler, soc.accept()+(timeout,))
        _thread.TIMEOUT_MAX
        time.sleep(0.3)
def get_current_time():
    current_time = time.strftime('%H:%M:%S',time.localtime(time.time()))
    return current_time

if __name__ == '__main__':
    # sw = sign_in_window()
    # ip = sw.get_ip_passwd()[0]
    # passwd = sw.get_ip_passwd()[1]
    _thread.start_new_thread(proxy_frame, ())
    Thread(target=start_server(host='192.168.1.3')).start()

