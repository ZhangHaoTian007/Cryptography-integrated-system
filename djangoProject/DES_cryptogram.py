from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from binascii import b2a_hex, a2b_hex
def get_random():
    # 随机生成8字节（即64位）的加密密钥
    return get_random_bytes(8), get_random_bytes(8)
import base64


def pkcs7_padding(data):  #补足8位pkcs7
    if not isinstance(data, bytes):
        data = data.encode()

    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def pkcs7_unpadding(padded_data):  #去除补位，这里没用到随便粘贴来了。
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
    data = unpadder.update(padded_data)
    try:
        uppadded_data = data + unpadder.finalize()
    except ValueError:
        raise Exception('无效的加密信息!')
    else:
        return uppadded_data


def DES_encrypt(data, key, pattern, iv):
# 要加密的内容
# 实例化加密套件，使用pattern模式
    data = data.encode()  #str->bytes加密需要字节流
    data = pkcs7_padding(data)   #补足八位
    des3 = DES.new(key, DES.MODE_CBC)
    if pattern == "CBC":
        des3 = DES.new(key, DES.MODE_CBC, iv)
    elif pattern == "ECB":
        des3 = DES.new(key, DES.MODE_ECB)  #ECB不需要iv
    elif pattern == "CFB":
        des3 = DES.new(key, DES.MODE_CFB, iv)
    elif pattern == "OFB":
        des3 = DES.new(key, DES.MODE_OFB, iv)
    cipher = des3.encrypt(data)
    return b2a_hex(cipher).decode().upper()    #由于可能有字节再utf-8编码之外，所以这里使用16进制的字符串
def DES_decrypt(data, key, pattern, iv):
    # 实例化加密套件
    '''
    pad = 8 - len(data) % 8
    padStr = ""
    for i in range(pad):
        padStr = padStr + chr(pad)
    data = data + padStr
    '''
    #data = base64.standard_b64decode(data)
    #data = pkcs7_unpadding(data)
    des3 = DES.new(key, DES.MODE_CBC)
    if pattern == "CBC":
        des3 = DES.new(key, DES.MODE_CBC, iv)
    elif pattern == "ECB":
        des3 = DES.new(key, DES.MODE_ECB)
    elif pattern == "CFB":
        des3 = DES.new(key, DES.MODE_CFB, iv)
    elif pattern == "OFB":
        des3 = DES.new(key, DES.MODE_OFB, iv)
    Plain = des3.decrypt(a2b_hex(data))
    #去除pkcs7补充的字节后得到的字符串
    return bytes.decode(Plain).rstrip("\x01"). \
        rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05"). \
        rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09"). \
        rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d"). \
        rstrip("\x0e").rstrip("\x0f").rstrip("\x10")
    return Plain


