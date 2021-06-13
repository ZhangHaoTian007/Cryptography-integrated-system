class j_k_lfsr:
    def __init__(self, j_start, k_start, j_s, k_s):
        self.j_s = (0xffffffff - j_s) & 0xffffffff
        #print("self.j_s is: ", str(bin(self.j_s))[2:])
        self.k_s = (0xffffffff - k_s) & 0xffffffff
        self.j_start = j_start & 0xffffffff
        #print("self.j_start is: ", str(bin(self.j_start))[2:])
        self.k_start = k_start & 0xffffffff
        self.data_state = 0       #jk触发器的初始状态
    def lfsr_jk(self, plaintext):
        #print(plaintext)
        def count_ones(n):
            bin2 = str(bin(n))[2:]
            count = 0
            for i in str(bin2):
                if i == '1':
                    count += 1
            return count

        cipher = []
        for i in range(len(plaintext)):
            #print("plain[", i, "]is: ", str(bin(plaintext[i]))[2:])
            outputq = 0x00
            for i_2 in range(8):
                tj = self.j_start & self.j_s
                tk = self.k_start & self.k_s
                #print("tj is: ", str(bin(tj))[2:])
                newj = count_ones(tj) % 2
                newk = count_ones(tk) % 2
                #print("newj is: ", str(bin(newj))[2:])
                j = ((0x80000000 & tj) >> 31) & 0xffffffff
                k = ((0x80000000 & tk) >> 31) & 0xffffffff
                #print("j is: ", str(bin(j))[2:])
                self.j_start = ((self.j_start << 1) + newj) & 0xffffffff
                self.k_start = ((self.k_start << 1) + newk) & 0xffffffff
                #print("j_start is: ", str(bin(self.j_start))[2:])
                outputq = (outputq << 1) + (j ^ (not (j ^ k) & self.data_state))
                #print("output is: ", str(bin(outputq))[2:])
                self.data_state = j ^ (not (j ^ k) & self.data_state)
                #print("data_state is: ", str(bin(self.data_state))[2:])
            cipher.append((plaintext[i] ^ outputq))
            #print(cipher)
        return cipher
'''
j_start = int(324234324234342)
k_start = int(456456465466564)
j_s = int(516)
k_s = int(56)
jk1 = j_k_lfsr(j_start, k_start, j_s, k_s)
plaintext = "张皓天"
plaintext = bytes(plaintext, encoding="utf-8")
cipher = jk1.lfsr_jk(plaintext)
print("111111", cipher)
jk2 = j_k_lfsr(j_start, k_start, j_s, k_s)
plaintext = jk2.lfsr_jk(cipher)
print("222222", plaintext)
print(plaintext)
print(str(bytes(plaintext), encoding="utf-8"))
'''
