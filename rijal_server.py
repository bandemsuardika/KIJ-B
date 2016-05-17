

import sys
import socket
import select

server_address = ('localhost', 10000)
SOCKET_LIST = []
RECV_BUFFER = 4096
USER_LIST = { }
ADDR_LIST = { }

def chat_server():

    # Create a TCP/IP socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind the socket to the port
    ser_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, 'Masuk %s port %s' % server_address
    ser_sock.bind(server_address)

    # Listen for incoming connections
    ser_sock.listen(10)

    SOCKET_LIST.append(ser_sock)


    while True:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:

            if sock == ser_sock:
                connection, client_address = ser_sock.accept()
                SOCKET_LIST.append(connection)
		#print "%s" %connection
		#datax = connection.recv(RECV_BUFFER)
		#print "%s" % datax
		#datax1 = datax.split(' ',1)[0]
		#datax2 = datax.split(' ',1)[1]
		#x1 = "('%s', %s)" %client_address
		#print "%s" %x1
    		#USER_LIST[x1] = datax2.replace("\n","")

		#print "Client ", USER_LIST[x1], " terkoneksi"
		print "Client (%s, %s) terkoneksi" % client_address

                #broadcast(ser_sock, connection, "\n[%s:%s] masuk ke dalam chat room\n" % client_address)

            else:
		try:
                    data = sock.recv(RECV_BUFFER)
		    if data:
			    data1 = data.split(' ',1)[0]
			    #data3 = data2.split(' ',1)[0]
			    #print "%s" %data2
			    #print "%s" %data3
			    #data4 = data2.split(' ',1)[1]
			    #data5 = data4.split(' ',1)[0]
			    #data6 = data4.split(' ',1)[0]

			    print "cekoceko"
			    #addr2 = str(sock.getpeername())
			    #name = USER_LIST["%s" %addr2]

			    if data1 == "login":
                                data2 = data.split(' ',1)[1]
				flag = True
				for xlist, xname in USER_LIST.iteritems():
					if data2.replace("\n","") == xname :
						flag = False
				if flag == True :
					ADDR_LIST[data2.replace("\n","")] = sock
					USER_LIST[sock] = data2.replace("\n","")
					print "%s" % ADDR_LIST[data2.replace("\n","")]
					selfy = USER_LIST[sock]
					print "%s" %selfy
					broadcast(ser_sock, connection, "\r" + '[' + selfy + '] ' + "Masuk ke dalam chat room\n")
				else :
					sock.send("\nNama sudah dipakai\n");

			    elif data1 == "send":
                                data2 = data.split(' ',1)[1]
				data3 = data2.split(' ',1)[0]
				data4 = data2.split(' ',1)[1]
			    	data5 = data4.split(' ',1)[0]
			    	data6 = data4.split(' ',1)[0]
				print "cek1"
				print "%s" % data3
				#print "%s" % ADDR_LIST[data3.replace("\n","")]
				flag = False
				for xlist, xname in USER_LIST.iteritems():
					if xname == data3 :
						flag = True

				if flag == True :
					private(ser_sock, sock, "\r" + '[' + selfy  + '] ' + data4, data3)
				elif flag == False :
					print("No User\n");

			    elif data1 == "sendall":
                                data2 = data.split(' ',1)[1]
				broadcast(ser_sock, sock, "\r" + '[' + selfy + '] ' + data2)
			    elif data1.replace("\n","") == "liston":
				print "wewewe\n"
				liston(sock, ser_sock)
			    else :
				print "perintah salah\n"
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(ser_sock, sock, "Client (%s, %s) diskonek \n" % client_address)
		except:
		    print "cek"
                    broadcast(ser_sock, sock, "Client (%s, %s) offline\n" % client_address)
                    continue

    ser_sock.close()


def broadcast (ser_sock, sock, message):
    for socket in SOCKET_LIST:
        if socket != ser_sock and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)



def private (ser_sock, sock, message, data2):

    for name, sockaddr in ADDR_LIST.iteritems():
	if sockaddr == sock :
	    print "nama %s" % data2
	    socket = ADDR_LIST[data2.replace("\n","")]
	    print "czec"
	    print "%s" % message
	    try :
		socket.send(message)
	    except :
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)

def liston (sock, ser_sock) :
	onlist = "\nList yang Online:\n"
	print "%s" % onlist
	for socket in SOCKET_LIST :
		for xname, xlist in ADDR_LIST.iteritems() :
			if socket == xlist :
				onlist += (xname + " on\n")
	try:
		sock.send(onlist)
	except:
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
#    for socket in SOCKET_LIST:
#        if socket != ser_sock and socket != sock:
#		for addr, user in USER_LIST.items():
#			if user == data2:
#           			try :
#                			socket.send(message)
#            			except :
#                			socket.close()
#                		if socket in SOCKET_LIST:
#                    			SOCKET_LIST.remove(socket)

if __name__ == "__main__":

    sys.exit(chat_server())

    __author__ = 'Ilham'
