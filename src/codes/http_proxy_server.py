#coding:utf-8
import socket, _thread, select ,gzip
from io import StringIO

BUFFER_SIZE = 4096
HTTPVER = 'HTTP/1.1'
__version__ = '0.1.0 Draft 1'
VERSION = 'Python Proxy/'+__version__

class ConnectionHandler:
    def __init__(self, connection, address, timeout):
        self.client = connection
        self.client_buffer = ''.encode()
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        self.target.close()
    # 获取客户端请求
    def get_base_header(self):
        while 1:
            self.client_buffer += self.client.recv(BUFFER_SIZE)
            end = self.client_buffer.find(b'\r\n\r\n')
            if end!=-1:
                break
        # self.client_buffer = self.client_buffer[end+1:]
        buff_str = str(self.client_buffer[:end+1],encoding='unicode_escape')
        data = buff_str.split()
        if (buff_str.find(r'm.analytics.126.net') > 0) & (self.client_buffer.find(b'\r\n\x1f\x8b') > 0):
            print('wwwwwww ------- %s'%self.client_buffer)
            #抓取并解密POST埋点数据
            res = read_and_decode(self.client_buffer)
            print ('debug ------- %s'%res)#debug
        return listRepack(data)

    def method_CONNECT(self):
        # print('CONNECT......' + self.path)
        # try:
        # path_encode = self.path.encode()
        self._connect_target(self.path)
        self.client.send((HTTPVER+' 200 Connection established\n'+
                          'Proxy-agent: %s\n\n'%VERSION).encode())
        self.client_buffer = ''
        self._read_write()
        # except Exception as e:
        #     print('CONNECT-------ERR----------------------')
        #     print(e)

    def method_others(self):
        self.path = self.path[7:]
        # print('method_others : %s' %self.path  )
        i = str(self.path).find(r'/')
        host = self.path[:i]
        path = self.path[i:]
        self._connect_target(host)
        self.target.send(('%s %s %s\r\n'%(self.method, path, self.protocol)).encode() + self.client_buffer)
        self.client_buffer = ''
        self._read_write()
        # print('method_others is ok')

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
            time_out_max = self.timeout/3
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

#解压gzip
def gzdecode1(content1):
    return gzip.decompress(content1).decode("utf-8")
def gzdecode2(content2) :
    compressedstream = StringIO(content2)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2

#读取上报并解密
def read_and_decode(content3):
    android_ind = content3.find(b'\r\n\x1f\x8b')
    ios_ind = content3.find(b'\r\n\r\n\x1f\x8b')
    print(ios_ind)
    # Android
    if content3.find(b'Android') < 500 & android_ind < 300:
        i = content3[content3.find(b'\r\n\r\n')+4:]
        de_res = gzip.decompress(i).decode("utf-8")
        return de_res
    # IOS
    elif content3.find(b'iOS') < 500 &  ios_ind< 500:
        i = content3[content3.find(b'\r\n\r\n')+4:]
        de_res = gzip.decompress(i).decode("utf-8")
        return de_res
    else:
        pass
    return content3

#请求头取前 三位
def listRepack(li):
    new_list = []
    for i in range(3):
        new_list.append(li[i])
    return new_list

def start_server(host='10.234.121.148', port=8888, IPv6=False, timeout=60,
                 handler=ConnectionHandler):
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print( "Serving on %s:%d."%(host, port))#debug
    soc.listen(1)
    while 1:
        _thread.start_new_thread(handler, soc.accept()+(timeout,))

if __name__ == '__main__':
    start_server()