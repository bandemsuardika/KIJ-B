__author__ = 'Ilham'

from DES_bs import des

print "inputkan initialization vector"
IV = raw_input()
print "inputkan key (8 karakter)"
key = raw_input()
print "inputkan plain text"
plaintext = raw_input()

#ciphertext = des(k1ey).encrypt(plaintext)
ciphertext = des(IV, key, plaintext).encrypt(plaintext)
print "ciphertext: " + str(ciphertext)

dechipered_text = des(IV, key, ciphertext).decrypt(ciphertext)
print "deciphered text: " + str(dechipered_text)

#hasil_decrypt = des(ky).decrypt(ciphertext)
#print "plain text has1il decipher: " + hasil_decrypt