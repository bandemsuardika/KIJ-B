__author__ = 'Ilham'

from DES_bs import des

f = open('dataset.txt',"rb")
temp = f.readlines()
f.close()
dataset = []
for data in temp:
    dataset.append(data.replace('\r\n',''))
#print dataset
num=len(dataset)

i=0
while i < num:
    #print "inputkan initialization vector"
    IV = dataset[i]
    #print "inputkan key (8 karakter)"
    key = dataset[i+1]
    #print "inputkan plain text"
    plaintext=''
    plaintext = dataset[i+2]

    print "initialization vector: " + str(IV)
    print "plaintext: " + str(plaintext)

    #ciphertext = des(k1ey).encrypt(plaintext)
    ciphertext = des(IV, key, plaintext).encrypt(plaintext)
    print "ciphertext: " + str(ciphertext)

    dechipered_text = des(IV, key, ciphertext).decrypt(ciphertext)
    print "deciphered text: " + str(dechipered_text)

    #hasil_decrypt = des(ky).decrypt(ciphertext)
    #print "plain text has1il decipher: " + hasil_decrypt

    i=i+3
    print "\n"
