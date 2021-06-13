from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect
import base64
import random

def index(request:HttpRequest):
    return HttpResponseRedirect("/Affine/")


from .DES_cryptogram import DES_decrypt ,DES_encrypt,get_random
import binascii
def DES(request: HttpRequest):
    if request.method == 'POST':
        Key = request.POST.get('Key', None)  # 初始密钥
        text = request.POST.get('written_words', None)  # 输入文字
        pattern = request.POST.get('pattern', None)  # 模式选择
        mode = request.POST.get('mode', None)  # 加密或解密判断
        IV = request.POST.get('IV', None) #初始向量
        if mode == "random": #随机产生初始密钥
            IV, Key = get_random()
            Key = base64.b64encode(Key)      #用base64编码在http过程交互
            IV = base64.b64encode(IV)
            Response = {}
            Response['Key'] = str(Key, encoding="utf-8")
            Response['IV'] = str(IV, encoding="utf-8")
            return HttpResponse(json.dumps(Response))         #ajax只能接受一个返回字符串，所以将对应的字典json序列化
        elif mode == "encrypt":  # 加密
            Key = base64.b64decode(Key)
            IV = base64.b64decode(IV)
            ciphertext = DES_encrypt(text, Key, pattern, IV)
            #ciphertext = base64.b64encode(ciphertext)
            return HttpResponse(ciphertext)
        elif mode == "decrypt":  # 解密
            Key = base64.b64decode(Key)
            IV = base64.b64decode(IV)
            Plaintext = DES_decrypt(text, Key, pattern, IV)
            return HttpResponse(Plaintext)
    return render(request, 'DES.html')


from .RSA_cryptogram import RSA_encrypt,RSA_decrypt,RSA_Build_key
import json
def RSA(request: HttpRequest):
    if request.method == 'POST':
        e = request.POST.get('e', None)
        d = request.POST.get('d', None)
        text = request.POST.get('written_words', None)  # 输入文字
        mode = request.POST.get('mode', None)  # 生成密钥或加密或解密判断
        if mode == "Generate_key":#生成密钥
            p, q, n, e, d = RSA_Build_key()  # n是p*q,e是公钥，d是私钥
            Response = {}
            request.session['n'] = n                  #将n暂存
            Response['e'] = str(e)
            Response['d'] = str(d)                    #ajax一次请求只能返回一个字符串，同时返回两个数据需要拼接为一个串，使用json序列
            return HttpResponse(json.dumps(Response))    #json.dumps转换为json字符串，dump转化为json对象
        elif mode == "decrypt": #解密
            n = request.session['n']                   #取出暂存的n
            text = RSA_decrypt(text, int(d), int(n))        #解密
            text = base64.b64decode(text)              #base64解码为bytes
            text = str(text, encoding="utf-8")           #bytes转换为string，utf-8编码
            return HttpResponse(text)
        elif mode == "encrypt":#加密
            text = bytes(text, encoding="utf-8")  # str->bytes
            text = base64.b64encode(text)  # bytes->base64
            text = str(text, encoding="utf-8")  # base64 ->str
            n = request.session['n']
            ciphertext = RSA_encrypt(text, int(e), int(n))     #加密
            return HttpResponse(ciphertext)
    return render(request, 'RSA.html')


def Affine(request: HttpRequest):
    from .Affine_cryptogram import encrypt,decrypt
    if request.method == 'POST':
        Multiplication_coefficient = request.POST.get('Multiplication_coefficient', None) #加系数
        Additive_coefficient = request.POST.get('Additive_coefficient', None)             #乘系数
        Plaintext = request.POST.get('written_words', None)                               #输入文字
        mode = request.POST.get('mode', None)                                             #加密或解密判断
        if mode == "encrypt": #加密
            Plaintext = bytes(Plaintext, encoding="utf-8")      #str->bytes
            Plaintext = base64.b64encode(Plaintext)    #bytes->base64
            Plaintext = str(Plaintext, encoding="utf-8") #base64 ->str
            ciphertext = encrypt(int(Multiplication_coefficient), int(Additive_coefficient), Plaintext)
            return HttpResponse(ciphertext)
        elif mode == "decrypt":    #解密
            Plaintext = decrypt(int(Multiplication_coefficient), int(Additive_coefficient), Plaintext)
            Plaintext = base64.b64decode(Plaintext)
            Plaintext = str(Plaintext, encoding="utf-8")
            return HttpResponse(Plaintext)
    return render(request, 'Affine.html')

from .RC4_cryptogram import RC4_decrypt, RC4_encrypt
def RC4(request: HttpRequest):
    if request.method == 'POST':
        Key_seed = request.POST.get('Key_seed', None)
        text = request.POST.get('written_words', None)                               #输入文字
        mode = request.POST.get('mode', None)                                             #加密或解密判断
        if mode == "encrypt": #加密
            Plaintext = bytes(text, encoding="utf-8")  # str->bytes
            Plaintext = base64.b64encode(Plaintext)  # bytes->base64
            Plaintext = str(Plaintext, encoding="utf-8")  # base64 ->str
            print(Plaintext)
            ciphertext = RC4_encrypt(Plaintext, Key_seed)
            return HttpResponse(ciphertext)
        elif mode == "decrypt":    #解密
            Plaintext = RC4_decrypt(text, Key_seed)
            print(Plaintext)
            Plaintext = base64.b64decode(Plaintext)
            return HttpResponse(Plaintext)
    return render(request, 'RC4.html')

from .LFSR_JK_cryptogram import j_k_lfsr
def LFSR_JK(request: HttpRequest):
    if request.method == 'POST':
        J_iv = request.POST.get('J_iv', None)
        J_s = request.POST.get('J_s', None)
        K_iv = request.POST.get('K_iv', None)
        K_s = request.POST.get('K_s', None)
        text = request.POST.get('written_words', None)                               #输入文字
        mode = request.POST.get('mode', None)
        if mode == "random":
            J_iv = random.randint(0x12345678,0xffffffff)
            J_s = random.randint(0x12345678,0xffffffff)
            K_iv = random.randint(0x12345678,0xffffffff)
            K_s = random.randint(0x12345678,0xffffffff)
            Response = {}
            Response['J_iv'] = str(J_iv)
            Response['J_s'] = str(J_s)
            Response['K_iv'] = str(K_iv)
            Response['K_s'] = str(K_s)
            return HttpResponse(json.dumps(Response))
        #加密或解密判断
        elif mode == "encrypt": #加密
            J_iv = int(J_iv)
            J_s = int(J_s)
            K_iv = int(K_iv)
            K_s = int(K_s)
            plaintext = bytes(text, encoding="utf-8")
            jk1 = j_k_lfsr(J_iv, K_iv, J_s, K_s)
            ciphertext = jk1.lfsr_jk(plaintext)
            for index in range(len(ciphertext)):
                ciphertext[index] = str(ciphertext[index])
            ciphertext = ' '.join(ciphertext)
            ciphertext = base64.b64encode(bytes(ciphertext, encoding="utf-8"))
            ciphertext = str(ciphertext, encoding="utf-8")
            return HttpResponse(ciphertext)
        elif mode == "decrypt":    #解密
            J_iv = int(J_iv)
            J_s = int(J_s)
            K_iv = int(K_iv)
            K_s = int(K_s)
            text = base64.b64decode(text)
            text = text.split()
            for index in range(len(text)):
                text[index] = int(text[index])
            jk2 = j_k_lfsr(J_iv, K_iv, J_s, K_s)
            plaintext = jk2.lfsr_jk(text)
            return HttpResponse(str(bytes(plaintext), encoding="utf-8"))



    return render(request, 'LFSR_JK.html')
'''
Generate_Client_key
Client_e
Client_d
Generate_Server_key
Server_e
Server_d
Generate_PQ
P
Q
a
integrity_client 完整性
autograph 签名
text
send_text
b
integrity_server
shared_key
'''
from .DH_cryptogram import get_random_key, MRF, to_sign_with_private_key, to_verify_with_public_key
def DH(request: HttpRequest): #主要使用session
    if request.method == 'POST':
        Client_d = request.POST.get('Client_d', None)
        text = request.POST.get('text', None)
        mode = request.POST.get('mode', None)  # 生成密钥或加密或解密判断
        if mode == "Generate_Client_key":
            Client_d, Client_e = get_random_key()
            Response = {}
            Response['Client_d'] = str(Client_d, encoding="utf-8")
            Response['Client_e'] = str(Client_e, encoding="utf-8")
            request.session['Client_e'] = str(Client_e, encoding="utf-8")
            request.session['Client_d'] = str(Client_d, encoding="utf-8")
            print(Response)
            return HttpResponse(json.dumps(Response))    #json.dumps转换为json字符串，dump转化为json对象
        elif mode == "Generate_Server_key":
            Server_d, Server_e = get_random_key()
            Response = {}
            Response['Server_d'] = str(Server_d, encoding="utf-8")
            Response['Server_e'] = str(Server_e, encoding="utf-8")
            request.session['Server_d'] = str(Server_d, encoding="utf-8")
            request.session['Server_e'] = str(Server_e, encoding="utf-8")
            return HttpResponse(json.dumps(Response))    #json.dumps转换为json字符串，dump转化为json对象            Client_d, Client_e = get_random_key()
            Response = {}
            Response['Client_d'] = str(Client_d, encoding="utf-8")
            Response['Client_e'] = str(Client_e, encoding="utf-8")
            return HttpResponse(json.dumps(Response))    #json.dumps转换为json字符串，dump转化为json对象
        elif mode == "Generate_PQ":
            P= random.randint(10000, 100000)
            Q = random.randint(10000, 100000)
            a = random.randint(100000, 1000000)
            P_Q = MRF(a, P, Q)
            request.session['P_Q'] = P_Q
            request.session['P'] = P
            request.session['Q'] = Q
            request.session['a'] = a
            Response = {}
            Response['P'] = P
            Response['Q'] = Q
            Response['a'] = a
            return HttpResponse(json.dumps(Response))    #json.dumps转换为json字符串，dump转化为json对象
        elif mode == "autograph":
            g_a = str(request.session['P_Q'])
            text = to_sign_with_private_key(g_a, bytes(request.session['Client_d'], encoding="utf-8"))
            # print(type(text))
            text = base64.b64encode(text)  # bytes->base64
            text = str(text, encoding="utf-8")  # base64 ->str
            return HttpResponse(text)
        elif mode == "send_text":
            # print(type(text))#原本的text读出是string类型，我们需要传参bytes类型
            text = bytes(text, encoding="utf-8")
            text = base64.b64decode(text)
            Vertify = to_verify_with_public_key(text,str(request.session['P_Q']),request.session['Client_e'])
            print(text)
            if Vertify == True:
                b = random.randint(100000, 1000000)
                g_b = MRF(b, int(request.session['P']), int(request.session['Q']))
                text_b = to_sign_with_private_key(str(g_b), bytes(request.session['Server_d'], encoding="utf-8"))
                print(type(text_b))
                print("omg")
                Vertify_b = to_verify_with_public_key(text_b, str(g_b), request.session['Server_e'])
                print(Vertify_b)
                if Vertify_b == True:

                    g_ab= MRF(int(request.session['a'])*b, int(request.session['P']), int(request.session['Q']))
                    print(g_ab)
                    Response = {}
                    Response['gab'] = str(g_ab)
                    Response['gab1'] = str(g_ab)
                    Response['b'] = str(b)
                    print("i am her  e")
                    return HttpResponse(json.dumps(Response))
               #json.dumps转换为json字符串，dump转化为json对象
    return render(request, 'DH.html')

def AES(request: HttpRequest):
    return render(request, 'AES.html')
def notfound_404(request: HttpRequest):
    return render(request, '404.html')



