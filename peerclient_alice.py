import socket
import select
import sys
from DES_bs import des

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

servera_address = ('127.0.0.1', 5001)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(servera_address)
server_socket.listen(5)

input_socket = [server_socket]

x=raw_input('apakah mau memulai chat? (y/n)')
if x=='y':
    initiate = 1
else:
    initiate = 0

ID_A = '00000001'
ID_B = '00000002'
key_A = '12345678'
Nonce1 = '87654321'
Nonce2 = '11111111'

try:
        if(initiate==1):
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

                        raw_input('nyalakan peer (enter)')

                        client_socket.close()

                        #di sini alice mengirimkan sebagian response KDC yang dienkripsi dengan Kb pada bob
                        serverb_address = ('127.0.0.1', 5002)
                        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket2.connect(serverb_address)

                        client_socket2.send(response[1])
                        print "\nmengirim response KDC untuk Bob (E(Kb, [Ks || IDA])):"
                        print response[1]

                        #di sini alice menerima response bob
                        bob_response = client_socket2.recv(1024)
                        print "\nmenerima response nonce2 dari Bob (E(Ks, N2)):"
                        print bob_response
                        Nonce2 = des(keySession, bob_response).decrypt(bob_response)
                        print "nonce 2 adalah: " + Nonce2
                        Nonce2 = '11111112'
                        print "nonce 2 modifikasi: " + Nonce2

                        #di sini alice mengirim response alice pada bob
                        encryptedResponse = des(keySession, Nonce2).encrypt(Nonce2)
                        print("\nmengirim balik nonce 2 modifikasi ke Bob (E(Ks, f(N2))):")
                        print encryptedResponse
                        client_socket2.send(encryptedResponse)

                else:
                        print "response KDC tidak terverifikasi"

        else:
                while True:
                        read_ready, write_ready, exception = select.select(input_socket, [], [])

                        for sock in read_ready:
                            if sock == server_socket:
                                client_socket, client_address = server_socket.accept()
                                input_socket.append(client_socket)

                            else:
                                data = sock.recv(1024)
                                if data:
                                    print "menerima response KDC dari bob (E(Kb, [Ks || IDA])):"
                                    print data
                                    untuk_B=data.split('\n')

                                    cek2_IDB=des(key_A, untuk_B[1]).decrypt(untuk_B[1])
                                    if(cek2_IDB==ID_B):
                                        print "\nID B terverifikasi"
                                        keySession = des(key_A, untuk_B[0]).decrypt(untuk_B[0])
                                        print "key session: " + keySession

                                    toBeEncrypted = str(Nonce2)
                                    encryptedResponse = des(keySession, toBeEncrypted).encrypt(toBeEncrypted)
                                    print "\nnonce 2: " + str(Nonce2)
                                    print "mengirim encrypted nonce2 pada bob (E(Ks, N2)):"
                                    print encryptedResponse
                                    sock.send(encryptedResponse)

                                    data2 = sock.recv(1024)
                                    print "\nmenerima response dari bob (E(Ks, f(N2))):"
                                    print data2
                                    Nonce2mod = des(keySession, data2).decrypt(data2)
                                    print "nonce 2 modifikasi:"
                                    print Nonce2mod

                                else:
                                    sock.close()
                                    input_socket.remove(sock)


except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)
