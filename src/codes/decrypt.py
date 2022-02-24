import base64
import gzip

# from Crypto.Cipher import AES
from Cryptodome.Cipher import AES

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

#加密
def aesEncrypt(key, data):
    key = key.encode('utf8')
    # 补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后的bytes使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    return enctext

#解密
def aesDecrypt(key, data):
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 去补位
    unpadStr = unpad(cipher.decrypt(data))
    unpadStr = unpadStr.decode('utf8')
    return unpadStr

#chunket 解码
def decode_chunked(content):
    # 自定义chunked解码
    newContent = b''
    offset = 0
    while True:
        try:
            pos = content.find(b'\r\n', offset)  # 找chunked块的前一个\r\n
            chunk_size = int(content[offset: pos], 16)
            if chunk_size > 0:
                offset = pos + 2
                newContent += content[offset: offset+chunk_size]
                pos = content.find(b'\r\n', offset+chunk_size)   # 找chunked块的后一个\r\n
                offset = pos + 2
            else: break
        except BaseException as ret:
            print(f'没有达到最后一个chunked块!,{ret}')
            break
    return newContent



# 分端解gzip压缩 + 解密
def read_and_decode(content3):
    try:
        term_ind = content3.find(b'\x1f\x8b\x08\x00')
        if term_ind != -1 :
            # Android
            if content3.find(b'Android') != -1:
                a = content3[term_ind:-7]
                de_res = gzip.decompress(a).decode("utf-8")
                if '{' in de_res:
                    return de_res
                else:
                    return aesDecrypt(DECTYPT_PASSWD,de_res)
            # IOS
            elif content3.find(b'iOS') != -1:
                i = content3[content3.find(b'\x1f\x8b\x08\x00'):]
                de_res = gzip.decompress(i).decode("utf-8")
                if '{' in de_res:
                    return de_res
                else:
                    return aesDecrypt(DECTYPT_PASSWD,de_res)
            else:
                pass
            return content3
    except Exception as e:
        # if content3.find(b'\r\n0\r\n\r\n') != -1:
        #     print('content3----  %s'%content3)
        #     print('a---- %s'%a)
        #     print('content3[term_ind:]---- %s'%content3[term_ind-6:])
        #     print('decode_chunked---- %s'%decode_chunked(content3[term_ind-6:]))
        pass
