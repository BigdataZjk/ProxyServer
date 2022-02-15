#coding:utf-8
import socket, _thread, select ,gzip
from io import StringIO
from numpy import unicode

BUFLEN = 2048
HTTPVER = 'HTTP/1.1'
__version__ = '0.1.0 Draft 1'
VERSION = 'Python Proxy/'+__version__



class ConnectionHandler:
    def __init__(self, connection, address, timeout):
        self.client = connection
        # print('%s'%self.client)
        self.client_buffer = ''.encode()
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        # print('%s'%self.method)
        # print('%s'%self.path())
        # print('%s'%self.protocol)
        if self.method=='CONNECT':
            self.method_CONNECT()
            print('%s method go'%self.method)
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE'):
            self.method_others()
            print('%s method go'%self.method)
        self.client.close()
        self.target.close()
    #???
    def get_base_header(self):
        while 1:
            self.client_buffer += self.client.recv(BUFLEN)
            # print ('%s'%self.client_buffer)#debug
            # print(str(self.client_buffer))
            end = str(self.client_buffer).find('\\r\\n')
            if end!=-1:
                break
        # print ('%s'%self.client_buffer)#debug
        data = str(self.client_buffer[:end+1],encoding='utf-8').split()
        self.client_buffer = self.client_buffer[end+1:]
        print(listRepack(data)) ## 返回请求头的数据
        return listRepack(data)
    def method_CONNECT(self):
        print('CONNECT......' + self.path)
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
        print('method_others : %s' %self.path  )
        i = unicode(self.path).find('/')
        host = self.path[:i]
        path = self.path[i:]
        self._connect_target(host)
        self.target.send(('%s %s %s\r\n'%(self.method, path, self.protocol)).encode() + self.client_buffer)
        self.client_buffer = ''
        self._read_write()
        print('method_others is ok')
    def _connect_target(self, host):
        i = unicode(host).find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
            print('port is ---  %s'%port)
            print('host is ---  %s'%host)
        else:
            port = 80
        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(soc_family)
        self.target.connect(address)

    def _read_write(self):
        print('_read_write is run')
        time_out_max = self.timeout/3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for in_ in recv:
                    data = in_.recv(BUFLEN)
                    if in_ is self.client:
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.send(data)
                        count = 0
            if count == time_out_max:
                break

#解压gzip
# def gzdecode(content):
#     return gzip.decompress(content).decode('utf8')
def gzdecode(content) :
    compressedstream = StringIO.StringIO(content)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2
#请求头取前 三位
def listRepack(li):
    new_list = []
    for i in range(3):
        new_list.append(li[i])
    return new_list


def start_server(host='192.168.1.3', port=8888, IPv6=False, timeout=60,
                 handler=ConnectionHandler):
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print( "Serving on %s:%d."%(host, port))#debug
    soc.listen(0)
    while 1:
        _thread.start_new_thread(handler, soc.accept()+(timeout,))

if __name__ == '__main__':
    start_server()