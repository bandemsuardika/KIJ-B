import sys
import socket
import select

def chat_client():
#    if(len(sys.argv) < 3) :
#        print 'Usage : python chat_client.py hostname port'
#        sys.exit()

#    host = sys.argv[1]
#    port = int(sys.argv[2])

    # Create a TCP/IP socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.settimeout(2)

    # Connect the socket to the port where the server is listening

    while True:
	    print "Terkoneksi dengan host\n"
	    print "\nMenu Command:\n 1. send = untuk private message\n 2. sendall = untuk broadcast\n 3. liston = untuk list yang online\n 4. login = untuk login pertama kali dikuti nama\n"
	    inp = sys.stdin.readline()
	    inp1 = inp.split(' ', 1)[0]

	    if inp1=="login":
		print("Logged on, start chatting");
		break
	    else :
		print "You Must Login"

    try :
        client_sock.connect(('localhost', 10000))
    except :
        print 'Gagal Konek'
        sys.exit()

    inp2 = inp.split(' ',1)[1]
    client_sock.sendall(inp)

    sys.stdout.write('[Saya] '); sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, client_sock]

        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:
            if sock == client_sock:
                data = sock.recv(4096)
                if not data :
                    print '\nDiskonek'
                    sys.exit()
                else :
                    sys.stdout.write(data)
		    if data == "\nNama sudah dipakai\n" :
			sys.exit()
		    else :
                        sys.stdout.write('[Saya] '); sys.stdout.flush()

            else :
                msg = sys.stdin.readline()
                client_sock.send(msg)
                sys.stdout.write('[Saya] '); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())
