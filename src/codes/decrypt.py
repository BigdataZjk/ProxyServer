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

# if __name__ == '__main__':
#     inputCommend = '1'
#     key = 'neteasemobiledat'
#     inputCommend = input('请输入解密串(0退出)：')
#     while inputCommend != '0':
#         if len(inputCommend) < 16 | inputCommend.isspace():
#             print('输入长度错误，重新输入')
#             inputCommend = input('请输入解密串(0退出)：')
#             continue
#         elif str(inputCommend).find('\/') != -1:
#             print('输入包含转义符:"\\"')
#             inputCommend = input('请输入解密串(0退出)：')
#             continue
#         else :
#             try:
#                 print('开始解密......')
#                 # result = json.dumps(aesDecrypt(key, inputCommend), sort_keys=True, indent=2)
#                 # print(result)
#                 # result2 = json.loads(re.sub(r'\\','',aesDecrypt(key, inputCommend)))
#                 # print(result2)
#                 result3 = json.loads(aesDecrypt(key, inputCommend))
#                 print(json.dumps(result3, sort_keys=True, indent=2))
#                 inputCommend = input('解密完成，请输入下一个解密串(0退出)：')
#                 continue
#             except TypeError:
#                 inputCommend = '0'
# data = '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'
# data = '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'
# print(aesDecrypt(DECTYPT_PASSWD, data))
# print(aesDecrypt(DECTYPT_PASSWD,'IF+Qt3hFULH/ple01M/xJ62fyfR7yV/dlpWMOakW1X/iqrIKF4gSYSjc0nLuUX+5b10rQX3oblKrZ+4no94bStOfnAPBunGKa1SKtRjO6No0TnhTiTdZvdmj8uuqPBzxqdm786tB1Cg+lwjrkStaxRuI1QFjA51LkXqfIOLn+iUtWPNZ4MsAN57aktB/AjHsmY9lYjeCMO7MtHK6LFwAAFl5O3iKkm2WMSbFIV4tDV+Ss0xUjSlM0pdhVGRq7LWGbhQd6Rv783AE1V7UrtmqdYzTX5HL72N70LL/OBnUsmhChGQRIacy+VXsVD2kqR5rEMZoUmUrmJfWBn9RPkG1mH2t/zgJMOi5eWsJI2DQEJBsxpTMEPPcdDQcurZYnR6YgTGdYlgrYTJqlsKzJO8v2vHuiqPntaBLNMiQ9QxmA1+xhM9Pl1CCfOxa8RBznm1+33SR/UAAqYUyPVytZKWf03lYb1m4Iyaw1xnReIw8grLGgH9SFyBt/5/WQ67+eGxCU0uVgpIwTEroLwkrtsL1hoHVtyNh6l4FFfsPxVo7k4Zjtp4Np/36tI/8cp4MiyV6svsEpbga1ug9bEftiHyIJh4Clg90j5FROl0u92fBDrHGyKl7lP5Qad4bgoy/z/BcTzoVG8ycK9kyF9bBqrRv2/qGq55zLni8cdTDNrt8JEOHVlhutRDA2q4iO5SycbqCskCQJk9sCGQU94FBkzlVH0PKK5VEry/BgDt89SvLJ+krl/VwIDd6DiNihlEAui8DusGH0Gj+jvQlhAjwbPZcMVF3kkVu8aw0jd9L9l1gz8IghuWB1C2HLeQbjWCgLskFk4jZHZK/w8Xj+Seg3F4kpKXOqFgLOjPn1FRr1vkt7clfp/dbOAhgJcCZnfYUyFfy6Uyl2+ZcQOdrsJaFJUwLInMdutiSwP9TCIlV13EzXcb9dWyRCyJ4/MYFvks6uGYy'))
