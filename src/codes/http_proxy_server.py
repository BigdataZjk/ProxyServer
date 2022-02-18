#coding:utf-8
import socket, _thread, select, time
from codes.decrypt import read_and_decode

BUFFER_SIZE = 20480
HTTPVER = 'HTTP/1.1'
__version__ = '0.1.0 Draft 1'
VERSION = 'Python Proxy/'+__version__

global_data_list=[]

class ConnectionHandler:
    def __init__(self, connection, address, timeout):
        self.client = connection
        self.client_buffer = b''
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE'):
            self.method_others()
        # if self.client_buffer.find(b'\r\n\r\n') != -1:
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
            tmp= read_and_decode(self.client_buffer)
            print (tmp)#debug
            global_data_list.append(tmp)
        return listRepack(data)

    def method_CONNECT(self):
        # try:
        self._connect_target(self.path)
        self.client.send((HTTPVER+' 200 Connection established\n'+
                          'Proxy-agent: %s\n\n'%VERSION).encode())
        self.client_buffer = b''
        self._read_write()
        # except Exception as e:
        #     print(e)

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

def listRepack(li):
    new_list = []
    for i in range(3):
        new_list.append(li[i])
    return new_list

def getAllData(self):
    tmp=global_data_list[:]
    global_data_list.clear()
    return tmp

def current_iso8601(self):
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

def onUpdate(self):
    self.now.set(self.current_iso8601())
    self.after(100, self.onUpdate)

# def start_server(host='10.234.121.148', port=8889, IPv6=False, timeout=60,handler=ConnectionHandler):
#     if IPv6==True:
#         soc_type=socket.AF_INET6
#     else:
#         soc_type=socket.AF_INET
#     soc = socket.socket(soc_type)
#     soc.bind((host, port))
#     print( "Serving on %s:%d."%(host, port))#debug
#     soc.listen(1)
#     while 1:
#         _thread.start_new_thread(handler, soc.accept()+(timeout,))
#         _thread.TIMEOUT_MAX
#         time.sleep(0.3)