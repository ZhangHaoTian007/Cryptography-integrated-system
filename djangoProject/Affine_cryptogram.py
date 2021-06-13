import string
def encrypt(k1,k2,message):
    dic = string.ascii_letters
    c = []
    for i in message:
        if i.islower():
            num = ord(i)-ord('a')
            c.append(dic[(num*k1+k2)%52])
        elif i.isupper():
            num = ord(i)-ord('A')+26
            c.append(dic[(num*k1+k2)%52])
        else:
            c.append(i)
    return ''.join(c)

def decrypt(k1,k2,message):
    inv = 0
    for i in range(52):
        if k1*i%52==1:
            inv = i
            break
    dic = string.ascii_letters
    m = []
    for i in message:
        if i.islower():
            num = ord(i)-ord('a')
            m.append(dic[inv*(num-k2)%52])
        elif i.isupper():
            num = ord(i)-ord('A')+26
            m.append(dic[inv*(num-k2)%52])
        else:
            m.append(i)
    return ''.join(m)

'''
message = 'YmDQhmDVurDQ TTSp'  # 待加密或解密的消息
a = 5  # key的范围0~51之间
b = 29  # key的范围0~51之间
xx = encrypt(a, b, message)
print(xx)
xx = decrypt(a, b, xx)
print(xx)
'''

