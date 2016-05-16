import socket
import select
import sys
import random
from DES_bs import des

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

#keylibrary
keyList = []
ID_A = ('00000001', '12345678')
keyList.append(ID_A)
ID_B = ('00000002', '23456789')
keyList.append(ID_B)

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:               
                data = sock.recv(1024)
                encryptedResponse = ""

                if data:
                    print "menerima data request key session (IDA || IDB || N1)"
                    print data
                    message = data.split('\n')

                    #random keySession
                    keySession = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
                    print "\nkey session: " + keySession

                    key = ""

                    #cek ID 1
                    i=0;
                    while i<len(keyList):
                        if keyList[i][0]==message[0]:
                            key = keyList[i][1]
                            break
                        else:
                            i=i+1

                    encryptedResponse = des(key, keySession).encrypt(keySession) + '\n' + des(key, message[0]).encrypt(message[0]) + '\n' + des(key, message[1]).encrypt(message[1]) + '\n' + des(key, message[2]).encrypt(message[2]) + '\n\n'
                    #print encryptedResponse

                    #cek ID 2
                    i=0;
                    while i<len(keyList):
                        if keyList[i][0]==message[1]:
                            key=keyList[i][1]
                            break
                        else:
                            i=i+1

                    encryptedResponse = encryptedResponse + des(key, keySession).encrypt(keySession) + '\n' + des(key, message[0]).encrypt(message[0])

                    print "\nrespon terenkripsi dari KDC (E(Ka, [Ks || IDA || IDB || N1]) || E(Kb, [Ks || IDA])):\n" + encryptedResponse
                    sock.send(encryptedResponse)

                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
