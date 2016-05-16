__author__ = 'Ilham'

import sys
import math

class des():
    # permutasi inisial IP
    ip = [57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8,  0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    #permutasi key PC-1
    pc1 = [56, 48, 40, 32, 24, 16,  8,
          0, 57, 49, 41, 33, 25, 17,
          9,  1, 58, 50, 42, 34, 26,
         18, 10,  2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14,
          6, 61, 53, 45, 37, 29, 21,
         13,  5, 60, 52, 44, 36, 28,
         20, 12,  4, 27, 19, 11,  3
    ]

    #permutasi key PC-2
    pc2 = [
        13, 16, 10, 23,  0,  4,
         2, 27, 14,  5, 20,  9,
        22, 18, 11,  3, 25,  7,
        15,  6, 26, 19, 12,  1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    #geser kiri pc1
    left_rotations = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]

    #ekspan plaintext dari 32 ke 48
    expansion_table = [
        31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]

    #Insialisasi S_box
    sbox = [
        # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        # S3
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        # S4
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        # S5
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        # S6
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        # S7
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        # S8
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]

    #permutasi output s-box
    p = [
            15, 6, 19, 20, 28, 11,
            27, 16, 0, 14, 22, 25,
            4, 17, 30, 9, 1, 7,
            23,13, 31, 26, 2, 8,
            18, 12, 29, 5, 21, 10,
            3, 24
        ]

    #permutasi final
    fp = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
    ]

    def __init__(self, IV, key, data):
        self.IV=IV
        self.binerIV=[]
        self.data=data
        self.key=key
        self.biner=[]
        self.binerdua=[]
        self.final=[]
        self.keybiner=[]
        self.kiri=[]
        self.kanan=[]
        self.keykiri=[]
        self.keykanan=[]
        self.subkunci=[ [0] * 48 ] * 16

    def encrypt(self, data):
        self.data = self.cekPadding(self.data)
        self
        #print"plaintext"
        self.biner=self.ubahBit(self.data, self.biner, 8)
        self.binerIV=self.ubahBit(self.IV, self.binerIV, 8)
        #print len(self.biner)
        #print "biner"
        #print self.biner
        flag=1
        self.block_cipher(flag)
        return self.ubahAscii(self.final)

    def decrypt(self, data):
        self.data = self.cekPadding(self.data)
        #print"plaintext"
        self.biner=self.ubahBit(self.data, self.biner, 8)
        self.binerIV=self.ubahBit(self.IV, self.binerIV, 8)
        #print "IV"
        #print self.IV
        #print self.binerIV
        #print len(self.biner)
        #print "biner"
        #print self.biner
        flag=0
        self.block_cipher(flag)
        return self.ubahAscii(self.final)


    def block_cipher(self, flag):
        i=0
        self.buat_subkey()
        while i < len(self.data) * 8:
            block=self.biner[i:i+64]

            if flag==1:
                #print self.binerIV
                #block = list(map(lambda x, y: x ^ y, block, self.binerIV))
                block=self.xor(block, self.binerIV)

            processed_block = self.des_crypt(block, flag)
            #print processed_block
            processed_block=self.ubahAscii(processed_block)

            if flag==1:
                self.binerIV = self.binerdua
                #print self.binerIV
            else:
            #    self.binerdua = list(map(lambda x, y: x ^ y, self.binerdua, self.binerIV))
                self.binerdua=self.xor(self.binerdua, self.binerIV)
                self.binerIV=self.binerdua
                #print self.binerIV

            self.final=self.final+self.binerdua
            i=i+64
            #break

#        print self.ubahAscii(self.final)

    def des_crypt(self, block, flag):
        #manipulasi awal (IP)
        block=self.permutasi(self.ip, block)
        self.kiri=block[:32]
        self.kanan=block[32:]
        #print "kiri"
        #print self.kiri
        #print "kanan"
        #print self.kanan

        if flag == 1:
            round=0
        else:
            round=15

        i=0
        while i<16:
            cad_kanan=self.kanan
            #print "self kanan"
            #print self.kanan
            #self.cekpanjangbit()
            self.kanan=self.permutasi(self.expansion_table, self.kanan)
            #print self.kanan

            #print self.subkunci[round]

            #print self.subkunci[round]
            self.kanan=self.xor(self.kanan, self.subkunci[round])
            #rint self.kanan
            #self.cekpanjangbit()

            temp=[0] * 32
            input_sbox=[0]*6
            j=0
            k=0
            while j < 8:
                input_sbox=self.kanan[k:k+6]
                #print "sbox input"
                #print input_sbox[j]

                baris=[]
                baris.append(input_sbox[0])
                baris.append(input_sbox[5])
                #print baris
                resbaris=0
                resbaris=self.binerkeangka(baris)
                #print resbaris

                kolom=[]
                kolom.append(input_sbox[1])
                kolom.append(input_sbox[2])
                kolom.append(input_sbox[3])
                kolom.append(input_sbox[4])
                #print kolom
                reskolom=0
                reskolom=self.binerkeangka(kolom)
                #print reskolom

                #print self.sbox[j]
                output=[0] * 4
                #print i
                #print j
                #print "sbox result"
                #print str(self.sbox[j][16*resbaris+reskolom])
                output=self.ubahBitDua(self.sbox[j][16*resbaris+reskolom])
                #print output
                #print output
                temp[j*4+0]=output[0]
                temp[j*4+1]=output[1]
                temp[j*4+2]=output[2]
                temp[j*4+3]=output[3]
#                print "\n"

                j=j+1
                k=k+6

            #print temp
            #print len(temp)
            balik32=[]
            balik32=self.permutasi(self.p, temp)
            #print balik32
            #print "\n"
            self.kanan=self.xor(balik32, self.kiri)
            #print self.kanan
            self.kiri=cad_kanan
            #print self.kiri
            #print balik32
            #self.cekpanjangbit()
            i=i+1
            if(flag==1):
                round=round+1
            else:
                round=round-1
            #print i

        #yang dipecah dijadikan satu lagi
        #print self.kiri
        #print self.kanan
        self.binerdua=self.kanan+self.kiri
        self.binerdua=self.permutasi(self.fp, self.binerdua)
        #print self.biner
        return self.binerdua

    def buat_subkey(self):
        self.keybiner=self.ubahBit(self.key, self.keybiner, 8)
        #print "keybiner"
        #print self.keybiner
        self.key=self.permutasi(self.pc1, self.keybiner)

        self.keykiri=self.key[:28]
        self.keykanan=self.key[28:]
        #print "key"
        #print self.keykiri
        #print self.keykanan

        i=0
        while i < 16:
            j=0
            while j < self.left_rotations[i]:
                self.keykiri.append(self.keykiri[0])
                del self.keykiri[0]

                self.keykanan.append(self.keykanan[0])
                del self.keykanan[0]

                j=j+1

            self.subkunci[i]=self.keykiri+self.keykanan
            self.subkunci[i]=self.permutasi(self.pc2, self.subkunci[i])

            #print "geser geser"
            #print self.keykiri
            #print self.keykanan
            #print self.subkunci[i]
            i=i+1

    def cekPadding(self, data):
        tambahan = 0
        if len(self.data)%8 != 0:
            tambahan = 8-len(self.data)%8
        if tambahan>0:
            x=0
            while x < tambahan:
                self.data=self.data+chr(0)
                x=x+1
        return self.data

    def ubahBit(self, abc, ubah, length):
        ubah=[0] * len(abc) * length
        #print "len"
        #print len(abc)
        #print len(ubah)

        i=0
        k=0
        while i < len(abc):
            j=length-1
            num=ord(abc[i])
            while j >= 0:
                if(num/pow(2,j)>0):
                    num=num-pow(2,j)
                    ubah[k]=1
                else:
                    ubah[k]=0
                j=j-1
                k=k+1
            i=i+1
        return ubah

    def ubahBitDua(self, angka):
        ubah=[0] * 4
        i=0
        while i < 4:
            if(angka/pow(2,3-i)>0):
                angka=angka-pow(2,3-i)
                ubah[i]=1
            else:
                ubah[i]=0
            i=i+1
        return ubah

    def ubahAscii(self, abc):
        ubah=[]

        i=0
        k=0
        while k < len(abc):
            temp=[0] * 8
            temp=abc[k:k+8]
            c=self.binerkeangka(temp)
            ubah.append(c)
            i=i+1
            k=k+8
        return ''.join([ chr(c) for c in ubah ])

    def permutasi(self, tabel, block):
        return list(map(lambda x: block[x], tabel))

    def xor(self, tabel1, tabel2):
        return list(map(lambda x, y: x ^ y, tabel1, tabel2))

    def cekpanjangbit(self):
        abc=[0] * 56
        z=0
        while z < 56:
            abc[z]=z%10
            z=z+1

        print abc

    def binerkeangka(self, data):
        i = 0
        res=0
        #print str(len(data)) + "len"
        while i < len(data):
            if(data[i]==1):
                res=res+pow(2,len(data)-i-1)
            i=i+1

        return res