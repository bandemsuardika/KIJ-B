import socket
import sys
from DES_bs import des

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

ID_A = '00000001'
ID_B = '00000002'
key_A = '12345678'
Nonce1 = '87654321'

try:
        keyRequest = ID_A + '\n' + ID_B + '\n' + Nonce1
        print "mengirim  request key session (IDA || IDB || N1)"
        print keyRequest
        client_socket.send(keyRequest)

        response = client_socket.recv(1024)
        print "\nresponse KDC (E(Ka, [Ks || IDA || IDB || N1]) || E(Kb, [Ks || IDA])):\n" + response

        response = response.split('\n\n')
        untuk_A = response[0].split('\n')

        cek_IDA = des(key_A, untuk_A[1]).decrypt(untuk_A[1])
        cek_IDB = des(key_A, untuk_A[2]).decrypt(untuk_A[2])
        cek_Nonce1 = des(key_A, untuk_A[3]).decrypt(untuk_A[3])
        if(cek_IDA==ID_A and cek_IDB==ID_B and cek_Nonce1==Nonce1):
                print "\nresponse KDC terverifikasi"
                keySession = des(key_A, untuk_A[0]).decrypt(untuk_A[0])
                print "key session: " + keySession

                #di sini alice mengirimkan sebagian response KDC yang dienkripsi dengan Kb pada bob

                #di sini alice menerima response bob

                #di sini alice mengirim response alice pada bob
        else:
                print "response KDC tidak terverifikasi"

except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)
