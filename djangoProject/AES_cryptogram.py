from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def AES_encryption(data):
# 要加密的内容
# 随机生成16字节（即128位）的加密密钥
    key = get_random_bytes(16)
# 实例化加密套件，使用CBC模式
    cipher = AES.new(key, AES.MODE_CBC)
# 对内容进行加密，pad函数用于分组和填充
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data,cipher.iv,key
def AES_decrypt(data,key,iv):
    # 实例化加密套件
    from Crypto.Util.Padding import unpad
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密，如无意外data值为最先加密的b"123456"
    data = unpad(cipher.decrypt(data), AES.block_size)
    return data