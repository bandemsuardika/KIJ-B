__author__ = 'Ilham'

import socket
import select
import sys
from DES_bs import des

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

serverb_address = ('127.0.0.1', 5002)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(serverb_address)
server_socket.listen(5)

input_socket = [server_socket]

ID_A = '00000001'
ID_B = '00000002'
key_B = '23456789'
Nonce1 = '87654321'
Nonce2 = 1111111

x=raw_input('apakah mau memulai chat? (y/n)')
if x=='y':
    initiate = 1
else:
    initiate = 0

try:
        if initiate==0:
            while True:
                read_ready, write_ready, exception = select.select(input_socket, [], [])

                for sock in read_ready:
                    if sock == server_socket:
                        client_socket, client_address = server_socket.accept()
                        input_socket.append(client_socket)

                    else:
                        data = sock.recv(1024)
                        if data:
                            print "menerima response KDC dari alice (E(Kb, [Ks || IDA])):"
                            print data
                            untuk_B=data.split('\n')

                            cek2_IDA=des(key_B, untuk_B[1]).decrypt(untuk_B[1])
                            if(cek2_IDA==ID_A):
                                print "\nID A terverifikasi"
                                keySession = des(key_B, untuk_B[0]).decrypt(untuk_B[0])
                                print "key session: " + keySession

                            toBeEncrypted = str(Nonce2)
                            encryptedResponse = des(keySession, toBeEncrypted).encrypt(toBeEncrypted)
                            print "\nnonce 2: " + str(Nonce2)
                            print "mengirim encrypted nonce2 pada alice (E(Ks, N2)):"
                            print encryptedResponse
                            sock.send(encryptedResponse)

                            data2 = sock.recv(1024)
                            print "\nmenerima response dari alice (E(Ks, f(N2))):"
                            print data2
                            Nonce2mod = des(keySession, data2).decrypt(data2)
                            print "nonce 2 modifikasi:"
                            print Nonce2mod

                        else:
                            sock.close()
                            input_socket.remove(sock)

        else:
            keyRequest = ID_B + '\n' + ID_A + '\n' + Nonce1
            print "mengirim  request key session (IDB || IDA || N1)"
            print keyRequest
            client_socket.send(keyRequest)

            response = client_socket.recv(1024)
            print "\nresponse KDC (E(Kb, [Ks || IDB || IDA || N1]) || E(Ka, [Ks || IDB])):\n" + response

            response = response.split('\n\n')
            untuk_B = response[0].split('\n')

            cek_IDB = des(key_B, untuk_B[1]).decrypt(untuk_B[1])
            cek_IDA = des(key_B, untuk_B[2]).decrypt(untuk_B[2])
            cek_Nonce1 = des(key_B, untuk_B[3]).decrypt(untuk_B[3])
            if(cek_IDA==ID_A and cek_IDB==ID_B and cek_Nonce1==Nonce1):
                    print "\nresponse KDC terverifikasi"
                    keySession = des(key_B, untuk_B[0]).decrypt(untuk_B[0])
                    print "key session: " + keySession

                    raw_input('nyalakan peer (enter)')

                    client_socket.close()

                    #di sini bob mengirimkan sebagian response KDC yang dienkripsi dengan KA pada alice
                    servera_address = ('127.0.0.1', 5001)
                    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket2.connect(servera_address)

                    client_socket2.send(response[1])
                    print "\nmengirim response KDC untuk Alice (E(KA, [Ks || IDB])):"
                    print response[1]

                    #di sini alice menerima response bob
                    bob_response = client_socket2.recv(1024)
                    print "\nmenerima response nonce2 dari Alice (E(Ks, N2)):"
                    print bob_response
                    Nonce2 = des(keySession, bob_response).decrypt(bob_response)
                    print "nonce 2 adalah: " + Nonce2
                    Nonce2 = '11111112'
                    print "nonce 2 modifikasi: " + Nonce2

                    #di sini alice mengirim response alice pada bob
                    encryptedResponse = des(keySession, Nonce2).encrypt(Nonce2)
                    print("\nmengirim balik nonce 2 modifikasi ke Alice (E(Ks, f(N2))):")
                    print encryptedResponse
                    client_socket2.send(encryptedResponse)

            else:
                    print "response KDC tidak terverifikasi"

except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)

